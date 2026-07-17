export function Dashboard() {
  const cards = [
    { label: "Services", value: "4", caption: "API, web, worker, ingress" },
    { label: "Controls", value: "18", caption: "Baseline policy checks" },
    { label: "Environments", value: "3", caption: "dev, staging, prod" }
  ];

  return (
    <section>
      <header className="page-header">
        <h2>Risk Lab Dashboard</h2>
        <p>Secure baseline used to generate realistic review scenarios.</p>
      </header>
      <div className="metric-grid">
        {cards.map((card) => (
          <article className="metric-card" key={card.label}>
            <span>{card.label}</span>
            <strong>{card.value}</strong>
            <p>{card.caption}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

