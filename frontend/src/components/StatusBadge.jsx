export function StatusBadge({ active }) {
  return <span className={active ? "badge success" : "badge muted"}>{active ? "Active" : "Inactive"}</span>;
}

