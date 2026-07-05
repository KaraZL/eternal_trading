import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { getBookRiskSummary } from "../api/books";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { MetricCard } from "../components/MetricCard";

export function BookRiskPage() {
  const { bookId } = useParams();

  const { data, isLoading, error } = useQuery({
    queryKey: ["book-risk", bookId],
    queryFn: () => getBookRiskSummary(bookId!),
    enabled: Boolean(bookId),
  });

  if (isLoading) return <LoadingState />;
  if (error) return <ErrorState message={(error as Error).message} />;
  if (!data) return <ErrorState message="No risk summary found." />;

  return (
    <section>
      <h2>{data.book_name} — Risk Summary</h2>

      <div className="metric-grid">
        <MetricCard label="Risk status" value={data.risk_status} />
        <MetricCard label="Weighted LTV" value={data.weighted_ltv} />
        <MetricCard label="Loan exposure" value={data.total_loan_exposure} />
        <MetricCard label="Eligible collateral" value={data.total_eligible_collateral_value} />
        <MetricCard label="Collateral market value" value={data.total_collateral_market_value} />
        <MetricCard label="Position market value" value={data.total_position_market_value} />
        <MetricCard label="Loans" value={data.loan_count} />
        <MetricCard label="Positions" value={data.position_count} />
        <MetricCard label="Pending orders" value={data.pending_trade_order_count} />
        <MetricCard label="Executed orders" value={data.executed_trade_order_count} />
      </div>
    </section>
  );
}