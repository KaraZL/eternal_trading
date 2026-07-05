import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { getBooks } from "../api/books";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";

export function BooksPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["books"],
    queryFn: getBooks,
  });

  if (isLoading) return <LoadingState />;
  if (error) return <ErrorState message={(error as Error).message} />;

  return (
    <section>
      <h2>Books</h2>

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Currency</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((book) => (
              <tr key={book.id}>
                <td>{book.name}</td>
                <td>{book.currency}</td>
                <td>
                  <Link to={`/books/${book.id}`}>Open</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}