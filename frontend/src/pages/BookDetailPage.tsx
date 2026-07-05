import { Link, useParams } from "react-router-dom";

export function BookDetailPage() {
  // useParams() reads the dynamic segments from the current URL, matched
  // against the route pattern in App.tsx: "/books/:bookId". If the URL is
  // "/books/abc-123", then bookId === "abc-123" here.
  const { bookId } = useParams();

  return (
    <section>
      <h2>Book Detail</h2>
      <p className="muted">Book ID: {bookId}</p>

      <div className="action-grid">
        {/* These <Link>s just change the browser URL - they don't call the
            backend. Clicking this one navigates to "/books/abc-123/risk",
            which App.tsx matches to <Route path="/books/:bookId/risk"
            element={<BookRiskPage />} />, so BookRiskPage renders next.
            It's BookRiskPage's own job (once written) to then call the
            actual API endpoint (/api/books/{bookId}/risk-summary) to fetch data. */}
        <Link className="action-card" to={`/books/${bookId}/risk`}>
          Risk Summary
        </Link>

        {/* Same idea, routes to the scenarios page for this book. */}
        <Link className="action-card" to={`/books/${bookId}/scenarios`}>
          Scenarios
        </Link>
      </div>
    </section>
  );
}
