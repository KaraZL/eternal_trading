// Navigate: a component that redirects when rendered (used below for "/").
// Route / Routes: the building blocks of react-router - Routes looks at the
// current URL and renders whichever Route matches it.
import { Navigate, Route, Routes } from "react-router-dom";

import { Layout } from "./components/Layout";
import { BooksPage } from "./pages/BooksPage";
import { BookDetailPage } from "./pages/BookDetailPage";
import { BookRiskPage } from "./pages/BookRiskPage";
import { ScenarioPage } from "./pages/ScenarioPage";
import { TradeOrdersPage } from "./pages/TradeOrdersPage";

export default function App() {
  return (
    // <Routes> scans its children and renders only the one whose path
    // matches the current URL - never more than one at a time.
    <Routes>
      {/* This <Route> has no `path`, so it always matches - it's a "layout
          route". Its job is just to render <Layout>, which presumably has
          an <Outlet /> inside it somewhere: that's where whichever nested
          route below matches actually gets rendered. This is how you share
          a navbar/header across every page without repeating it. */}
      <Route element={<Layout />}>
        {/* Visiting "/" doesn't show a page itself - it immediately
            redirects to "/books" via <Navigate>. `replace` means it swaps
            the current history entry instead of adding a new one, so
            clicking the browser's back button won't bounce you back to
            "/" (it'll skip past it, since it was never really "visited"). */}
        <Route path="/" element={<Navigate to="/books" replace />} />

        {/* Plain static route: URL "/books" -> render <BooksPage />. */}
        <Route path="/books" element={<BooksPage />} />

        {/* ":bookId" is a dynamic URL segment (a route param). Visiting
            e.g. "/books/abc-123" matches this route, and "abc-123" becomes
            available inside BookDetailPage via the useParams() hook. */}
        <Route path="/books/:bookId" element={<BookDetailPage />} />

        {/* Same param pattern, different sub-page for the same book. */}
        <Route path="/books/:bookId/risk" element={<BookRiskPage />} />
        <Route path="/books/:bookId/scenarios" element={<ScenarioPage />} />

        {/* A route unrelated to a specific book. */}
        <Route path="/trade-orders" element={<TradeOrdersPage />} />
      </Route>
    </Routes>
  );
}
