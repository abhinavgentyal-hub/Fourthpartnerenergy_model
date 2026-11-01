"""
FPEL MATERIAL BUY-OR-HOLD FORECASTER
Fourth Partner Energy Limited (FPEL) — Kit-to-Site Operations Advisory
Production Enterprise Decision-Support Application (FPEL Dark Corporate Edition)
Grounded strictly in Kit-to-Site_Data_Pack.xlsx and Kit-to-Site_Case_Brief.pdf
"""

import os
import io
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & FPEL DARK ENTERPRISE THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FPEL Material Buy-or-Hold Forecaster",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fourth Partner Energy Dark Corporate Palette
DARK_CANVAS = "#070C18"       # Deep Obsidian Canvas
DARK_SURFACE = "#0F172A"      # Slate Obsidian Card Surface
DARK_ELEVATED = "#131E35"     # Elevated Slate Metric Surface
ACCENT_CYAN = "#38BDF8"       # FPEL Solar Electric Cyan/Sky Blue
ACCENT_BLUE = "#0284C7"       # FPEL Corporate Blue
ACCENT_GOLD = "#F59E0B"       # FPEL Solar Sunburst Gold
ACCENT_COPPER = "#FB923C"     # Dynamic Copper Rust / Amber Orange
ACCENT_COLOR = "#F59E0B"      # Solar Amber Accent
INFO_COLOR = "#38BDF8"        # FPEL Electric Cyan
SUCCESS_COLOR = "#10B981"     # Clean-Tech Emerald Green
TEXT_WHITE = "#FFFFFF"        # Pure High-Contrast White
TEXT_LIGHT = "#F8FAFC"        # Primary Text
TEXT_MUTED = "#94A3B8"        # Secondary Text
BORDER_SUBTLE = "rgba(255, 255, 255, 0.08)" # Hairline Dark Border

# -----------------------------------------------------------------------------
# HIGH-END DARK DESIGN SYSTEM (FPEL BRAND ALIGNMENT & SOLAR MESH)
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Completely hide sidebar and collapse chevron */
    section[data-testid="stSidebar"], [data-testid="collapsedControl"] {{
        display: none !important;
    }}
    
    /* Completely hide Streamlit Share top header bar, toolbar, decoration line, and footer */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    .stApp > header,
    div[data-testid="stDecoration"],
    div[data-testid="stToolbar"],
    div[data-testid="stToolbarActions"],
    div[data-testid="stStatusWidget"],
    div[data-testid="stAppDeployButton"],
    div[data-testid="stMainMenu"],
    #MainMenu,
    footer,
    .viewerBadge_container__r5tak,
    .viewerBadge_link__1S137,
    [data-testid="manage-app-button"],
    #manage-app-button,
    button[data-testid="manage-app-button"],
    div[class*="manageApp"],
    button[class*="manageApp"],
    a[class*="manageApp"],
    div[class*="viewerBadge"],
    a[class*="viewerBadge"],
    div[class*="FloatingContainer"],
    div[style*="position: fixed"][style*="bottom:"],
    div[style*="position:fixed"][style*="bottom:"],
    button[style*="position: fixed"][style*="bottom:"],
    button[style*="position:fixed"][style*="bottom:"],
    a[style*="position: fixed"][style*="bottom:"],
    a[style*="position:fixed"][style*="bottom:"],
    iframe[title*="manage-app"],
    iframe[title*="Manage app"] {{
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        width: 0px !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transform: scale(0) !important;
        position: absolute !important;
        bottom: -9999px !important;
        right: -9999px !important;
        z-index: -9999 !important;
    }}
    
    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: {TEXT_LIGHT};
        background-color: {DARK_CANVAS} !important;
        background-image: 
            radial-gradient(circle at 10% 8%, rgba(2, 132, 199, 0.18) 0%, transparent 45%),
            radial-gradient(circle at 90% 12%, rgba(245, 158, 11, 0.16) 0%, transparent 42%),
            radial-gradient(circle at 50% 92%, rgba(16, 185, 129, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 82% 78%, rgba(56, 189, 248, 0.10) 0%, transparent 45%) !important;
        background-attachment: fixed !important;
        -webkit-font-smoothing: antialiased;
    }}
    
    /* Layout Spacing & Margins */
    .block-container {{
        padding-top: 1.25rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1440px;
    }}
    
    /* Smooth Transitions & Animations */
    * {{
        transition: background-color 0.22s cubic-bezier(0.16, 1, 0.3, 1), 
                    border-color 0.22s cubic-bezier(0.16, 1, 0.3, 1), 
                    box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1), 
                    transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes pulseGlow {{
        0%, 100% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.35); opacity: 0.65; }}
    }}
    
    .stTabs [data-baseweb="tab-panel"] {{
        animation: fadeIn 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        padding-top: 16px;
    }}
    
    /* FPEL Corporate Masthead Banner with Ambient Solar Glow */
    .fpel-masthead {{
        background: linear-gradient(135deg, #070D1E 0%, #0F172A 55%, #131E35 100%);
        border: 1px solid rgba(56, 189, 248, 0.22);
        border-radius: 16px;
        padding: 22px 30px;
        margin-bottom: 18px;
        box-shadow: 0 12px 36px -4px rgba(0, 0, 0, 0.65);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 18px;
        position: relative;
        overflow: hidden;
    }}
    
    .fpel-masthead::after {{
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 260px;
        height: 260px;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.22) 0%, rgba(2, 132, 199, 0.16) 45%, transparent 75%);
        pointer-events: none;
    }}
    
    .fpel-brand-wrap {{
        display: flex;
        align-items: center;
        gap: 18px;
        z-index: 1;
    }}
    
    .fpel-logo-svg {{
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.08);
        padding: 12px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }}
    
    .fpel-title-box h1 {{
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase;
    }}
    
    .fpel-title-box p {{
        color: #94A3B8 !important;
        font-size: 13px !important;
        margin: 4px 0 0 0 !important;
        font-weight: 500;
        letter-spacing: 0.2px;
    }}
    
    .fpel-meta-badges {{
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
        z-index: 1;
    }}
    
    .fpel-sun-badge {{
        display: flex;
        align-items: center;
        background: rgba(245, 158, 11, 0.14);
        color: #FDE68A;
        border: 1px solid rgba(245, 158, 11, 0.35);
        padding: 8px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        gap: 8px;
    }}
    
    .fpel-sun-dot {{
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #10B981;
        animation: pulseGlow 2s infinite ease-in-out;
    }}
    
    .fpel-pill-button {{
        background: linear-gradient(135deg, {ACCENT_BLUE} 0%, #0369A1 100%);
        color: #FFFFFF !important;
        font-size: 12px;
        font-weight: 600;
        padding: 8px 16px;
        border-radius: 9999px;
        letter-spacing: 0.3px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
    }}
    
    /* Sleek Top Quick Scenario Ribbon Bar */
    .top-ribbon-bar {{
        background: {DARK_SURFACE};
        border: 1px solid {BORDER_SUBTLE};
        border-radius: 14px;
        padding: 14px 20px;
        margin-bottom: 22px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }}
    
    .ribbon-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        background: #1E293B;
        color: #CBD5E1;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    
    .ribbon-pill.active {{
        background: rgba(2, 132, 199, 0.22);
        color: #38BDF8;
        border-color: rgba(56, 189, 248, 0.45);
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.15);
    }}
    
    /* Refined Streamlit Tabs */
    button[data-baseweb="tab"], [data-testid="stTab"] {{
        background: {DARK_SURFACE} !important;
        border: 1px solid {BORDER_SUBTLE} !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        color: {TEXT_MUTED} !important;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    }}
    
    button[data-baseweb="tab"]:hover, [data-testid="stTab"]:hover {{
        background: #1E293B !important;
        color: {TEXT_WHITE} !important;
        border-color: rgba(56, 189, 248, 0.35) !important;
        transform: translateY(-1px) !important;
    }}
    
    button[data-baseweb="tab"][aria-selected="true"], [data-testid="stTab"][aria-selected="true"] {{
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: {TEXT_WHITE} !important;
        border-color: #38BDF8 !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4) !important;
    }}
    
    /* Metric Cards with Colored Top-Border Accents */
    div[data-testid="stMetric"] {{
        background: linear-gradient(180deg, {DARK_ELEVATED} 0%, {DARK_SURFACE} 100%) !important;
        border: 1px solid {BORDER_SUBTLE} !important;
        border-radius: 14px !important;
        padding: 18px 20px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 24px -4px rgba(0, 0, 0, 0.45) !important;
        border-color: rgba(56, 189, 248, 0.3) !important;
    }}
    
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] {{ border-top: 3px solid #38BDF8 !important; }}
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] {{ border-top: 3px solid {ACCENT_GOLD} !important; }}
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] {{ border-top: 3px solid #94A3B8 !important; }}
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetric"] {{ border-top: 3px solid {ACCENT_COPPER} !important; }}
    div[data-testid="column"]:nth-of-type(5) div[data-testid="stMetric"] {{ border-top: 3px solid {SUCCESS_COLOR} !important; }}
    
    div[data-testid="stMetricLabel"] {{
        font-size: 11.5px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        color: {TEXT_MUTED} !important;
        margin-bottom: 4px !important;
    }}
    
    div[data-testid="stMetricValue"] {{
        font-size: 19px !important;
        font-weight: 800 !important;
        color: {TEXT_WHITE} !important;
        letter-spacing: -0.3px !important;
        white-space: nowrap !important;
    }}
    
    /* Decision Pills */
    .pill-buy {{
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.45);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }}
    
    .pill-transfer {{
        display: inline-flex;
        align-items: center;
        background: rgba(2, 132, 199, 0.2);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.45);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }}
    
    .pill-hold {{
        display: inline-flex;
        align-items: center;
        background: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.45);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }}
    
    /* Themed Parameter Subcards (Dark Mode Luminous) */
    .subcard-gi {{
        background: rgba(2, 132, 199, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 10px;
        padding: 14px 16px;
        margin: 12px 0;
        font-size: 12px;
        line-height: 1.65;
        color: #BAE6FD;
    }}
    
    .subcard-dc {{
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.28);
        border-radius: 10px;
        padding: 14px 16px;
        margin: 12px 0;
        font-size: 12px;
        line-height: 1.65;
        color: #FDE68A;
    }}
    
    .subcard-ac {{
        background: rgba(251, 146, 60, 0.12);
        border: 1px solid rgba(251, 146, 60, 0.28);
        border-radius: 10px;
        padding: 14px 16px;
        margin: 12px 0;
        font-size: 12px;
        line-height: 1.65;
        color: #FED7AA;
    }}
    
    /* Generous padding inside all Streamlit bordered containers to eliminate abrupt cutoffs */
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlock"]:has(.decision-card-body),
    div[data-testid="stVerticalBlock"]:has([data-testid="stSlider"]) {{
        border-radius: 16px !important;
        border: 1px solid {BORDER_SUBTLE} !important;
        background: {DARK_SURFACE} !important;
        box-shadow: 0 4px 24px -2px rgba(0, 0, 0, 0.4) !important;
        overflow: visible !important;
        padding: 24px 26px 36px 26px !important;
        margin-bottom: 24px !important;
    }}
    
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        padding: 24px 26px 36px 26px !important;
    }}
    
    .decision-card-body {{
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 520px;
        padding-bottom: 18px;
        margin-bottom: 6px;
    }}
    
    .reversal-callout {{
        margin-top: 20px;
        margin-bottom: 8px;
        padding: 12px 16px;
        background: rgba(239, 68, 68, 0.12);
        border-left: 4px solid #EF4444;
        border-radius: 8px;
        font-size: 11.5px;
        color: #FCA5A5;
        line-height: 1.55;
    }}
    
    /* Section Headings Spacing */
    h3, h4 {{
        color: {TEXT_WHITE} !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
        margin-top: 22px !important;
        margin-bottom: 12px !important;
    }}
    
    /* Scrollbars */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #334155;
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: #475569;
    }}
