import { apiGet, apiPost } from "./client";
import type {
  ScenarioRun,
  StressScenarioRequest,
  StressScenarioResponse,
} from "../types/scenario";

export function runStressScenario(
  bookId: string,
  request: StressScenarioRequest,
): Promise<StressScenarioResponse> {
  return apiPost<StressScenarioResponse, StressScenarioRequest>(
    `/api/scenarios/books/${bookId}/stress`,
    request,
  );
}

export function runAndPersistStressScenario(
  bookId: string,
  request: StressScenarioRequest,
): Promise<ScenarioRun> {
  return apiPost<ScenarioRun, StressScenarioRequest>(
    `/api/scenarios/books/${bookId}/stress-runs`,
    request,
  );
}

export function getScenarioRuns(bookId: string): Promise<ScenarioRun[]> {
  return apiGet<ScenarioRun[]>(`/api/scenarios/books/${bookId}/runs`);
}