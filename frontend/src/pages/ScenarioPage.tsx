import { FormEvent, useState } from "react";
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

  const [scenarioName, setScenarioName] = useState("Equity market drops 20 percent");
  const [equityShock, setEquityShock] = useState("-0.20");
  const [bondShock, setBondShock] = useState("-0.05");
  const [lastPreview, setLastPreview] = useState<StressScenarioResponse | null>(null);

  const scenarioRunsQuery = useQuery({
    queryKey: ["scenario-runs", bookId],
    queryFn: () => getScenarioRuns(bookId!),
    enabled: Boolean(bookId),
  });

  const previewMutation = useMutation({
    mutationFn: () =>
      runStressScenario(bookId!, {
        scenario_name: scenarioName,
        asset_type_shocks: {
          equity: equityShock,
          bond: bondShock,
        },
      }),
    onSuccess: (data) => {
      setLastPreview(data);
    },
  });

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
      await queryClient.invalidateQueries({
        queryKey: ["scenario-runs", bookId],
      });
    },
  });

  function handlePreview(event: FormEvent) {
    event.preventDefault();
    previewMutation.mutate();
  }

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
          <button type="submit" disabled={previewMutation.isPending}>
            Preview scenario
          </button>

          <button
            type="button"
            disabled={persistMutation.isPending}
            onClick={handlePersist}
          >
            Run and save
          </button>
        </div>
      </form>

      {previewMutation.error && (
        <ErrorState message={(previewMutation.error as Error).message} />
      )}

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