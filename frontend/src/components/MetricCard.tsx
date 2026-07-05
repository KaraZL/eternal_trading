type MetricCardProps = {
  label: string;
  value: string | number | null;
};

export function MetricCard({ label, value }: MetricCardProps) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value ?? "N/A"}</strong>
    </div>
  );
}