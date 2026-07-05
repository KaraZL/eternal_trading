// Link: like an <a>, but intercepts the click and lets react-router change
// the URL/page without a full browser page reload (that's the whole point
// of a single-page app - no white-flash reload between pages).
// Outlet: a placeholder - "render whichever nested route matched here."
import { Link, Outlet } from "react-router-dom"

// This is the component App.tsx registers as the parent/layout route
// (<Route element={<Layout />}>). It renders once and stays on screen
// while only the <Outlet /> content changes as you navigate between pages.
export function Layout() {
    return (
        <div className="app-shell">
            {/* Sidebar: always visible, regardless of which page is active. */}
            <aside className="sidebar">
                <h1>RiskBook AI</h1>
                <nav>
                    {/* `to="/books"` - clicking this changes the URL to /books.
                        react-router then re-renders <Outlet /> below with
                        whatever component App.tsx mapped to that path
                        (BooksPage). Using <Link> instead of <a href="/books">
                        avoids a full page reload, so the sidebar/state don't
                        get wiped out on every navigation. */}
                    <Link to="/books">Books</Link>
                    <Link to="/trade-orders">Trade Orders</Link>
                </nav>
            </aside>

            <main className="main-content">
                {/* This is where the matched page actually renders - e.g.
                    BooksPage, BookDetailPage, TradeOrdersPage, etc, depending
                    on the current URL. Without <Outlet />, nested routes
                    would match but never actually show anything. */}
                <Outlet />
            </main>
        </div>
    );
}
