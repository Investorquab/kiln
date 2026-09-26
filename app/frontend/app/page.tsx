const stages = [
  ["01", "Specify", "Requirements become a concrete plan and explicit guarantees."],
  ["02", "Model", "State, transitions, dependencies, and invariants are made executable."],
  ["03", "Build", "The approved slice becomes working software with tests."],
  ["04", "Attack", "Adversarial scenarios try to break the declared guarantees."],
  ["05", "Repair", "Failures become reproducible fixes and regression tests."],
  ["06", "Verify", "An independent check confirms the critical evidence."],
];

const attacks = [
  ["Concurrency", "50 competing requests", "Double-booking"],
  ["Idempotency", "3 replays + key reuse", "Duplicate side effects"],
  ["Timezone", "Equivalent UTC/offset windows", "Inconsistent instants"],
  ["Boundary", "Naive timestamps", "Invalid state"],
];

const seats = [
  ["Architect", "Specify"],
  ["Modeler", "Model"],
  ["Builder", "Build"],
  ["Adversary", "Attack"],
  ["Repairer", "Repair"],
  ["Verifier", "Verify"],
];

const workOrder = [
  ["ID", "WO-TABLEKEEPER-001"],
  ["Input", "Clean-room reservation requirement"],
  ["Output", "Verified product + evidence chain"],
  ["Authority", "Verifier evidence"],
];

export default function Home() {
  return (
    <main className="shell">
      <header className="topbar">
        <span className="brand">KILN / FACTORY FLOOR</span>
        <span className="status"><i /> CONTROL PLANE ONLINE</span>
      </header>

      <section className="hero">
        <div className="eyebrow">AUTONOMOUS SOFTWARE FACTORY</div>
        <h1>Build it.<br />Break it.<br />Prove it.</h1>
        <p className="lede">The agent is not the factory. The evidence chain is.</p>
        <p className="copy">
          Kiln turns a replaceable work order into a governed production run:
          specialists hand off artifacts, adversarial checks expose failures,
          repair cycles close the loop, and an independent verifier decides
          whether the result is proved.
        </p>
        <div className="hero-meta">
          <span>6 generic seats</span>
          <span>1 replaceable work order</span>
          <span>Verifier-owned completion</span>
        </div>
      </section>

      <section className="section-head">
        <div className="eyebrow">ACTIVE WORK ORDER</div>
        <h2>Tablekeeper / clean-room reservation workload</h2>
      </section>

      <section className="work-order" aria-label="Active work order">
        {workOrder.map(([label, value]) => (
          <div className="work-item" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </section>

      <section className="section-head">
        <div className="eyebrow">FACTORY LOOP</div>
        <h2>Production is a gated pipeline.</h2>
      </section>

      <section className="loop" aria-label="Factory stages">
        {stages.map(([number, title, description]) => (
          <article className="stage" key={number}>
            <span className="number">{number}</span>
            <h3>{title}</h3>
            <p>{description}</p>
          </article>
        ))}
      </section>

      <section className="section-head attack-head">
        <div className="eyebrow">WORK STATIONS</div>
        <h2>Generic seats. Replaceable workload.</h2>
      </section>

      <section className="seats" aria-label="Generic agent seats">
        {seats.map(([name, role], index) => (
          <article className="seat" key={name}>
            <span className="number">0{index + 1}</span>
            <strong>{name}</strong>
            <span>{role}</span>
          </article>
        ))}
      </section>

      <section className="section-head attack-head">
        <div className="eyebrow">QUALITY CONTROL / ATTACK CELL</div>
        <h2>Every guarantee gets a way to fail.</h2>
      </section>

      <section className="attacks">
        {attacks.map(([name, scenario, target]) => (
          <article className="attack" key={name}>
            <div>
              <span className="attack-name">{name}</span>
              <span className="attack-target">{target}</span>
            </div>
            <p>{scenario}</p>
          </article>
        ))}
      </section>

      <section className="factory-status">
        <div>
          <div className="eyebrow">RUN LEDGER</div>
          <h2>Evidence follows the work.</h2>
          <p>
            Each run records stage status, attempts, artifacts, and evidence
            events. A failed attack moves the run into repair; only a passed
            independent verification can close the factory run as proved.
          </p>
        </div>
        <div className="ledger">
          <div><span>STATE</span><strong>RUNNING</strong></div>
          <div><span>ARTIFACTS</span><strong>6 HANDOFF TYPES</strong></div>
          <div><span>FINAL GATE</span><strong>VERIFIER</strong></div>
        </div>
      </section>

      <section className="demo">
        <div>
          <div className="eyebrow">PRODUCT OUTPUT</div>
          <h2>Tablekeeper reservation service</h2>
          <p>
            The workload is the thing Kiln builds. Kiln itself remains
            workload-agnostic: change the work order, keep the factory.
          </p>
        </div>
        <div className="proof">
          <span className="proof-dot" />
          Evidence-driven verification
        </div>
      </section>
    </main>
  );
}
