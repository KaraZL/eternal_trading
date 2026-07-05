import { apiGet } from './client';
import type { TradeOrder } from '../types/tradeOrder';

export function getTradeOrders(): Promise<TradeOrder[]> {
    return apiGet<TradeOrder[]>("/api/trade-orders")
}