</style>
""", unsafe_allow_html=True)

# Client-side removal of floating badges and host toolbars
components.html("""
<script>
function purgeHostBadges() {
    try {
        const contexts = [document, window.parent ? window.parent.document : null];
        contexts.forEach(ctx => {
            if (!ctx) return;
            const selectors = [
                '[data-testid="manage-app-button"]',
                '#manage-app-button',
                '.viewerBadge_container__r5tak',
                '.viewerBadge_link__1S137',
                '[class*="viewerBadge"]',
                '[class*="manageApp"]',
                '[class*="manage-app"]',
                '[class*="ManageApp"]',
                'div[data-testid="stStatusWidget"]'
            ];
            selectors.forEach(sel => {
                const nodes = ctx.querySelectorAll(sel);
                nodes.forEach(n => {
                    n.style.display = 'none';
                    n.style.visibility = 'hidden';
                    try { n.remove(); } catch(e) {}
                });
            });
        });
    } catch(e) {}
}
setInterval(purgeHostBadges, 300);
document.addEventListener("DOMContentLoaded", purgeHostBadges);
</script>
""", height=0, width=0)

def format_minimal_chart(fig, title, yaxis_title=""):
    """Format Plotly charts with the FPEL high-contrast dark minimal aesthetic."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Inter, -apple-system, sans-serif", size=13, color="#F8FAFC", weight=700)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=25, t=48, b=40),
        font=dict(family="Inter, -apple-system, sans-serif", size=11, color="#94A3B8"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(15, 23, 42, 0.85)",
            font=dict(color="#CBD5E1")
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="#334155",
            tickfont=dict(size=11, color="#94A3B8")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.06)",
            linecolor="#334155",
            title=dict(text=yaxis_title, font=dict(size=11, color="#94A3B8")),
            tickfont=dict(size=11, color="#94A3B8")
        ),
        hovermode="x unified"
    )
    return fig

# -----------------------------------------------------------------------------
# PRODUCTION DATA RESOLUTION & INGESTION
# -----------------------------------------------------------------------------
APP_ROOT = Path(__file__).parent
DATA_DIR = APP_ROOT / "data"

def resolve_data_pack_source(uploaded_file=None):
    """Resolve data source path with production fallbacks."""
    if uploaded_file is not None:
        return uploaded_file
    bundled = DATA_DIR / "Kit-to-Site_Data_Pack.xlsx"
    if bundled.exists():
        return str(bundled)
    local_download = Path(r"c:\Users\abhin\Downloads\Kit-to-Site_Data_Pack.xlsx")
    if local_download.exists():
        return str(local_download)
    secondary = Path(r"F:\New download\Kit-to-Site_Data_Pack.xlsx")
    if secondary.exists():
        return str(secondary)
    return None

