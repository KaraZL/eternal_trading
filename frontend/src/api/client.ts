// Read the API URL from .env (Vite only exposes vars prefixed with VITE_
// on import.meta.env). Falls back to the backend's default address if unset.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string ?? 'http://127.0.0.1:8000';

// Reusable helper for GET requests. <T> is a generic - the caller decides
// what shape of data comes back, e.g. apiGet<Book[]>('/api/books').
export async function apiGet<T>(path: string): Promise<T> {
    // Send the request to baseURL + path, e.g. http://127.0.0.1:8000/api/books
    // `await` pauses here until the response arrives.
    const response = await fetch(`${API_BASE_URL}${path}`);

    // response.ok is true for status codes 200-299 (success).
    // So we throw when it's NOT ok (i.e. an error response).
    if (!response.ok) {
        throw new Error(`GET ${path} failed with status ${response.status}`)
    }

    // Parse the response body as JSON, and tell TypeScript to treat it as type T.
    return response.json() as Promise<T>;
}

// Reusable helper for POST requests. Two generics here, not one:
// - TBody: the shape of the data you're sending (the request payload).
// - TResponse: the shape of the data you expect back (like T in apiGet).
// They're independent - sending a TradeOrderRequest can come back as a TradeOrderResponse.
export async function apiPost<TResponse, TBody>(path: string, body: TBody, ): Promise<TResponse> {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        // GET is fetch's default method, so apiGet didn't need to say it.
        // POST has to be explicit.
        method: "POST",
        headers: {
            // Tells the server "the body I'm sending is JSON text",
            // so it knows how to parse it (FastAPI/pydantic relies on this).
            "Content-Type": "application/json",
        },
        // fetch can only send strings/binary data over the network, not raw
        // JS objects - JSON.stringify turns `body` into a JSON string first.
        body: JSON.stringify(body),
    });

    if (!response.ok) {
        // Unlike apiGet, this reads the error body as text before throwing,
        // so the error message includes whatever detail the backend sent
        // (e.g. FastAPI's validation error messages), not just the status code.
        const errorText = await response.text();
        throw new Error(`POST ${path} failed with status ${response.status}: ${errorText}`)
    }

    // Same idea as apiGet: parse the JSON response and tell TypeScript
    // to treat it as TResponse (a type assertion, not a runtime check).
    return response.json() as Promise<TResponse>;
}