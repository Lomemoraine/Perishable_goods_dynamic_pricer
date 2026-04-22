# Perishable Goods Dynamic Pricer

## Overview
This project implements a dynamic pricing engine for perishable goods in open-air markets.  
It simulates vendor inventory, competitor pricing, and perishability decay to recommend optimal prices that balance profitability, competitiveness, and waste reduction.

Deliverables:
- `generator.py` → Synthetic dataset generator (stock, competitor prices, sales history).
- `pricer.py` → Dynamic pricer with exponential freshness decay.
- `simulation.ipynb` → 7-day simulation comparing pricer vs. baselines.
- `sms_pricesheet.md` → SMS artifact for low-tech vendor communication.
- `process_log.md` → Hour-by-hour implementation log.
- `SIGNED.md` → Honor code declaration.

---

## Workflow
1. **Data Generation (`generator.py`)**
   - Produces:
     - `stock.csv`: 120 SKUs with purchase times, costs, shelf life, suppliers.
     - `competitor_prices.csv`: 48 hours of competitor prices across 12 stalls, 30-min granularity.
     - `sales_history.csv`: Historical sales for demand curve calibration.

2. **Dynamic Pricer (`pricer.py`)**
   - Uses exponential decay formula:
     

\[
     f(age) = \max(0, 1 - (age/SL)^{1.5})
     \]


   - Blends competitor mean and competitor min prices based on freshness factor.
   - Enforces cost × margin floor.

3. **Simulation (`simulation.ipynb`)**
   - Runs 7-day simulation at 30-min intervals.
   - Compares:
     - Dynamic pricer
     - Cost-plus baseline
     - Cheapest competitor baseline
   - Outputs charts for profit, waste, and margin.

4. **SMS Price Sheet (`sms_pricesheet.md`)**
   - 160-character daily SMS templates.
   - Fallback strategies for illiterate vendors (voice calls, picture sheets, agent relay).
   - Unit economics table.

---

## How to Run
1. **Generate Data**
   ```bash
   python generator.py
2. **Test the Pricer on CLI**
   ```bash
   ``python pricer.py --sku 5 --now 2026-04-20T15:30``
3. **Open the simulation notebook and run all the cells**