@st.cache_data
def load_and_audit_data_pack(file_source):
    if file_source is None:
        return None
    try:
        xls = pd.ExcelFile(file_source)
        sheets = {sheet: pd.read_excel(xls, sheet) for sheet in xls.sheet_names}
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return None
    
    audit_log = []
    
    # 1. Clean March 2026 Copper MCX typo (8,940 -> 894)
    if "Price_History" in sheets:
        ph = sheets["Price_History"].copy()
        ph["Copper_Raw"] = ph["Copper MCX (Rs/kg)"]
        mar_mask = ph["Month"] == "Mar-2026"
        if mar_mask.any() and ph.loc[mar_mask, "Copper MCX (Rs/kg)"].values[0] > 5000:
            raw_cu = ph.loc[mar_mask, "Copper MCX (Rs/kg)"].values[0]
            corrected_cu = raw_cu / 10.0
            ph.loc[mar_mask, "Copper MCX (Rs/kg)"] = corrected_cu
            audit_log.append({
                "Category": "Commodity Forensics",
                "Item": "March 2026 Copper MCX",
                "Raw Value": f"₹{raw_cu:,.0f}/kg",
                "Corrected Value": f"₹{corrected_cu:,.0f}/kg",
                "Diagnosis": "10x decimal entry typo in Price_History row 7",
                "Resolution": "Corrected to ₹894.0/kg. Cleaned 12M mean is ₹889.9/kg. Sep (₹908) is +2.0% above yearly average."
            })
        sheets["Price_History_Cleaned"] = ph
        
    # 2. Standardize AMD rolls to metres in Warehouse_Stock
    if "Warehouse_Stock" in sheets:
        ws = sheets["Warehouse_Stock"].copy()
        for sku in ["DC-4-RD", "DC-4-BK"]:
            amd_mask = (ws["Store"] == "AMD") & (ws["SKU"] == sku)
            if amd_mask.any() and ws.loc[amd_mask, "On hand (30-09-2026)"].values[0] < 1000:
                raw_qty = ws.loc[amd_mask, "On hand (30-09-2026)"].values[0]
                std_qty = raw_qty * 100.0 # 1 roll = 100 metres
                ws.loc[amd_mask, "On hand (30-09-2026)"] = std_qty
                ws.loc[amd_mask, "UoM"] = "Metre"
                audit_log.append({
                    "Category": "UoM Harmonization",
                    "Item": f"{sku} (AMD)",
                    "Raw Value": f"{raw_qty:.0f} rolls",
                    "Corrected Value": f"{std_qty:,.0f} m",
                    "Diagnosis": "Unit of Measure mismatch: recorded as 100m rolls instead of linear metres",
                    "Resolution": f"Converted {raw_qty:.0f} rolls × 100m = {std_qty:,.0f}m to align with Pune store."
                })
                
        # 3. TR-071 In-Transit Cable Attribution
        tr071_mask = (ws["Store"] == "PUN") & (ws["SKU"] == "AC-AL-150")
        ws["In_Transit"] = 0.0
        if tr071_mask.any():
            ws.loc[tr071_mask, "In_Transit"] = 2800.0
            audit_log.append({
                "Category": "In-Transit Recognition",
                "Item": "TR-071 (AC Cable)",
                "Raw Value": "Not counted on floor",
                "Corrected Value": "2,800 m Usable",
                "Diagnosis": "Dispatched 26-Sep from OEM, arriving 03-Oct Pune",
                "Resolution": "Credited to opening Pune usable stock; raises Pune AC stock to 6,431m (covers Oct demand)."
            })
            
        # 4. Dead stock & Legacy SKU flags
        amd_perc = (ws["Store"] == "AMD") & (ws["SKU"] == "MOD-540-PERC")
        if amd_perc.any():
            perc_qty = ws.loc[amd_perc, "On hand (30-09-2026)"].values[0]
            audit_log.append({
                "Category": "Dead Stock Flag",
                "Item": "MOD-540-PERC (AMD)",
                "Raw Value": f"{perc_qty:.0f} nos",
                "Corrected Value": "Liquidate / Write-down",
                "Diagnosis": "Discontinued 540 Wp mono PERC modules taking 38.4 m² floor",
                "Resolution": "Excluded from active 580 Wp TOPCon project BOM allocations."
            })
            
        pun_mc4 = (ws["Store"] == "PUN") & (ws["SKU"] == "CON-MC4-PAIR")
        if pun_mc4.any():
            mc4_qty = ws.loc[pun_mc4, "On hand (30-09-2026)"].values[0]
            audit_log.append({
                "Category": "Legacy SKU Flag",
                "Item": "CON-MC4-PAIR (PUN)",
                "Raw Value": f"{mc4_qty:.0f} pairs",
                "Corrected Value": "Re-code to MC4-CONN-PR",
                "Diagnosis": "Legacy SKU holding stock while standard SKU suffered stockouts",
                "Resolution": "Re-code for immediate consumption in Pune store."
            })
            
        ws["Total_Usable"] = ws["On hand (30-09-2026)"] + ws["In_Transit"]
        sheets["Warehouse_Stock_Cleaned"] = ws
        
    sheets["Audit_Log"] = pd.DataFrame(audit_log)
    return sheets

# -----------------------------------------------------------------------------
# SESSION STATE & SCENARIO MANAGEMENT (TAB & TOP-RIBBON DRIVEN)
# -----------------------------------------------------------------------------
SCENARIOS = [
    "Base Case (Approved Plan: 29.0 MWp Stage-Timed)",
    "Committed Downside (Signed PPAs Only: 16.2 MWp)",
    "Zero-Slippage Nominal (Prob-Weighted: 34.1 MWp)",
    "Full Pipeline Upside (100% Ceiling: 68.5 MWp)",
    "Bull Market (+10% Commodity Price Inflation)",
    "Bear Market (-10% Commodity Price Deflation)"
]

SCENARIO_DEFAULTS = {
    "Base Case (Approved Plan: 29.0 MWp Stage-Timed)": {
        "signed": 0.92, "neg": 0.55, "early": 0.20, "hrc": 0, "cu": 0, "al": 0, "timing": "Stage-Timed"
    },
    "Committed Downside (Signed PPAs Only: 16.2 MWp)": {
        "signed": 0.92, "neg": 0.00, "early": 0.00, "hrc": 0, "cu": 0, "al": 0, "timing": "Stage-Timed"
    },
    "Zero-Slippage Nominal (Prob-Weighted: 34.1 MWp)": {
        "signed": 0.92, "neg": 0.55, "early": 0.20, "hrc": 0, "cu": 0, "al": 0, "timing": "Project Start-Timed (0 Slip)"
    },
    "Full Pipeline Upside (100% Ceiling: 68.5 MWp)": {
        "signed": 1.00, "neg": 1.00, "early": 1.00, "hrc": 0, "cu": 0, "al": 0, "timing": "Project Start-Timed (0 Slip)"
    },
    "Bull Market (+10% Commodity Price Inflation)": {
        "signed": 0.92, "neg": 0.55, "early": 0.20, "hrc": 10, "cu": 10, "al": 10, "timing": "Stage-Timed"
    },
    "Bear Market (-10% Commodity Price Deflation)": {
        "signed": 0.92, "neg": 0.55, "early": 0.20, "hrc": -10, "cu": -10, "al": -10, "timing": "Stage-Timed"
    }
}

if "scenario_choice" not in st.session_state:
    st.session_state.scenario_choice = SCENARIOS[0]

def apply_scenario_preset():
    choice = st.session_state.scenario_choice
    defs = SCENARIO_DEFAULTS[choice]
    st.session_state.signed_conv = defs["signed"]
    st.session_state.neg_conv = defs["neg"]
    st.session_state.early_conv = defs["early"]
    st.session_state.hrc_shock_pct = defs["hrc"]
    st.session_state.cu_shock_pct = defs["cu"]
    st.session_state.al_shock_pct = defs["al"]

# Initialize default slider values if not present
if "signed_conv" not in st.session_state:
    apply_scenario_preset()
if "carrying_cost_rate" not in st.session_state:
    st.session_state.carrying_cost_rate = 1.25
if "gi_rate_lock_active" not in st.session_state:
    st.session_state.gi_rate_lock_active = True
if "rebalance_dc_active" not in st.session_state:
    st.session_state.rebalance_dc_active = True
if "custom_data_pack" not in st.session_state:
    st.session_state.custom_data_pack = None

# Ingest data pack
resolved_source = resolve_data_pack_source(st.session_state.custom_data_pack)
data_pack = load_and_audit_data_pack(resolved_source)

if data_pack is None:
    st.error("No valid Data Pack found. Please upload `Kit-to-Site_Data_Pack.xlsx` in Tab 2 (Simulation Controls).")
    st.stop()

# -----------------------------------------------------------------------------
# CORE ANALYTICAL CALCULATION ENGINE
# -----------------------------------------------------------------------------
scenario_choice = st.session_state.scenario_choice
signed_conv = st.session_state.signed_conv
neg_conv = st.session_state.neg_conv
early_conv = st.session_state.early_conv
hrc_shock_pct = st.session_state.hrc_shock_pct
cu_shock_pct = st.session_state.cu_shock_pct
al_shock_pct = st.session_state.al_shock_pct
carrying_cost_rate = st.session_state.carrying_cost_rate / 100.0
gi_rate_lock_active = st.session_state.gi_rate_lock_active
rebalance_dc_active = st.session_state.rebalance_dc_active
def_timing = SCENARIO_DEFAULTS[scenario_choice]["timing"]

ph_clean = data_pack["Price_History_Cleaned"]
pipe_raw = data_pack["Pipeline"]
ws_clean = data_pack["Warehouse_Stock_Cleaned"]
audit_df = data_pack["Audit_Log"]

# 1. Econometric Pass-Through Regressions
hrc_lag_series = ph_clean["Steel HRC index (Rs/tonne)"].iloc[:-1].values
gi_actual_series = ph_clean["FPEL price: GI structure (Rs/kg)"].iloc[1:].values
p_gi = np.polyfit(hrc_lag_series, gi_actual_series, 1) # [slope, intercept]
r_gi = np.corrcoef(hrc_lag_series, gi_actual_series)[0, 1]

cu_series = ph_clean["Copper MCX (Rs/kg)"].values
dc_series = ph_clean["FPEL price: DC cable 4 sq mm (Rs/m)"].values
p_dc = np.polyfit(cu_series, dc_series, 1)
r_dc = np.corrcoef(cu_series, dc_series)[0, 1]

al_series = ph_clean["Aluminium MCX (Rs/kg)"].values
ac_series = ph_clean["FPEL price: AC cable 3.5C 150 sq mm Al (Rs/m)"].values
p_ac = np.polyfit(al_series, ac_series, 1)
r_al = np.corrcoef(al_series, ac_series)[0, 1]

# 2. Monthly Commodity Indices & Finished Material Prices
months = ["Oct-2026", "Nov-2026", "Dec-2026", "Jan-2027", "Feb-2027", "Mar-2027"]
sep_hrc = 52300.0
sep_cu = 908.0
sep_al = 240.0

