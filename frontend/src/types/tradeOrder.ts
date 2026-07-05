export type TradeOrder = {
  id: string;
  book_id: string;
  side: string;
  asset_type: string;
  asset_name: string;
  quantity: string;
  limit_price: string;
  currency: string;
  status: string;
  execution_price: string | null;
  executed_at: string | null;
};