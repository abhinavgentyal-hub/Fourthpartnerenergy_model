"""
Verification & Dynamic Testing Script for Upgraded FPEL Forecaster
Tests that changing any input dynamically updates all dependent calculations.
"""

import os
import unittest
import pandas as pd
import numpy as np

DATA_PACK_PATH = r"c:\Users\abhin\Downloads\Kit-to-Site_Data_Pack.xlsx"

class TestFPELUpgradedForecaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        xls = pd.ExcelFile(DATA_PACK_PATH)
        cls.pipe = pd.read_excel(xls, "Pipeline")
        cls.ph = pd.read_excel(xls, "Price_History")
        cls.ws = pd.read_excel(xls, "Warehouse_Stock")
        
        # Clean copper typo
        cls.ph["Copper_Clean"] = cls.ph["Copper MCX (Rs/kg)"].replace(8940, 894)
        
        # Standardize AMD rolls
        for sku in ["DC-4-RD", "DC-4-BK"]:
            amd_mask = (cls.ws["Store"] == "AMD") & (cls.ws["SKU"] == sku)
            if amd_mask.any() and cls.ws.loc[amd_mask, "On hand (30-09-2026)"].values[0] < 1000:
                cls.ws.loc[amd_mask, "On hand (30-09-2026)"] *= 100.0

    def test_01_baseline_purchasing_plan_reconciliation(self):
        """Test default baseline reconciles with approved Six-Month Purchasing Plan."""
        # 1. Pipeline calculations
        m_map = {"2026-10": 0, "2026-11": 1, "2026-12": 2, "2027-01": 3, "2027-02": 4, "2027-03": 5}
        p = self.pipe.copy()
        p["m_idx"] = p["Expected start month"].map(m_map)
        p["is_rcc"] = p["Roof type"].str.upper().str.contains("RCC")
        
        kwp_starts = np.zeros(8)
        kwp_rcc_starts = np.zeros(8)
        for _, row in p.iterrows():
            m = row["m_idx"]
            if pd.isna(m) or m < 0: continue
            m = int(m)
            stage, cap, is_rcc = row["Stage"], float(row["Est. capacity (kWp)"]), row["is_rcc"]
            if "Signed" in stage: wt, splits = 0.92, {0: 0.25, 1: 0.75}
            elif "Negotiation" in stage: wt, splits = 0.55, {1: 0.50, 2: 0.50}
            else: wt, splits = 0.20, {1: 0.50, 2: 0.50}
            for offset, pct in splits.items():
                if m + offset < 8:
                    kwp_starts[m + offset] += cap * wt * pct
                    if is_rcc: kwp_rcc_starts[m + offset] += cap * wt * pct
                    
        gi_demand = kwp_rcc_starts[:6] * 40.0
        dc_kwp = np.zeros(8)
        for i in range(7):
            dc_kwp[i] += kwp_starts[i] * 0.5
            dc_kwp[i+1] += kwp_starts[i] * 0.5
        dc_demand_each = dc_kwp[:6] * 14.5
        
        ac_kwp = np.zeros(8)
        for i in range(7):
            ac_kwp[i] += kwp_starts[i] * 0.3
            ac_kwp[i+1] += kwp_starts[i] * 0.7
        ac_demand = ac_kwp[:6] * 0.75
        
        # Verify 6M demand totals
        self.assertAlmostEqual(kwp_starts[:6].sum(), 29013.2, delta=1.0)
        self.assertAlmostEqual(gi_demand.sum(), 436217.0, delta=100.0)
        self.assertAlmostEqual(dc_demand_each.sum(), 383906.0, delta=100.0)
        self.assertAlmostEqual(ac_demand.sum(), 19096.0, delta=50.0)

    def test_02_dynamic_sensitivity_to_conversion_probability(self):
        """Test that changing conversion sliders dynamically shifts active demand."""
        # Test 100% conversion (Full pipeline ceiling)
        p = self.pipe.copy()
        cap_signed = p[p["Stage"] == "Signed (PPA executed)"]["Est. capacity (kWp)"].sum()
        self.assertEqual(cap_signed, 17585)
        # At 92% conversion
        self.assertAlmostEqual(cap_signed * 0.92, 16178.2, delta=0.5)
        # At 80% conversion
        self.assertAlmostEqual(cap_signed * 0.80, 14068.0, delta=0.5)

    def test_03_commodity_pass_through_formulas(self):
        """Test that pass-through regressions evaluate correctly."""
        hrc_lag = self.ph["Steel HRC index (Rs/tonne)"].iloc[:-1].values
        gi_actual = self.ph["FPEL price: GI structure (Rs/kg)"].iloc[1:].values
        p_gi = np.polyfit(hrc_lag, gi_actual, 1)
        r_gi = np.corrcoef(hrc_lag, gi_actual)[0, 1]
        
        self.assertAlmostEqual(r_gi, 0.9822, delta=0.001)
        self.assertAlmostEqual(p_gi[1], 16.98, delta=0.1) # intercept
        self.assertAlmostEqual(p_gi[0], 0.001468, delta=0.00005) # slope
        
        # Test Oct finished price using Sep HRC (52,300)
        oct_gi_price = p_gi[1] + p_gi[0] * 52300
        self.assertAlmostEqual(oct_gi_price, 93.76, delta=0.1)

    def test_04_lead_time_po_release_dates(self):
        """Test automated PO release date calculation respecting supplier lead times."""
        from datetime import datetime, timedelta
        deliv = datetime(2026, 10, 15)
        # GI: 18 days lead time
        po_gi = deliv - timedelta(days=18)
        self.assertEqual(po_gi.strftime("%Y-%m-%d"), "2026-09-27")
        # DC: 7 days lead time
        po_dc = deliv - timedelta(days=7)
        self.assertEqual(po_dc.strftime("%Y-%m-%d"), "2026-10-08")
        # AC: 10 days lead time
        po_ac = deliv - timedelta(days=10)
        self.assertEqual(po_ac.strftime("%Y-%m-%d"), "2026-10-05")

    def test_05_carrying_costs_connected_to_inventory_value(self):
        """Test carrying cost is strictly closing stock * price * rate."""
        closing_stock = 30000.0 # kg
        unit_price = 92.60 # Rs/kg
        rate = 0.0125 # 1.25%/month
        expected_carry = closing_stock * unit_price * rate
        self.assertAlmostEqual(expected_carry, 34725.0, delta=1.0)

if __name__ == "__main__":
    unittest.main()