base_hrc_monthly = np.array([52300, 52800, 53200, 53500, 53200, 52900]) * (1.0 + hrc_shock_pct / 100.0)
base_cu_monthly = np.array([908, 905, 912, 918, 910, 905]) * (1.0 + cu_shock_pct / 100.0)
base_al_monthly = np.array([240, 242, 244, 245, 243, 241]) * (1.0 + al_shock_pct / 100.0)

# Finished material prices
gi_monthly_prices = []
for i in range(6):
    lagged_hrc = (sep_hrc * (1.0 + hrc_shock_pct / 100.0)) if i == 0 else base_hrc_monthly[i-1]
    gi_monthly_prices.append(p_gi[1] + p_gi[0] * lagged_hrc)
gi_monthly_prices = np.array(gi_monthly_prices)

dc_monthly_prices = np.array([p_dc[1] + p_dc[0] * cu for cu in base_cu_monthly])
ac_monthly_prices = np.array([p_ac[1] + p_ac[0] * al for al in base_al_monthly])

# 3. Dynamic Pipeline Demand Engine
m_map = {"2026-10": 0, "2026-11": 1, "2026-12": 2, "2027-01": 3, "2027-02": 4, "2027-03": 5}
pipe = pipe_raw.copy()
pipe["m_idx"] = pipe["Expected start month"].map(m_map)
pipe["is_rcc"] = pipe["Roof type"].str.upper().str.contains("RCC")

kwp_starts = np.zeros(8)
kwp_rcc_starts = np.zeros(8)

for _, row in pipe.iterrows():
    m = row["m_idx"]
    if pd.isna(m) or m < 0:
        continue
    m = int(m)
    stage = row["Stage"]
    cap = float(row["Est. capacity (kWp)"])
    is_rcc = row["is_rcc"]
    
    if "Signed" in stage:
        wt = signed_conv
        splits = {0: 1.0} if "0 Slip" in def_timing else {0: 0.25, 1: 0.75} # 3w slip
    elif "Negotiation" in stage:
        wt = neg_conv
        splits = {0: 1.0} if "0 Slip" in def_timing else {1: 0.50, 2: 0.50} # 6w slip
    else: # Early
        wt = early_conv
        splits = {0: 1.0} if "0 Slip" in def_timing else {1: 0.50, 2: 0.50}
        
    for offset, pct in splits.items():
        if m + offset < 8:
            kwp_starts[m + offset] += cap * wt * pct
            if is_rcc:
                kwp_rcc_starts[m + offset] += cap * wt * pct

# Stage-timed installation requirements
gi_demand = kwp_rcc_starts[:6] * 40.0 # S1 Day 0

dc_kwp = np.zeros(8)
for i in range(7):
    dc_kwp[i] += kwp_starts[i] * 0.5
    dc_kwp[i+1] += kwp_starts[i] * 0.5
dc_demand_each = dc_kwp[:6] * 14.5 # S3 Day 14-35

ac_kwp = np.zeros(8)
for i in range(7):
    ac_kwp[i] += kwp_starts[i] * 0.3
    ac_kwp[i+1] += kwp_starts[i] * 0.7
ac_demand = ac_kwp[:6] * 0.75 # S4 Day 20-40

# 4. Inventory Balances & Procurement Plan
# A. Fabricated GI Structure
gi_opening = 4644.0 # Pune on-hand
curr_gi_stock = gi_opening
gi_net_buys = []
gi_closing_stocks = []
gi_spends = []
gi_carry_costs = []

for i in range(6):
    d = gi_demand[i]
    p = 92.60 if (gi_rate_lock_active and i < 3) else gi_monthly_prices[i]
    target_buffer = (gi_demand[i+1] * 0.5) if i < 5 else 60000.0
    
    # Oct rate lock order covers Q4
    if i == 0 and gi_rate_lock_active:
        buy = max(0.0, 170000.0 - gi_opening)
    else:
        buy = max(0.0, (d + target_buffer) - curr_gi_stock)
        
    gi_net_buys.append(buy)
    curr_gi_stock = curr_gi_stock + buy - d
    gi_closing_stocks.append(curr_gi_stock)
    sp = buy * p
    gi_spends.append(sp)
    gi_carry_costs.append(curr_gi_stock * p * carrying_cost_rate)

# B. DC Solar Cable
dc_opening_rd = 13438.0
dc_opening_bk = 13407.0
rebalance_qty = 20000.0 if rebalance_dc_active else 0.0
curr_stock_rd = dc_opening_rd + rebalance_qty
curr_stock_bk = dc_opening_bk + rebalance_qty

dc_buys_rd = []
dc_buys_bk = []
dc_closing_rd = []
dc_closing_bk = []
dc_spends = []
dc_carry_costs = []

for i in range(6):
    d = dc_demand_each[i]
    p = dc_monthly_prices[i]
    target_buf = (dc_demand_each[i+1] * 0.5) if i < 5 else 50000.0
    
    buy_rd = max(0.0, (d + target_buf) - curr_stock_rd)
    buy_bk = max(0.0, (d + target_buf) - curr_stock_bk)
    
    dc_buys_rd.append(buy_rd)
    dc_buys_bk.append(buy_bk)
    
    curr_stock_rd = curr_stock_rd + buy_rd - d
    curr_stock_bk = curr_stock_bk + buy_bk - d
    dc_closing_rd.append(curr_stock_rd)
    dc_closing_bk.append(curr_stock_bk)
    
    sp = (buy_rd + buy_bk) * p
    dc_spends.append(sp)
    dc_carry_costs.append((curr_stock_rd + curr_stock_bk) * p * carrying_cost_rate)

# C. Aluminium AC Cable
ac_opening = 6431.0 # Usable opening stock (including TR-071)
curr_ac_stock = ac_opening
ac_buys = []
ac_closing_stocks = []
ac_spends = []
ac_carry_costs = []

for i in range(6):
    d_ac = ac_demand[i]
    p_ac_m = ac_monthly_prices[i]
    target_buf = (ac_demand[i+1] * 0.5) if i < 5 else 2573.0
    
    if i < 2 and (curr_ac_stock >= d_ac):
        buy_ac = 0.0
    else:
        buy_ac = max(0.0, (d_ac + target_buf) - curr_ac_stock)
        
    ac_buys.append(buy_ac)
    curr_ac_stock = curr_ac_stock + buy_ac - d_ac
    ac_closing_stocks.append(curr_ac_stock)
    sp = buy_ac * p_ac_m
    ac_spends.append(sp)
    ac_carry_costs.append(curr_ac_stock * p_ac_m * carrying_cost_rate)

# Automated PO Release Dates
delivery_dates = [datetime(2026, 10, 15) + timedelta(days=i*30) for i in range(6)]
gi_po_dates = [(d - timedelta(days=18)).strftime("%Y-%m-%d") for d in delivery_dates] # 18d lead
dc_po_dates = [(d - timedelta(days=7)).strftime("%Y-%m-%d") for d in delivery_dates]  # 7d lead
ac_po_dates = [(d - timedelta(days=10)).strftime("%Y-%m-%d") for d in delivery_dates] # 10d lead

tot_6m_spend = sum(gi_spends) + sum(dc_spends) + sum(ac_spends)
tot_carry_cost = sum(gi_carry_costs) + sum(dc_carry_costs) + sum(ac_carry_costs)

# -----------------------------------------------------------------------------
# FPEL BRAND MASTHEAD (MATCHING FOURTHPARTNER.CO OFFICIAL IDENTITY)
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="fpel-masthead">
    <div class="fpel-brand-wrap">
        <div class="fpel-logo-svg">
            <svg width="34" height="34" viewBox="0 0 40 40" fill="none">
                <circle cx="20" cy="11" r="4.5" fill="#FFFFFF"/>
                <path d="M10 20C14 16 26 16 30 20" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
                <rect x="13" y="24" width="3.5" height="12" rx="1.5" fill="#FFFFFF"/>
                <rect x="18.25" y="22" width="3.5" height="14" rx="1.5" fill="#FFFFFF"/>
                <rect x="23.5" y="24" width="3.5" height="12" rx="1.5" fill="#FFFFFF"/>
            </svg>
        </div>
        <div class="fpel-title-box">
            <h1>FOURTH PARTNER ENERGY</h1>
            <p>Material Buy-or-Hold Forecaster · Kit-to-Site Operations Decision Engine</p>
        </div>
    </div>
    <div class="fpel-meta-badges">
        <div class="fpel-sun-badge">
            <span class="fpel-sun-dot"></span>
            <span>Horizon: Oct 2026 – Mar 2027</span>
        </div>
        <div class="fpel-pill-button">
            {scenario_choice.split('(')[0].strip()}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SLEEK TOP QUICK SCENARIO SELECTOR RIBBON
