import argparse
import pandas as pd
from datetime import datetime

def freshness_factor(age_hours: float, shelf_life_hours: float) -> float:
    """
    Exponential perishability decay.
    f(age) = max(0, 1 - (age/SL)^1.5)
    Justified: This formula models rapid decay near expiration, common for perishables like tomatoes or milk,
    ensuring freshness_factor drops monotonically from 1 to 0.
    """
    if shelf_life_hours <= 0:
        return 0.0  # Avoid division by zero
    return max(0.0, 1.0 - (age_hours / shelf_life_hours) ** 1.5)

def suggest_price(sku, now, competitor_snapshot, unit_cost, margin_floor=1.1):
    """
    Recommend an optimal price balancing competitor prices and perishability.
    - sku: dict with sku_id, purchased_at, shelf_life_hours, etc.
    - now: current timestamp (datetime)
    - competitor_snapshot: list of competitor prices for this product
    - unit_cost: vendor’s cost per unit
    - margin_floor: minimum markup multiplier
    Returns: dict with chosen_price, freshness_factor, rationale
    """

    # Step 1: Compute product age
    purchased_at = sku["purchased_at"]
    shelf_life = sku["shelf_life_hours"]
    age_hours = (now - purchased_at).total_seconds() / 3600
    age_hours = max(0, age_hours)  # Ensure non-negative to avoid complex numbers

    # Step 2: Freshness factor
    f = freshness_factor(age_hours, shelf_life)

    # Step 3: Competitor reference price
    if competitor_snapshot:
        competitor_mean = sum(competitor_snapshot) / len(competitor_snapshot)
        competitor_min = min(competitor_snapshot)
    else:
        # Fallback: use unit cost with margin if no competitors
        competitor_mean = unit_cost * margin_floor
        competitor_min = unit_cost * margin_floor

    # Step 4: Demand-adjusted price
    # Interpolate between competitor_mean (when fresh) and competitor_min (when decayed)
    # This ensures price drops monotonically as f -> 0
    price = competitor_min + (competitor_mean - competitor_min) * f

    # Step 5: Enforce cost floor
    min_price = unit_cost * margin_floor
    price = max(price, min_price)

    return {
        "sku": sku["sku_id"],
        "chosen_price": round(price, 2),
        "freshness_factor": round(f, 3),
        "rationale": f"Competitor mean={competitor_mean:.2f}, min={competitor_min:.2f}, decay={f:.3f}"
    }

if __name__ == "__main__":
    import argparse
    import pandas as pd

    parser = argparse.ArgumentParser()
    parser.add_argument("--sku", type=int, required=True, help="SKU ID from stock.csv")
    parser.add_argument("--now", type=str, required=True, help="Current timestamp in ISO format")
    args = parser.parse_args()

    # Load stock data
    stock = pd.read_csv("data/stock.csv", parse_dates=["purchased_at"])
    sku_row = stock.loc[stock["sku_id"] == args.sku].iloc[0]

    # Load competitor prices for this product at the given time
    competitor_prices = pd.read_csv("data/competitor_prices.csv", parse_dates=["timestamp"])
    comp_snapshot = competitor_prices.loc[
        (competitor_prices["timestamp"] == pd.to_datetime(args.now)) &
        (competitor_prices["product"] == sku_row["product"])
    ]["price"].tolist()

    # Run pricer
    result = suggest_price(
        sku_row.to_dict(),
        pd.to_datetime(args.now),
        comp_snapshot,
        sku_row["unit_cost_xaf"]
    )

    print(result)