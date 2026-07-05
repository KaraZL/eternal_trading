// WHAT THIS PAGE DOES, IN GENERAL:
// It's the page rendered at "/books/:bookId/risk" (see App.tsx). It reads
// the book's id from the URL, asks the backend for that book's risk
// numbers (LTV, exposure, collateral value, etc.), and while waiting/on
// failure shows a loading or error message instead. Once the data arrives,
// it renders one <MetricCard> per number, in a grid.
//
// The general shape (params -> useQuery -> loading/error/data branches ->
// render) is the same pattern you'll repeat in BookDetailPage, ScenarioPage,
// TradeOrdersPage, etc. - it's the standard "fetch and display" page.

import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { getBookRiskSummary } from "../api/books";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { MetricCard } from "../components/MetricCard";

export function BookRiskPage() {
  // Pull :bookId out of the current URL, e.g. "/books/abc-123/risk" -> "abc-123".
  const { bookId } = useParams();

  // useQuery does three things for you:
  // 1. Calls queryFn (getBookRiskSummary) when the component mounts.
  // 2. Caches the result under queryKey - if you leave this page and come
  //    back, react-query can show the cached data instantly while it
  //    re-fetches in the background, instead of a blank loading screen.
  // 3. Gives you back isLoading/error/data so you don't manage that state
  //    by hand with useState/useEffect.
  const { data, isLoading, error } = useQuery({
    // The cache key. Includes bookId so risk data for book A is never
    // confused with cached data for book B.
    queryKey: ["book-risk", bookId],
    // bookId is typed as `string | undefined` (URL params might not match).
    // The "!" tells TypeScript "trust me, it's defined" - safe here only
    // because `enabled` below stops this from running when it isn't.
    queryFn: () => getBookRiskSummary(bookId!),
    // Don't fire the request at all until bookId actually has a value.
    enabled: Boolean(bookId),
  });

  // Three early returns, checked in order: still loading, failed, or
  // succeeded-but-empty. Only if none of these apply do we fall through
  // to the real render below - this keeps the JSX after this point able
  // to assume `data` is a valid, loaded BookRiskSummary.
  if (isLoading) return <LoadingState />;
  if (error) return <ErrorState message={(error as Error).message} />;
  if (!data) return <ErrorState message="No risk summary found." />;

  return (
    <section>
      <h2>{data.book_name} — Risk Summary</h2>

      {/* One MetricCard per number from the backend's risk-summary response.
          MetricCard just renders a label + value pair, falling back to
          "N/A" if the value is null (e.g. weighted_ltv can be null when a
          book has no loans/collateral yet - see BookRiskResponse on the backend). */}
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