# -----------------------------------------------------------------------------
ribbon_col1, ribbon_col2 = st.columns([1.2, 2.8])
with ribbon_col1:
    st.selectbox(
        "Active Scenario Preset",
        SCENARIOS,
        index=SCENARIOS.index(st.session_state.scenario_choice),
        key="scenario_choice",
        on_change=apply_scenario_preset,
        help="Instantly update all probabilities, lead times, commodity shocks, and procurement quantities."
    )
with ribbon_col2:
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; margin-top:28px; flex-wrap:wrap;">
        <span class="ribbon-pill active">Demand: <b>{kwp_starts[:6].sum():,.1f} kWp</b></span>
        <span class="ribbon-pill">Spend: <b>₹{tot_6m_spend/1e5:,.1f} L</b></span>
        <span class="ribbon-pill">HRC Shock: <b>{hrc_shock_pct:+d}%</b></span>
        <span class="ribbon-pill">DC Rebalance: <b>{'Active (40km)' if rebalance_dc_active else 'Disabled'}</b></span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7 PRODUCTION WORKSPACES (STREAMLINED CORE TABS)
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "Executive Overview",
    "Simulation Controls",
    "Commodity Forecaster",
    "Pipeline Demand",
    "Inventory & Rebalance",
    "PO Schedule & Dates",
    "Forensic Audit & Exports"
])

