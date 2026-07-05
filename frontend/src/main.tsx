// StrictMode: a dev-only wrapper that helps catch bugs by intentionally
// double-invoking things like component renders and effects. It doesn't
// affect production builds, and renders no visible UI itself.
import { StrictMode } from "react";
// createRoot: React 18+'s API for mounting a React app into a real DOM node.
import { createRoot } from "react-dom/client";
// BrowserRouter: enables client-side routing (URL changes without full page
// reloads). It has to wrap anything that uses routes/links (like <App />).
import { BrowserRouter } from "react-router-dom";
// QueryClient / QueryClientProvider: react-query's cache + config object,
// and the provider that makes it available to every component in the tree.
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import App from "./App";
// Global stylesheet - imported here (not in App.tsx) so it's the very
// first thing loaded, before any component renders.
import "./styles.css";

// One QueryClient for the whole app. It holds the cache for every
// api call made with react-query. Nothing calls useQuery yet (pages/
// are still empty) - this just makes the hook usable once they do,
// e.g. useQuery({ queryKey: ['books'], queryFn: getBooks }) in BooksPage.tsx.
const queryClient = new QueryClient();

// Two unrelated "root"s here, despite the shared name:
// 1. "root" (the string) - the id of the actual <div id="root"></div>
//    sitting in index.html, before any React code has run.
// 2. createRoot (the function) - imported from react-dom/client above.
//    It's not related to the div's id, it just happens to share the word
//    by convention. It takes that DOM element and turns it into a
//    "React root": an internal object React uses to manage everything
//    it renders inside that div from now on.
//
// getElementById returns `HTMLElement | null` (it can't know at compile
// time whether the element exists). The "!" is a non-null assertion -
// it tells TypeScript "trust me, this won't be null", since we know
// index.html always has this div. It does NOT check this at runtime -
// if the div were missing, this would crash instead.
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    {/* Makes `queryClient` available to any component below via hooks
        like useQuery/useMutation, without passing it down manually. */}
    <QueryClientProvider client={queryClient}>
      {/* Enables <Link>, useNavigate, useParams, <Routes> etc. inside App. */}
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
);
