from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(title="Kiln Tablekeeper Demo", version="0.1.0")


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


_store: dict[str, Reservation] = {}
_idempotency: dict[str, Reservation] = {}


def canonical_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return value.astimezone(timezone.utc)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/reservations", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation(
    request: ReservationRequest,
    idempotency_key: str = Header(min_length=1, alias="Idempotency-Key"),
) -> Reservation:
    start = canonical_utc(request.start_at)
    end = canonical_utc(request.end_at)

    if end <= start:
        raise HTTPException(status_code=422, detail="end_at must be after start_at")

    previous = _idempotency.get(idempotency_key)
    if previous:
        return previous

    for existing in _store.values():
        if existing.resource_id != request.resource_id:
            continue
        overlaps = start < existing.end_at and existing.start_at < end
        if overlaps:
            raise HTTPException(status_code=409, detail="resource is already reserved")

    reservation = Reservation(
        id=uuid4(),
        resource_id=request.resource_id,
        start_at=start,
        end_at=end,
        guest_name=request.guest_name,
        idempotency_key=idempotency_key,
    )
    _store[str(reservation.id)] = reservation
    _idempotency[idempotency_key] = reservation
    return reservation