# =============================================================================
# TAB 1: EXECUTIVE COMMAND CENTER
# =============================================================================
with tabs[0]:
    with st.container(border=True):
        st.markdown(f"""
<div style="font-size: 11.5px; font-weight: 700; letter-spacing: 1px; color: {ACCENT_COLOR}; text-transform: uppercase; margin-bottom: 6px;">
    Strategic Action Directives
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 12.5px; line-height: 1.55; color: #CBD5E1;">
    <div>• <b style="color: #FFFFFF;">GI Steel Structure:</b> Lock 170,000 kg call-off contract @ ₹92.60/kg for Q4. Ship direct to site (18d lead time).</div>
    <div>• <b style="color: #FFFFFF;">DC Solar Cable:</b> Transfer 40,000m (20k Red + 20k Black) AMD → PUN in Week 1. Rolling bi-weekly POs start Dec 1.</div>
    <div>• <b style="color: #FFFFFF;">AC Aluminium Cable:</b> Consume 6,431m network stock in Oct–Nov. Release monthly OEM cut-length orders from Dec 1.</div>
    <div>• <b style="color: #FFFFFF;">Direct-to-Site Dispatch:</b> Direct fabricator & OEM shipments reduce warehouse floor footprint to 27.3%, eliminating store bottlenecks.</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    
    # 5 Responsive Metric Cards with Native Sparklines
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric(
        label="Active 6M Demand",
        value=f"{kwp_starts[:6].sum():,.1f} kWp",
        delta=scenario_choice.split('(')[0].strip(),
        border=True,
        chart_data=list(kwp_starts[:6]),
        chart_type="bar"
    )
    k2.metric(
        label="6-Month Net Spend",
        value=f"₹{tot_6m_spend/1e5:,.1f} L",
        delta=f"₹{tot_6m_spend/1e7:.2f} Cr Budget",
        border=True,
        chart_data=[(gi_spends[i] + dc_spends[i] + ac_spends[i])/1e5 for i in range(6)],
        chart_type="line"
    )
    k3.metric(
        label="GI Steel Net Buy",
        value=f"{sum(gi_net_buys):,.0f} kg",
        delta=f"₹{sum(gi_spends)/1e5:,.1f} L spend",
        border=True,
        chart_data=[b/1e3 for b in gi_net_buys],
        chart_type="line"
    )
    k4.metric(
        label="DC Cable Net Buy",
        value=f"{sum(dc_buys_rd)+sum(dc_buys_bk):,.0f} m",
        delta=f"₹{sum(dc_spends)/1e5:,.1f} L spend",
        border=True,
        chart_data=[(dc_buys_rd[i]+dc_buys_bk[i])/1e3 for i in range(6)],
        chart_type="line"
    )
    k5.metric(
        label="Carrying Cost",
        value=f"₹{tot_carry_cost/1e5:,.1f} L",
        delta=f"@{carrying_cost_rate*100:.2f}%/mo rate",
        border=True,
        chart_data=[(gi_carry_costs[i]+dc_carry_costs[i]+ac_carry_costs[i])/1e3 for i in range(6)],
        chart_type="area"
    )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:14px; font-weight:700; color:{TEXT_WHITE}; margin-bottom:10px;'>Three Material-Specific Buy-or-Hold Decision Cards</div>", unsafe_allow_html=True)
    
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        with st.container(border=True):
            st.markdown(f"""
<div class="decision-card-body">
<div>
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
<span class="pill-buy">BUY NOW / RATE LOCK</span>
<span style="font-size: 11px; font-weight: 700; color: #38BDF8; background: rgba(2, 132, 199, 0.2); padding: 3px 9px; border-radius: 9999px; border: 1px solid rgba(56, 189, 248, 0.4);">Score: 88/100</span>
</div>
<div style="font-size: 17px; font-weight: 800; color: #FFFFFF; margin-bottom: 2px;">Fabricated GI Structure</div>
<div style="font-size: 11px; font-weight: 500; color: #94A3B8; margin-bottom: 12px;">SKU: STR-RCC-GI · Steel HRC (1-Mo Lag)</div>

<div class="subcard-gi">
<div><b style="color: #FFFFFF;">Current Price:</b> ₹92.60/kg (Sep-26 actual)</div>
<div><b style="color: #FFFFFF;">Forecast Oct Price:</b> ₹{gi_monthly_prices[0]:.2f}/kg (+{((gi_monthly_prices[0]-92.6)/92.6)*100:.1f}%)</div>
<div><b style="color: #FFFFFF;">Recommended Action:</b> Lock 170 tonnes @ ₹92.60/kg for Q4</div>
<div><b style="color: #FFFFFF;">6M Net Requirement:</b> {sum(gi_net_buys):,.0f} kg (₹{sum(gi_spends)/1e5:,.1f} L)</div>
<div><b style="color: #FFFFFF;">Supplier Lead Time:</b> 18 days</div>
</div>

<p style="font-size: 12px; line-height: 1.55; color: #CBD5E1; margin: 12px 0 8px 0;">
<b style="color: #FFFFFF;">Reasoning:</b> HRC bottomed in Aug (₹51,600) and rose +1.36% in Sep. Because finished GI pricing lags HRC by 1 month (r = 0.9822), Oct fabricator price will rise to ₹{gi_monthly_prices[0]:.2f}/kg. Locking captures immediate savings. Direct fabricator dispatch eliminates warehouse congestion.
</p>
</div>
<div class="reversal-callout">
<b style="color: #EF4444;">Policy Reversal:</b> Exit rate lock if HRC falls below ₹49,000/t or RCC pipeline drops below 35%.
</div>
</div>
""", unsafe_allow_html=True)
        
    with col_d2:
        with st.container(border=True):
            st.markdown(f"""
<div class="decision-card-body">
<div>
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
<span class="pill-transfer">REBALANCE & CALL-OFF</span>
<span style="font-size: 11px; font-weight: 700; color: #FBBF24; background: rgba(245, 158, 11, 0.2); padding: 3px 9px; border-radius: 9999px; border: 1px solid rgba(245, 158, 11, 0.4);">Score: 35/100</span>
</div>
<div style="font-size: 17px; font-weight: 800; color: #FFFFFF; margin-bottom: 2px;">DC Solar Cable 4 sq mm</div>
<div style="font-size: 11px; font-weight: 500; color: #94A3B8; margin-bottom: 12px;">SKU: DC-4-RD & BK · Copper MCX</div>

<div class="subcard-dc">
<div><b style="color: #FFFFFF;">Current Price:</b> ₹58.70/m (Cleaned Copper ₹{base_cu_monthly[0]:.0f}/kg)</div>
<div><b style="color: #FFFFFF;">Cleaned 12M Mean:</b> ₹889.9/kg (Sep is +2.0% ABOVE average)</div>
<div><b style="color: #FFFFFF;">Recommended Action:</b> Transfer 40k m AMD → PUN (TR-072)</div>
<div><b style="color: #FFFFFF;">6M Net Requirement:</b> {sum(dc_buys_rd)+sum(dc_buys_bk):,.0f} m (₹{sum(dc_spends)/1e5:,.1f} L)</div>
<div><b style="color: #FFFFFF;">Supplier Lead Time:</b> 7 days</div>
</div>

<p style="font-size: 12px; line-height: 1.55; color: #CBD5E1; margin: 12px 0 8px 0;">
<b style="color: #FFFFFF;">Reasoning:</b> Reject Arjun's 6-month upfront buy request. Copper is NOT cheap; Arjun's claim relies on a 10x Mar-26 typo (₹8,940 vs ₹894/kg). Carrying 6 months costs 7.5%. Rebalancing 40km cable at ₹36k freight covers Pune until Dec at zero new material cost.
</p>
</div>
<div class="reversal-callout">
<b style="color: #EF4444;">Policy Reversal:</b> Forward buy only if Copper MCX drops below ₹840/kg.
</div>
</div>
""", unsafe_allow_html=True)

    with col_d3:
        with st.container(border=True):
            st.markdown(f"""
<div class="decision-card-body">
<div>
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
<span class="pill-hold">HOLD & CUT-DRUM</span>
<span style="font-size: 11px; font-weight: 700; color: #FB923C; background: rgba(251, 146, 60, 0.2); padding: 3px 9px; border-radius: 9999px; border: 1px solid rgba(251, 146, 60, 0.4);">Score: 42/100</span>
</div>
<div style="font-size: 17px; font-weight: 800; color: #FFFFFF; margin-bottom: 2px;">Aluminium AC Armoured Cable</div>
<div style="font-size: 11px; font-weight: 500; color: #94A3B8; margin-bottom: 12px;">SKU: AC-AL-150 · Aluminium MCX</div>

<div class="subcard-ac">
<div><b style="color: #FFFFFF;">Current Price:</b> ₹527.00/m (Aluminium ₹{base_al_monthly[0]:.0f}/kg)</div>
<div><b style="color: #FFFFFF;">12M Aluminium Mean:</b> ₹244.2/kg (Sep is -1.7% below average)</div>
<div><b style="color: #FFFFFF;">Opening Usable Stock:</b> 6,431 m (covers Oct–Nov demand)</div>
<div><b style="color: #FFFFFF;">6M Net Requirement:</b> {sum(ac_buys):,.0f} m (₹{sum(ac_spends)/1e5:,.1f} L)</div>
<div><b style="color: #FFFFFF;">Supplier Lead Time:</b> 10 days</div>
</div>

<p style="font-size: 12px; line-height: 1.55; color: #CBD5E1; margin: 12px 0 8px 0;">
<b style="color: #FFFFFF;">Reasoning:</b> Aluminium is stable with short 10-day lead time. Current usable inventory (6,431 m incl. TR-071) easily covers Oct–Nov demand ({ac_demand[:2].sum():,.0f} m). Ordering OEM cut-lengths from Dec minimizes scrap and working capital.
</p>
</div>
<div class="reversal-callout">
<b style="color: #EF4444;">Policy Reversal:</b> Lock 60 days of requirement only if Aluminium MCX spikes >15% (>₹275/kg).
</div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# TAB 2: SIMULATION CONTROLS & SCENARIO ENGINE (SIDEBAR REPLACEMENT)
# =============================================================================
with tabs[1]:
    st.markdown("### Simulation Controls, Pipeline Probabilities & Macro Shocks")
    st.markdown("Fine-tune conversion ratios, commodity stress tests, and operational policies. All procurement quantities, cash flows, and PO releases recalculate in real time.")
    
    sim_col1, sim_col2 = st.columns(2)
    
    with sim_col1:
        with st.container(border=True):
            st.markdown(f"<div style='font-size: 14px; font-weight: 700; color: {TEXT_WHITE}; margin-bottom: 12px;'>1. Pipeline Stage Conversion Probabilities</div>", unsafe_allow_html=True)
            new_signed = st.slider(
                "Signed PPA Conversion Rate",
                min_value=0.70, max_value=1.00, value=float(st.session_state.signed_conv), step=0.02,
                help="Approved Base Case assumes 92% conversion with a 3-week installation slippage (25% in start month, 75% in month+1)."
            )
            new_neg = st.slider(
                "Negotiation Stage Conversion Rate",
                min_value=0.00, max_value=0.80, value=float(st.session_state.neg_conv), step=0.05,
                help="Approved Base Case assumes 55% conversion with a 6-week slippage (50% in month+1, 50% in month+2)."
            )
            new_early = st.slider(
                "Early Proposal Conversion Rate",
                min_value=0.00, max_value=0.50, value=float(st.session_state.early_conv), step=0.05,
                help="Approved Base Case assumes 20% conversion with a 6-week slippage."
            )
            
            if (new_signed != st.session_state.signed_conv or 
                new_neg != st.session_state.neg_conv or 
                new_early != st.session_state.early_conv):
                st.session_state.signed_conv = new_signed
                st.session_state.neg_conv = new_neg
                st.session_state.early_conv = new_early
                st.rerun()
                
            st.markdown(f"""
            <div style="font-size: 11.5px; color: #94A3B8; background: rgba(255, 255, 255, 0.04); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08); margin-top: 10px;">
                <b>Timing Model:</b> Incorporates empirically observed sales cycle slippage (3 weeks for Signed, 6 weeks for Negotiation/Early).
            </div>
            """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"<div style='font-size: 14px; font-weight: 700; color: {TEXT_WHITE}; margin-bottom: 12px;'>3. Operational Procurement Policies</div>", unsafe_allow_html=True)
            new_cc = st.slider(
                "Monthly Inventory Carrying Cost Rate (%/month)",
                min_value=0.50, max_value=2.50, value=float(st.session_state.carrying_cost_rate), step=0.25,
                help="Covers working capital financing, insurance, storage, and handling costs (standard FPEL baseline is 1.25%/mo = 15%/yr)."
            )
            if new_cc != st.session_state.carrying_cost_rate:
                st.session_state.carrying_cost_rate = new_cc
                st.rerun()
                
            new_lock = st.checkbox("Execute Q4 Fabricated GI Rate Lock (@ ₹92.60/kg)", value=bool(st.session_state.gi_rate_lock_active))
            if new_lock != st.session_state.gi_rate_lock_active:
                st.session_state.gi_rate_lock_active = new_lock
                st.rerun()
                
            new_reb = st.checkbox("Execute DC Cable Inter-Warehouse Rebalance (AMD → PUN, 40km)", value=bool(st.session_state.rebalance_dc_active))
            if new_reb != st.session_state.rebalance_dc_active:
                st.session_state.rebalance_dc_active = new_reb
                st.rerun()

    with sim_col2:
        with st.container(border=True):
            st.markdown(f"<div style='font-size: 14px; font-weight: 700; color: {TEXT_WHITE}; margin-bottom: 12px;'>2. Macro Commodity Stress Tests (% vs Baseline)</div>", unsafe_allow_html=True)
            new_hrc = st.slider(
                "Steel HRC Price Shock (%)",
                min_value=-20, max_value=20, value=int(st.session_state.hrc_shock_pct), step=5,
                help="Stress-test steel index variations. GI structure pricing adjusts with a 1-month lag (r = 0.9822)."
            )
            new_cu = st.slider(
                "Copper MCX Price Shock (%)",
                min_value=-20, max_value=20, value=int(st.session_state.cu_shock_pct), step=5,
                help="Stress-test Copper MCX shocks. Direct pass-through factor is 0.0573 Rs/m per Rs/kg Cu."
            )
            new_al = st.slider(
                "Aluminium MCX Price Shock (%)",
                min_value=-20, max_value=20, value=int(st.session_state.al_shock_pct), step=5,
                help="Stress-test Aluminium MCX shocks. Direct pass-through factor is 1.40 kg Al per metre."
            )
            
            if (new_hrc != st.session_state.hrc_shock_pct or 
                new_cu != st.session_state.cu_shock_pct or 
                new_al != st.session_state.al_shock_pct):
                st.session_state.hrc_shock_pct = new_hrc
                st.session_state.cu_shock_pct = new_cu
                st.session_state.al_shock_pct = new_al
                st.rerun()

            st.markdown(f"""
            <div style="font-size: 11.5px; color: #94A3B8; background: rgba(255, 255, 255, 0.04); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08); margin-top: 10px;">
                <b>Econometric Sensitivity:</b> Shocks propagate instantly through the regression models to finished fabricator quotes.
            </div>
            """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"<div style='font-size: 14px; font-weight: 700; color: {TEXT_WHITE}; margin-bottom: 12px;'>4. Custom Excel Data Pack Ingestion</div>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Upload Updated Kit-to-Site Data Pack (.xlsx)",
                type=["xlsx"],
                help="Upload an updated Excel workbook containing Pipeline, Price_History, and Warehouse_Stock sheets."
            )
            if uploaded_file is not None and uploaded_file != st.session_state.custom_data_pack:
                st.session_state.custom_data_pack = uploaded_file
                st.success("Custom Data Pack loaded successfully!")
                st.rerun()
                
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("Reset to Default Plan", width="stretch"):
                    st.session_state.scenario_choice = SCENARIOS[0]
                    apply_scenario_preset()
                    st.session_state.custom_data_pack = None
                    st.rerun()
            with c_btn2:
                st.markdown("<div style='font-size:11.5px; color:#94A3B8; text-align:center; padding-top:8px;'>Status: Active Base Pack</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 3: COMMODITY INTELLIGENCE & PASS-THROUGH FORECASTER
# =============================================================================
with tabs[2]:
    st.markdown("### Econometric Pass-Through Regressions & Monthly Price Trajectories")
    
    col_reg1, col_reg2, col_reg3 = st.columns(3)
    with col_reg1:
        st.markdown(f"""
        **Steel HRC → Fabricated GI Structure**
        - Formula: `Price_t = {p_gi[1]:.2f} + {p_gi[0]:.6f} × HRC_(t-1)`
        - **1-Month Lagged Correlation:** `r = {r_gi:.4f}` ($R^2 = {r_gi**2:.4f}$)
        - Same-Month Correlation: `r = 0.7151` (proves 1-month lag)
        - Forecast Oct Rate: **₹{gi_monthly_prices[0]:.2f}/kg**
        """)
    with col_reg2:
        st.markdown(f"""
        **Copper MCX → DC Solar Cable (Cleaned)**
        - Formula: `Price_t = {p_dc[1]:.2f} + {p_dc[0]:.5f} × Cu_t`
        - **Correlation:** `r = {r_dc:.4f}` ($R^2 = {r_dc**2:.4f}$)
        - Mar-26 Copper Typo: 8,940 corrected to 894 Rs/kg
        - Forecast Oct Rate: **₹{dc_monthly_prices[0]:.2f}/m**
        """)
    with col_reg3:
        st.markdown(f"""
        **Aluminium MCX → AC Cable**
        - Formula: `Price_t = {p_ac[1]:.2f} + {p_ac[0]:.4f} × Al_t`
        - **Correlation:** `r = {r_al:.4f}` ($R^2 = {r_al**2:.4f}$)
        - Stable pass-through factor: 1.40 kg Al / metre
        - Forecast Oct Rate: **₹{ac_monthly_prices[0]:.2f}/m**
        """)
        
    st.markdown("---")
    st.markdown("#### Monthly Finished Material Price Forecast (Oct 2026 – Mar 2027)")
    
    fc_price_df = pd.DataFrame({
        "Month": months,
        "Steel HRC (₹/t)": base_hrc_monthly.round(0),
        "GI Structure Price (₹/kg)": gi_monthly_prices.round(2),
        "Copper MCX (₹/kg)": base_cu_monthly.round(0),
        "DC Cable Price (₹/m)": dc_monthly_prices.round(2),
        "Aluminium MCX (₹/kg)": base_al_monthly.round(0),
        "AC Cable Price (₹/m)": ac_monthly_prices.round(2),
    })
    st.dataframe(fc_price_df, width="stretch")
    
    # Plotly Forecast Chart
    fig_p = go.Figure()
    fig_p.add_trace(go.Scatter(
        x=months, y=gi_monthly_prices, mode="lines+markers",
        name="GI Structure Forecast",
        line=dict(color=ACCENT_CYAN, width=2.5),
        marker=dict(size=7, color=ACCENT_CYAN)
    ))
    fig_p.add_hline(
        y=92.60, line_dash="dot", line_color=SUCCESS_COLOR,
        annotation_text="Q4 Rate Lock Offer (₹92.60/kg)",
        annotation_position="top left",
        annotation_font=dict(size=11, color=SUCCESS_COLOR)
    )
    format_minimal_chart(fig_p, "Fabricated GI Structure Price: Rate Lock vs Monthly Forecast", "₹ / kg")
    st.plotly_chart(fig_p, width="stretch", config={"displayModeBar": False})

# =============================================================================
# TAB 4: PIPELINE DEMAND ENGINE
# =============================================================================
with tabs[3]:
    st.markdown("### Six-Month Project Pipeline & Material Consumption Demand")
    
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        st.markdown("#### Pipeline Distribution by Sales Stage")
        stage_df = pipe.groupby("Stage")["Est. capacity (kWp)"].agg(["count", "sum"]).reset_index()
        stage_df.columns = ["Stage", "Projects Count", "Total Capacity (kWp)"]
        stage_df["Conversion Weight"] = stage_df["Stage"].map({
            "Signed (PPA executed)": f"{signed_conv*100:.0f}%",
            "Negotiation": f"{neg_conv*100:.0f}%",
            "Early (proposal sent)": f"{early_conv*100:.0f}%"
        })
        st.dataframe(stage_df, width="stretch")
        
    with col_d2:
        st.markdown("#### Roof Type Breakdown")
        roof_df = pipe.groupby("Roof type")["Est. capacity (kWp)"].agg(["count", "sum"]).reset_index()
        roof_df.columns = ["Roof Type", "Projects Count", "Total Capacity (kWp)"]
        st.dataframe(roof_df, width="stretch")
        
    st.markdown("#### Monthly Material Demand Schedule")
    m_dem_df = pd.DataFrame({
        "Month": months,
        "Active Project Starts (kWp)": kwp_starts[:6].round(1),
        "Fabricated GI Structure (kg)": gi_demand.round(0),
        "DC Cable per Polarity (m)": dc_demand_each.round(0),
        "Combined DC Cable (m)": (dc_demand_each * 2).round(0),
        "Aluminium AC Cable (m)": ac_demand.round(0)
    })
    st.dataframe(m_dem_df.style.format({
        "Active Project Starts (kWp)": "{:,.1f}",
        "Fabricated GI Structure (kg)": "{:,.0f}",
        "DC Cable per Polarity (m)": "{:,.0f}",
        "Combined DC Cable (m)": "{:,.0f}",
        "Aluminium AC Cable (m)": "{:,.0f}"
    }), width="stretch")
    
    with st.expander("View Transparent Demand Calculation Formulas"):
        st.markdown(r"""
        - **GI Structure Demand ($D_{\text{GI}}$):** $\text{Active RCC kWp} \times \frac{4,000 \text{ kg}}{100 \text{ kWp}} = \text{Active RCC kWp} \times 40.0$ (Stage S1, Day 0).
        - **DC Cable Demand ($D_{\text{DC}}$):** $\text{Active Total kWp} \times \frac{1,450 \text{ m}}{100 \text{ kWp}} = \text{Active Total kWp} \times 14.5$ per polarity (Stage S3, 45% duration = 50% Month $M$, 50% Month $M+1$).
        - **AC Cable Demand ($D_{\text{AC}}$):** $\text{Active Total kWp} \times \frac{75 \text{ m}}{100 \text{ kWp}} = \text{Active Total kWp} \times 0.75$ (Stage S4, 65% duration = 30% Month $M$, 70% Month $M+1$).
        """)

# =============================================================================
# TAB 5: INVENTORY & REBALANCING
# =============================================================================
with tabs[4]:
    st.markdown("### Store Inventory Balances (30-09-2026) & DC Cable Rebalance")
    
    focal_skus = ["STR-RCC-GI", "DC-4-RD", "DC-4-BK", "AC-AL-150"]
    stock_focal = ws_clean[ws_clean["SKU"].isin(focal_skus)][[
        "Store", "SKU", "Description", "On hand (30-09-2026)", "In_Transit", "Total_Usable", "UoM", "Avg monthly issue (Jul-Sep)"
    ]].copy()
    stock_focal["Stock Cover (Days)"] = (stock_focal["Total_Usable"] / stock_focal["Avg monthly issue (Jul-Sep)"]) * 30.0
    
    st.dataframe(stock_focal.style.format({
        "On hand (30-09-2026)": "{:,.0f}",
        "In_Transit": "{:,.0f}",
        "Total_Usable": "{:,.0f}",
        "Avg monthly issue (Jul-Sep)": "{:,.1f}",
        "Stock Cover (Days)": "{:.1f} d"
    }), width="stretch")
    
    st.markdown("---")
    st.markdown("#### DC Cable Network Rebalancing: Ahmedabad → Pune")
    st.info("Ahmedabad holds 62,700m Red and 63,000m Black (78 days cover — severe overstock), while Pune holds only 13,438m Red and 13,407m Black (12 days cover — severe deficit).")
    
    t_qty = st.slider("Transfer Quantity per Polarity (metres)", 5000, 30000, 20000, 5000)
    
    pun_post_rd = 13438.0 + (t_qty if rebalance_dc_active else 0.0)
    amd_post_rd = 62700.0 - (t_qty if rebalance_dc_active else 0.0)
    
    col_reb1, col_reb2, col_reb3 = st.columns(3)
    col_reb1.metric("Pune Red DC Stock Post-Transfer", f"{pun_post_rd:,.0f} m", f"+{t_qty:,.0f} m (30 days cover)")
    col_reb2.metric("Ahmedabad Stock Post-Transfer", f"{amd_post_rd:,.0f} m", f"-{t_qty:,.0f} m (53 days cover — safe)")
    col_reb3.metric("Transfer Freight Cost", "₹36,000", "Avoids spot purchases in Oct-Nov")

# =============================================================================
# TAB 6: PROCUREMENT SCHEDULE & PO DATES
# =============================================================================
with tabs[5]:
    st.markdown("### Month-by-Month Purchase Orders, Cash Flow & Automated PO Release Dates")
    
    planner_rows = []
    for i in range(6):
        planner_rows.append({
            "Month": months[i],
            "PO Release (GI)": gi_po_dates[i],
            "GI Net Buy (kg)": gi_net_buys[i],
            "GI Spend (₹)": gi_spends[i],
            "PO Release (DC)": dc_po_dates[i],
            "DC Net Buy (m)": dc_buys_rd[i] + dc_buys_bk[i],
            "DC Spend (₹)": dc_spends[i],
            "PO Release (AC)": ac_po_dates[i],
            "AC Net Buy (m)": ac_buys[i],
            "AC Spend (₹)": ac_spends[i],
            "Total Monthly Spend (₹)": gi_spends[i] + dc_spends[i] + ac_spends[i],
            "Monthly Carrying Cost (₹)": gi_carry_costs[i] + dc_carry_costs[i] + ac_carry_costs[i]
        })
        
    planner_df = pd.DataFrame(planner_rows)
    st.dataframe(planner_df.style.format({
        "GI Net Buy (kg)": "{:,.0f}",
        "GI Spend (₹)": "₹{:,.0f}",
        "DC Net Buy (m)": "{:,.0f}",
        "DC Spend (₹)": "₹{:,.0f}",
        "AC Net Buy (m)": "{:,.0f}",
        "AC Spend (₹)": "₹{:,.0f}",
        "Total Monthly Spend (₹)": "₹{:,.0f}",
        "Monthly Carrying Cost (₹)": "₹{:,.0f}"
    }), width="stretch")
    
    st.markdown(f"**Total Six-Month Procurement Spend:** `₹{tot_6m_spend/1e5:,.2f} Lakhs` (₹{tot_6m_spend/1e7:.2f} Crore)")
    
    # Stacked Cash Flow Chart
    fig_cf = go.Figure()
    fig_cf.add_trace(go.Bar(x=months, y=[s/1e5 for s in gi_spends], name="GI Steel Structure", marker_color=ACCENT_CYAN))
    fig_cf.add_trace(go.Bar(x=months, y=[s/1e5 for s in dc_spends], name="DC Solar Cable", marker_color=ACCENT_GOLD))
    fig_cf.add_trace(go.Bar(x=months, y=[s/1e5 for s in ac_spends], name="AC Cable", marker_color=SUCCESS_COLOR))
    format_minimal_chart(fig_cf, "Monthly Procurement Cash Outflow Bridge (₹ Lakhs)", "₹ Lakhs")
    fig_cf.update_layout(barmode="stack")
    st.plotly_chart(fig_cf, width="stretch", config={"displayModeBar": False})

# =============================================================================
# TAB 7: FORENSIC AUDIT & EXPORTS
# =============================================================================
with tabs[6]:
    st.markdown("### Forensic Data Health Audit & Export Center")
    st.dataframe(audit_df, width="stretch")
    
    st.markdown("---")
    c_e1, c_e2 = st.columns(2)
    with c_e1:
        st.markdown("#### Download Excel Decision Workbook")
        buf_xls = io.BytesIO()
        with pd.ExcelWriter(buf_xls, engine="openpyxl") as writer:
            planner_df.to_excel(writer, sheet_name="Procurement_Plan", index=False)
            m_dem_df.to_excel(writer, sheet_name="Monthly_Demand", index=False)
            fc_price_df.to_excel(writer, sheet_name="Price_Forecasts", index=False)
            stock_focal.to_excel(writer, sheet_name="Store_Inventory", index=False)
            audit_df.to_excel(writer, sheet_name="Audit_Log", index=False)
            
        st.download_button(
            label="Download Complete Excel Workbook (.xlsx)",
            data=buf_xls.getvalue(),
            file_name=f"FPEL_Procurement_Plan_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch"
        )
        
    with c_e2:
        st.markdown("#### Download Executive Decision PDF Memo")
        buf_pdf = io.BytesIO()
        doc = SimpleDocTemplate(buf_pdf, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
        p_styles = getSampleStyleSheet()
        
        pdf_story = []
        pdf_story.append(Paragraph("FOURTH PARTNER ENERGY LIMITED (FPEL)", ParagraphStyle("T1", parent=p_styles["Heading1"], fontSize=16, leading=20, textColor=colors.HexColor("#0B1329"))))
        pdf_story.append(Paragraph("Kit-to-Site Operations Advisory — Material Buy-or-Hold Decision Memo", ParagraphStyle("T2", parent=p_styles["Normal"], fontSize=9, textColor=colors.HexColor("#64748B"))))
        pdf_story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor(ACCENT_GOLD), spaceAfter=10))
        
        pdf_story.append(Paragraph("<b>1. EXECUTIVE BUY-OR-HOLD DECISION SCORECARD</b>", ParagraphStyle("H1", parent=p_styles["Heading2"], fontSize=11, leading=14, textColor=colors.HexColor("#0B1329"))))
        dec_tbl_data = [
            ["Material SKU", "Commodity", "Recommended Action", "6M Net Buy", "6M Spend"],
            ["STR-RCC-GI", "Steel HRC (1-Mo Lag)", "BUY NOW / Q4 RATE LOCK (170t @ Rs 92.60/kg)", f"{sum(gi_net_buys):,.0f} kg", f"Rs {sum(gi_spends)/1e5:,.1f} L"],
            ["DC-4-RD & BK", "Copper MCX", "HOLD BULK BUY; Rebalance 40k m AMD->PUN; rolling POs from Dec", f"{sum(dc_buys_rd)+sum(dc_buys_bk):,.0f} m", f"Rs {sum(dc_spends)/1e5:,.1f} L"],
            ["AC-AL-150", "Aluminium MCX", "HOLD BULK BUY; Consume 6,431m stock; monthly cut-drums from Dec", f"{sum(ac_buys):,.0f} m", f"Rs {sum(ac_spends)/1e5:,.1f} L"],
        ]
        t_pdf = Table(dec_tbl_data, colWidths=[90, 85, 200, 65, 75])
        t_pdf.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0B1329")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('FONTSIZE', (0,1), (-1,-1), 7.5),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ]))
        pdf_story.append(t_pdf)
        pdf_story.append(Spacer(1, 10))
        
        pdf_story.append(Paragraph("<b>2. STRATEGIC REASONING & PASS-THROUGH DYNAMICS</b>", ParagraphStyle("H2", parent=p_styles["Heading2"], fontSize=11, leading=14, textColor=colors.HexColor("#0B1329"))))
        reasons = [
            f"<b>GI Steel Rate Lock:</b> Steel HRC rose +1.36% in September. Due to the 1-month lag (r = {r_gi:.4f}), October fabricator pricing will rise to ~Rs {gi_monthly_prices[0]:.2f}/kg. Locking Rs 92.60/kg captures value. Direct-to-site delivery saves warehouse floor.",
            "<b>DC Cable Bulk Buy Rejection:</b> Arjun's bulk buy claim relies on a 10x Mar-26 typo (8,940 vs 894 Rs/kg). Copper is +2.0% ABOVE the true 12M mean (889.9 Rs/kg). Carrying 6 months costs 7.5%. Rebalancing 40km from AMD to PUN covers Q4 at Rs 36k freight.",
            "<b>AC Cable Stock Drawdown:</b> Aluminium is stable with 10-day lead time. Current usable stock (6,431m) covers Oct-Nov demand. Ordering OEM cut-lengths from Dec minimizes scrap."
        ]
        for r in reasons:
            pdf_story.append(Paragraph(f"• {r}", ParagraphStyle("B", parent=p_styles["Normal"], fontSize=8, leading=11)))
            pdf_story.append(Spacer(1, 4))
            
        doc.build(pdf_story)
        st.download_button(
            label="Download Executive PDF Memo (.pdf)",
            data=buf_pdf.getvalue(),
            file_name=f"FPEL_Material_Procurement_Decision_Memo_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            width="stretch"
        )
