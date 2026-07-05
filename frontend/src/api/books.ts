import { apiGet } from "./client";
import type { Book } from "../types/book";
import type { BookRiskSummary } from "../types/risk";

export function getBooks(): Promise<Book[]> {
    return apiGet<Book[]>("api/books");
}

export function getBookRiskSummary(bookId: string): Promise<BookRiskSummary> {
    return apiGet<BookRiskSummary>(`api/books/${bookId}/risk_summary`);
}