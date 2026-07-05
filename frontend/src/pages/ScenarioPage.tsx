// WHAT THIS PAGE DOES, IN GENERAL:
// Rendered at "/books/:bookId/scenarios" (see App.tsx). Lets the user fill
// in a scenario name + shock percentages, then either:
//   - "Preview" it: ask the backend to compute the impact WITHOUT saving it
//   - "Run and save": same calculation, but persisted as a ScenarioRun
// and shows a table of previously saved runs for this book below.

import { type SubmitEvent, useState } from "react";
import { useParams } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  getScenarioRuns,
  runAndPersistStressScenario,
  runStressScenario,
} from "../api/scenarios";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import type { StressScenarioResponse } from "../types/scenario";

export function ScenarioPage() {
  const { bookId } = useParams();
  const queryClient = useQueryClient();

  // --- Plain React state: backs the form inputs (controlled components).
  // Each <input>'s `value` comes FROM these variables, and `onChange` is
  // what updates them - the input never manages its own value internally,
  // React state is the single source of truth for what's on screen.
  const [scenarioName, setScenarioName] = useState("Equity market drops 20 percent");
  const [equityShock, setEquityShock] = useState("-0.20");
  const [bondShock, setBondShock] = useState("-0.05");

  // Not tied to any input - just remembers "the last preview result",
  // purely so it can be displayed after clicking Preview. Starts as null,
  // gets filled in by previewMutation's onSuccess below.
  const [lastPreview, setLastPreview] = useState<StressScenarioResponse | null>(null);

  // --- React Query state: for network requests. Runs automatically
  // (fetches the saved runs list as soon as bookId is available).
  const scenarioRunsQuery = useQuery({
    queryKey: ["scenario-runs", bookId],
    queryFn: () => getScenarioRuns(bookId!),
    enabled: Boolean(bookId),
  });

  // useMutation is like useQuery, but it does NOT run automatically - it
  // only fires when you call .mutate() yourself (see handlePreview below).
  // That's the right tool here: this is a POST triggered by a button
  // click, not data you want loaded the moment the page opens.
  // isPending/error/data are tracked internally by react-query - notice
  // there's no useState written for "is this loading" anywhere here.
  const previewMutation = useMutation({
    mutationFn: () =>
      runStressScenario(bookId!, {
        scenario_name: scenarioName,
        asset_type_shocks: {
          equity: equityShock,
          bond: bondShock,
        },
      }),
    // Runs after a successful response - stores the result so it can render below.
    onSuccess: (data) => {
      setLastPreview(data);
    },
  });

  // Same idea, but calls the "stress-runs" endpoint that actually saves
  // the result in the database (rather than just computing a preview).
  const persistMutation = useMutation({
    mutationFn: () =>
      runAndPersistStressScenario(bookId!, {
        scenario_name: scenarioName,
        asset_type_shocks: {
          equity: equityShock,
          bond: bondShock,
        },
      }),
    onSuccess: async () => {
      // Tell react-query "the scenario-runs list is now stale" - this
      // triggers scenarioRunsQuery to automatically re-fetch, so the new
      // row shows up in the table below without any manual state update.
      await queryClient.invalidateQueries({
        queryKey: ["scenario-runs", bookId],
      });
    },
  });

  // Handles the <form>'s submit event (fired by the "Preview scenario"
  // button, since it's type="submit" inside the form).
  function handlePreview(event: SubmitEvent) {
    // Stops the browser's default behavior for form submission, which is
    // to reload the page (there's no `action` attribute, so it would
    // otherwise navigate to the same URL and lose all component state).
    event.preventDefault();
    previewMutation.mutate();
  }

  // Handles the "Run and save" button directly (it's type="button", not
  // "submit", so it does NOT go through the form's onSubmit at all).
  function handlePersist() {
    persistMutation.mutate();
  }

  return (
    <section>
      <h2>Scenario Analysis</h2>
      <p className="muted">Book ID: {bookId}</p>

      <form className="form-card" onSubmit={handlePreview}>
        <label>
          Scenario name
          <input
            value={scenarioName}
            onChange={(event) => setScenarioName(event.target.value)}
          />
        </label>

        <label>
          Equity shock
          <input
            value={equityShock}
            onChange={(event) => setEquityShock(event.target.value)}
          />
        </label>

        <label>
          Bond shock
          <input
            value={bondShock}
            onChange={(event) => setBondShock(event.target.value)}
          />
        </label>

        <div className="button-row">
          {/* type="submit" -> clicking this triggers the <form>'s onSubmit (handlePreview). */}
          <button type="submit" disabled={previewMutation.isPending}>
            Preview scenario
          </button>

          {/* type="button" -> does NOT submit the form; onClick calls handlePersist directly. */}
          <button
            type="button"
            disabled={persistMutation.isPending}
            onClick={handlePersist}
          >
            Run and save
          </button>
        </div>
      </form>

      {/* Only shows up if the preview request actually failed. */}
      {previewMutation.error && (
        <ErrorState message={(previewMutation.error as Error).message} />
      )}

      {/* Only shows up once a successful preview has been run at least once. */}
      {lastPreview && (
        <div className="table-card">
          <h3>Preview result</h3>
          <p>Base LTV: {lastPreview.base_weighted_ltv}</p>
          <p>Base status: {lastPreview.base_risk_status}</p>
          <p>Stressed LTV: {lastPreview.stressed_weighted_ltv}</p>
          <p>Stressed status: {lastPreview.stressed_risk_status}</p>
        </div>
      )}

      <h3>Saved scenario runs</h3>

      {/* This is scenarioRunsQuery's state, unrelated to the mutations above. */}
      {scenarioRunsQuery.isLoading && <LoadingState />}
      {scenarioRunsQuery.error && (
        <ErrorState message={(scenarioRunsQuery.error as Error).message} />
      )}

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Created</th>
              <th>Name</th>
              <th>Base status</th>
              <th>Stressed status</th>
              <th>Base LTV</th>
              <th>Stressed LTV</th>
            </tr>
          </thead>
          <tbody>
            {/* "?." (optional chaining) - scenarioRunsQuery.data is undefined
                until the fetch resolves, so ".map" would crash on undefined
                without it. `?.map` just does nothing (renders nothing) in
                that case, instead of throwing. */}
            {scenarioRunsQuery.data?.map((run) => (
              <tr key={run.id}>
                <td>{new Date(run.created_at).toLocaleString()}</td>
                <td>{run.scenario_name}</td>
                <td>{run.base_risk_status}</td>
                <td>{run.stressed_risk_status}</td>
                <td>{run.base_weighted_ltv}</td>
                <td>{run.stressed_weighted_ltv}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
