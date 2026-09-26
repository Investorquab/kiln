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
  ["Architect", "Plan"],
  ["Modeler", "Specify"],
  ["Builder", "Build"],
  ["Adversary", "Attack"],
  ["Repairer", "Repair"],
  ["Verifier", "Verify"],
];

export default function Home() {
  return (
    <main className="shell">
      <section className="hero">
        <div className="eyebrow">AUTONOMOUS SOFTWARE FACTORY / KILN</div>
        <h1>Build it.<br />Break it.<br />Prove it.</h1>
        <p className="lede">Software that earns its green check.</p>
        <p className="copy">
          Kiln turns requirements into working software, attacks its own
          implementation, repairs reproducible failures, and independently
          verifies the final result.
        </p>
        <div className="hero-meta">
          <span>6 generic agent seats</span>
          <span>4 adversarial scenarios</span>
          <span>1 evidence chain</span>
        </div>
      </section>

      <section className="section-head">
        <div className="eyebrow">FACTORY LOOP</div>
        <h2>From requirement to evidence.</h2>
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
        <div className="eyebrow">AGENT BAND</div>
        <h2>Specialists hand off evidence, not assumptions.</h2>
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
        <div className="eyebrow">ADVERSARIAL LAYER</div>
        <h2>Don't trust the implementation. Try to break it.</h2>
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

      <section className="demo">
        <div>
          <div className="eyebrow">DEMONSTRATION WORKLOAD</div>
          <h2>Tablekeeper reservation service</h2>
          <p>
            A clean-room reservation workload used to expose concurrency,
            idempotency, timezone, and boundary correctness.
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
