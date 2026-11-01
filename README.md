# Fourth Partner Energy (FPEL) - Material Buy-or-Hold Forecaster

Production Decision-Support Forecaster & Inventory Optimization Engine developed for **Fourth Partner Energy Limited (FPEL)** Kit-to-Site Operations.

Grounded strictly in `Kit-to-Site_Data_Pack.xlsx` and `Kit-to-Site_Case_Brief.pdf`.

---

## Overview

The FPEL Material Buy-or-Hold Forecaster models monthly procurement requirements, dynamic pipeline conversions, econometric commodity pass-through pricing, and store inventory levels across the 6-month planning horizon (**October 2026 – March 2027**).

### Core Capabilities

1. **Strategic Action Directives & Decision Cards:**
   - **Fabricated GI Structure (STR-RCC-GI):** Q4 Rate Lock (@ Rs 92.60/kg) for 170 tonnes. Direct fabricator dispatch to site.
   - **DC Solar Cable 4 sq mm (DC-4-RD / BK):** Hold bulk buy; execute 40km inter-warehouse stock rebalancing (Ahmedabad to Pune); rolling bi-weekly POs starting Dec 1.
   - **Aluminium AC Cable (AC-AL-150):** Hold bulk buy; consume 6,431m network stock (including TR-071 in-transit); release OEM cut-length POs starting Dec 1.

2. **Simulation Controls & Macro Shocks:**
   - 6 Instant Pre-configured Macro Scenarios (Base Case, Committed Downside, Zero-Slippage Nominal, Full Pipeline Upside, Bull Market, Bear Market).
   - Dynamic conversion sliders for Signed PPA (92%), Negotiation (55%), and Early Proposals (20%) with stage-duration slippage.
   - Commodity price shocks for Steel HRC, Copper MCX, and Aluminium MCX.
   - Operational toggles for carrying cost rate, Q4 rate lock, and DC cable rebalancing.

3. **Econometric Pass-Through Forecasting:**
   - GI Steel structure pricing modeled via 1-month lagged HRC regression ($r = 0.9822$).
   - DC cable pricing modeled via cleaned Copper MCX regression ($r = 0.9830$).
   - AC cable pricing modeled via Aluminium MCX regression ($r = 0.9906$).

4. **Forensic Data Audit & Exports:**
   - Detection and correction of March 2026 Copper MCX 10x entry typo (Rs 8,940 corrected to Rs 894/kg).
   - Harmonization of Ahmedabad DC cable stock from 100m rolls to linear metres.
   - Recognition of TR-071 (2,800m) in-transit stock arriving October 3.
   - Export to Excel Decision Workbook (`.xlsx`) and Executive Decision PDF Memo (`.pdf`).

---

## Deployment on Streamlit Community Cloud

This repository is ready to be hosted on **Streamlit Community Cloud (Streamlit Share)**:

1. Sign in to [share.streamlit.io](https://share.streamlit.io).
2. Click **New app**.
3. Select this repository: `abhinavgentyal-hub/Fourthpartnerenergy_model`.
4. Set branch: `main`.
5. Set main file path: `app.py`.
6. Click **Deploy**.

---

## Local Development

```bash
# Clone the repository
git clone https://github.com/abhinavgentyal-hub/Fourthpartnerenergy_model.git
cd Fourthpartnerenergy_model

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app.py
```

### Running Automated Unit Tests
```bash
python test_forecaster.py
```
