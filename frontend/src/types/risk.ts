export type BookRiskSummary = {
  book_id: string;
  book_name: string;
  currency: string;
  loan_count: number;
  position_count: number;
  pending_trade_order_count: number;
  executed_trade_order_count: number;
  total_loan_exposure: string;
  total_collateral_market_value: string;
  total_eligible_collateral_value: string;
  weighted_ltv: string | null;
  total_position_market_value: string;
  risk_status: string;
};