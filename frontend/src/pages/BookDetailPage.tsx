import { Link, useParams } from "react-router-dom";

export function BookDetailPage() {
  const { bookId } = useParams();

  return (
    <section>
      <h2>Book Detail</h2>
      <p className="muted">Book ID: {bookId}</p>

      <div className="action-grid">
        <Link className="action-card" to={`/books/${bookId}/risk`}>
          Risk Summary
        </Link>

        <Link className="action-card" to={`/books/${bookId}/scenarios`}>
          Scenarios
        </Link>
      </div>
    </section>
  );
}