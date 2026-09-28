from datetime import datetime, timezone
from uuid import UUID, uuid4

import os
import psycopg
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field


DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://kiln:kiln@localhost:5432/kiln",
)

app = FastAPI(title="Kiln Tablekeeper Demo", version="0.4.0")


class ReservationRequest(BaseModel):
    resource_id: str = Field(min_length=1)
    start_at: datetime
    end_at: datetime
    guest_name: str = Field(min_length=1, max_length=120)


class Reservation(BaseModel):
    id: UUID
    resource_id: str
    start_at: datetime
    end_at: datetime
    guest_name: str
    idempotency_key: str
    status: str
    cancelled_at: datetime | None


def canonical_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return value.astimezone(timezone.utc)


def connection():
    return psycopg.connect(DATABASE_URL)


def ensure_schema() -> None:
    with connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id uuid PRIMARY KEY,
                resource_id text NOT NULL,
                start_at timestamptz NOT NULL,
                end_at timestamptz NOT NULL,
                guest_name text NOT NULL,
                idempotency_key text NOT NULL UNIQUE,
                status text NOT NULL DEFAULT 'active',
                cancelled_at timestamptz,
                CHECK (end_at > start_at),
                CHECK (status IN ('active', 'cancelled'))
            )
            """
        )
        conn.execute(
            "ALTER TABLE reservations ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'active'"
        )
        conn.execute(
            "ALTER TABLE reservations ADD COLUMN IF NOT EXISTS cancelled_at timestamptz"
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cancellation_requests (
                idempotency_key text PRIMARY KEY,
                reservation_id uuid NOT NULL REFERENCES reservations(id),
                created_at timestamptz NOT NULL DEFAULT now()
            )
            """
        )
        conn.commit()


@app.on_event("startup")
def startup() -> None:
    ensure_schema()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def row_to_reservation(row) -> Reservation:
    return Reservation(
        id=row[0],
        resource_id=row[1],
        start_at=row[2],
        end_at=row[3],
        guest_name=row[4],
        idempotency_key=row[5],
        status=row[6],
        cancelled_at=row[7],
    )


@app.get("/reservations", response_model=list[Reservation])
def list_reservations() -> list[Reservation]:
    with connection() as conn:
        rows = conn.execute(
            """
            SELECT id, resource_id, start_at, end_at, guest_name, idempotency_key, status, cancelled_at
            FROM reservations
            ORDER BY start_at, id
            """
        ).fetchall()
    return [row_to_reservation(row) for row in rows]


@app.post(
    "/reservations",
    response_model=Reservation,
    status_code=status.HTTP_201_CREATED,
)
def create_reservation(
    request: ReservationRequest,
    idempotency_key: str = Header(min_length=1, alias="Idempotency-Key"),
) -> Reservation:
    try:
        start = canonical_utc(request.start_at)
        end = canonical_utc(request.end_at)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if end <= start:
        raise HTTPException(status_code=422, detail="end_at must be after start_at")

    reservation_id = uuid4()

    try:
        with connection() as conn:
            with conn.transaction():
                # Serialize reservations for the same resource. The overlap
                # check and insert therefore share one atomic critical section.
                conn.execute(
                    "SELECT pg_advisory_xact_lock(hashtextextended(%s, 0))",
                    (request.resource_id,),
                )
                # Idempotency keys are globally unique, so serialize their
                # lookup/creation path as well. This also prevents a same-key
                # race across different resources from becoming a raw
                # database unique-constraint error.
                conn.execute(
                    "SELECT pg_advisory_xact_lock(hashtextextended(%s, 0))",
                    (f"idempotency:{idempotency_key}",),
                )

                existing = conn.execute(
                    """
                    SELECT id, resource_id, start_at, end_at, guest_name, idempotency_key, status, cancelled_at
                    FROM reservations
                    WHERE idempotency_key = %s
                    """,
                    (idempotency_key,),
                ).fetchone()

                if existing:
                    previous = row_to_reservation(existing)
                    if (
                        previous.resource_id != request.resource_id
                        or previous.start_at != start
                        or previous.end_at != end
                        or previous.guest_name != request.guest_name
                    ):
                        raise HTTPException(
                            status_code=409,
                            detail="idempotency key was already used for a different request",
                        )
                    return previous

                conflict = conn.execute(
                    """
                    SELECT 1
                    FROM reservations
                    WHERE resource_id = %s
                      AND status = 'active'
                      AND start_at < %s
                      AND %s < end_at
                    LIMIT 1
                    """,
                    (request.resource_id, end, start),
                ).fetchone()

                if conflict:
                    raise HTTPException(
                        status_code=409,
                        detail="resource is already reserved",
                    )

                row = conn.execute(
                    """
                    INSERT INTO reservations
                        (id, resource_id, start_at, end_at, guest_name, idempotency_key)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id, resource_id, start_at, end_at, guest_name, idempotency_key, status, cancelled_at
                    """,
                    (
                        reservation_id,
                        request.resource_id,
                        start,
                        end,
                        request.guest_name,
                        idempotency_key,
                    ),
                ).fetchone()

                return row_to_reservation(row)
    except HTTPException:
        raise



@app.delete("/reservations/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(
    reservation_id: UUID,
    idempotency_key: str = Header(min_length=1, alias="Idempotency-Key"),
) -> None:
    try:
        with connection() as conn:
            with conn.transaction():
                conn.execute(
                    "SELECT pg_advisory_xact_lock(hashtextextended(%s, 0))",
                    (f"reservation:{reservation_id}",),
                )
                conn.execute(
                    "SELECT pg_advisory_xact_lock(hashtextextended(%s, 0))",
                    (f"cancel-idempotency:{idempotency_key}",),
                )

                existing_request = conn.execute(
                    """
                    SELECT reservation_id
                    FROM cancellation_requests
                    WHERE idempotency_key = %s
                    """,
                    (idempotency_key,),
                ).fetchone()

                if existing_request:
                    if existing_request[0] != reservation_id:
                        raise HTTPException(
                            status_code=409,
                            detail="idempotency key was already used for a different cancellation",
                        )
                    return None

                reservation = conn.execute(
                    """
                    SELECT status
                    FROM reservations
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (reservation_id,),
                ).fetchone()

                if reservation is None:
                    raise HTTPException(status_code=404, detail="reservation not found")

                if reservation[0] != "active":
                    raise HTTPException(status_code=409, detail="reservation is already cancelled")

                conn.execute(
                    """
                    UPDATE reservations
                    SET status = 'cancelled', cancelled_at = now()
                    WHERE id = %s AND status = 'active'
                    """,
                    (reservation_id,),
                )
                conn.execute(
                    """
                    INSERT INTO cancellation_requests (idempotency_key, reservation_id)
                    VALUES (%s, %s)
                    """,
                    (idempotency_key, reservation_id),
                )
                return None
    except HTTPException:
        raise
