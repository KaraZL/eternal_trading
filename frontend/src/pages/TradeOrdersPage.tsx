import { useQuery } from "@tanstack/react-query";

import { getTradeOrders } from "../api/tradeOrders";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";

export function TradeOrdersPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["trade-orders"],
    queryFn: getTradeOrders,
  });

  if (isLoading) return <LoadingState />;
  if (error) return <ErrorState message={(error as Error).message} />;

  return (
    <section>
      <h2>Trade Orders</h2>

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Side</th>
              <th>Asset</th>
              <th>Quantity</th>
              <th>Limit price</th>
              <th>Status</th>
              <th>Execution price</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((order) => (
              <tr key={order.id}>
                <td>{order.side}</td>
                <td>{order.asset_name}</td>
                <td>{order.quantity}</td>
                <td>{order.limit_price}</td>
                <td>{order.status}</td>
                <td>{order.execution_price ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}