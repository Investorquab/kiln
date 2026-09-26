const stages = [
  ["01", "Specify", "Turn requirements into a concrete plan and guarantees."],
  ["02", "Model", "Derive state, transitions, dependencies, and invariants."],
  ["03", "Build", "Implement the approved slice with executable tests."],
  ["04", "Attack", "Try to break the declared guarantees."],
  ["05", "Repair", "Diagnose failures and add regression coverage."],
  ["06", "Verify", "Independently reproduce critical scenarios."],
];

export default function Home() {
  return (
    <main className="shell">
      <section className="hero">
        <div className="eyebrow">AUTONOMOUS SOFTWARE FACTORY</div>
        <h1>Kiln</h1>
        <p className="lede">Build software. Attack it. Repair it. Prove it.</p>
        <p className="copy">Kiln turns requirements into working software and then treats its own implementation as hostile until independent verification produces evidence.</p>
      </section>

      <section className="loop" aria-label="Factory stages">
        {stages.map(([number, title, description]) => (
          <article className="stage" key={number}>
            <span className="number">{number}</span>
            <h2>{title}</h2>
            <p>{description}</p>
          </article>
        ))}
      </section>

      <section className="demo">
        <div>
          <div className="eyebrow">LIVE WORKLOAD</div>
          <h2>Tablekeeper reservation service</h2>
          <p>Clean-room workload for demonstrating concurrency safety, idempotency, timezone normalization, and transactional correctness.</p>
        </div>
        <div className="status"><span /> Verification harness ready</div>
      </section>
    </main>
  );
}
