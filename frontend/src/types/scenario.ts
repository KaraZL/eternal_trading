export type StressScenarioRequest = {
  scenario_name: string;
  asset_type_shocks: Record<string, string>;
};

export type StressScenarioResponse = {
  book_id: string;
  scenario_name: string;

  base_total_loan_exposure: string;
  base_total_collateral_market_value: string;
  base_total_eligible_collateral_value: string;
  base_weighted_ltv: string | null;
  base_risk_status: string;

  stressed_total_collateral_market_value: string;
  stressed_total_eligible_collateral_value: string;
  stressed_weighted_ltv: string | null;
  stressed_risk_status: string;

  base_total_position_market_value: string;
  stressed_total_position_market_value: string;
};

export type ScenarioRun = {
  id: string;
  book_id: string;
  scenario_name: string;
  asset_type_shocks: Record<string, string>;
  created_at: string;

  base_total_loan_exposure: string;
  base_total_collateral_market_value: string;
  base_total_eligible_collateral_value: string;
  base_weighted_ltv: string | null;
  base_risk_status: string;

  stressed_total_collateral_market_value: string;
  stressed_total_eligible_collateral_value: string;
  stressed_weighted_ltv: string | null;
  stressed_risk_status: string;

  base_total_position_market_value: string;
  stressed_total_position_market_value: string;
};