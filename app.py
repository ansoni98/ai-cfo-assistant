import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from anthropic import Anthropic
import json
from datetime import datetime, timedelta
import random

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CFO.ai — Executive Financial Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* Global */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0a0f1e; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1428 0%, #0a0f1e 100%);
    border-right: 1px solid rgba(99,179,237,0.15);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #63b3ed !important;
    font-family: 'Syne', sans-serif !important;
}

/* Main header */
.cfo-header {
    background: linear-gradient(135deg, #0d1428 0%, #111827 50%, #0a0f1e 100%);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.cfo-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.cfo-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.02em;
}
.cfo-header .subtitle {
    color: #63b3ed;
    font-size: 0.95rem;
    font-weight: 300;
    margin-top: 6px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.cfo-header .live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(72,187,120,0.15);
    border: 1px solid rgba(72,187,120,0.3);
    color: #68d391;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 20px;
    margin-top: 10px;
}

/* KPI Cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 24px; }
.kpi-card {
    background: linear-gradient(135deg, #0d1428 0%, #111827 100%);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 14px;
    padding: 20px 22px;
    transition: border-color 0.3s;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--accent, #63b3ed);
    opacity: 0.6;
}
.kpi-card:hover { border-color: rgba(99,179,237,0.4); }
.kpi-label { color: #718096; font-size: 0.78rem; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 8px; }
.kpi-value { color: #f7fafc; font-family: 'Syne', sans-serif; font-size: 1.75rem; font-weight: 700; line-height: 1; }
.kpi-delta { font-size: 0.8rem; margin-top: 6px; }
.kpi-delta.up { color: #68d391; }
.kpi-delta.down { color: #fc8181; }

/* Chat Container */
.chat-container {
    background: #0d1428;
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 16px;
    padding: 0;
    overflow: hidden;
}
.chat-header {
    background: linear-gradient(90deg, #0d1428, #111827);
    border-bottom: 1px solid rgba(99,179,237,0.15);
    padding: 16px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}

/* Message Bubbles */
.msg-user {
    background: linear-gradient(135deg, #1a365d, #2a4a7f);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    color: #e2e8f0;
    font-size: 0.9rem;
    line-height: 1.6;
    max-width: 75%;
    margin-left: auto;
}
.msg-ai {
    background: linear-gradient(135deg, #111827, #1a2234);
    border: 1px solid rgba(99,179,237,0.12);
    border-left: 3px solid #63b3ed;
    border-radius: 4px 16px 16px 16px;
    padding: 16px 18px;
    color: #e2e8f0;
    font-size: 0.9rem;
    line-height: 1.7;
    max-width: 85%;
}
.msg-ai strong { color: #90cdf4; }
.msg-ai ul { margin: 8px 0; padding-left: 20px; }
.msg-ai li { margin-bottom: 4px; color: #cbd5e0; }

/* Insight Tags */
.insight-tag {
    display: inline-block;
    background: rgba(99,179,237,0.1);
    border: 1px solid rgba(99,179,237,0.25);
    color: #90cdf4;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px;
}
.insight-tag.warning { background: rgba(246,173,85,0.1); border-color: rgba(246,173,85,0.25); color: #f6ad55; }
.insight-tag.success { background: rgba(72,187,120,0.1); border-color: rgba(72,187,120,0.25); color: #68d391; }
.insight-tag.danger  { background: rgba(252,129,129,0.1); border-color: rgba(252,129,129,0.25); color: #fc8181; }

/* Section Titles */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title span { color: #63b3ed; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: rgba(99,179,237,0.3); border-radius: 3px; }

/* Streamlit overrides */
.stTextInput > div > div > input {
    background: #111827 !important;
    border: 1px solid rgba(99,179,237,0.25) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button {
    background: linear-gradient(135deg, #2b6cb0, #3182ce) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #3182ce, #4299e1) !important;
    transform: translateY(-1px);
}
.stSelectbox > div > div {
    background: #111827 !important;
    border: 1px solid rgba(99,179,237,0.25) !important;
    color: #e2e8f0 !important;
}
.stMetric { background: transparent !important; }
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0d1428, #111827);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 12px;
    padding: 16px;
}
div[data-testid="metric-container"] label { color: #718096 !important; font-size: 0.78rem !important; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #f7fafc !important; font-family: 'Syne', sans-serif !important; }
.stPlotlyChart { border-radius: 12px; overflow: hidden; }
hr { border-color: rgba(99,179,237,0.1) !important; }
.element-container { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Anthropic Client ──────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# ─── Financial Data Generator ─────────────────────────────────────────────────
@st.cache_data
def generate_financial_data():
    np.random.seed(42)
    months = pd.date_range("2024-01-01", periods=12, freq="MS")
    revenue = [4.2, 4.5, 4.1, 4.8, 5.2, 5.6, 5.3, 5.8, 6.1, 6.4, 6.8, 7.2]
    expenses = [3.1, 3.3, 3.0, 3.4, 3.7, 3.9, 3.8, 4.0, 4.2, 4.3, 4.5, 4.8]
    profit = [r - e for r, e in zip(revenue, expenses)]
    cashflow = [0.8, 1.0, 0.7, 1.1, 1.2, 1.5, 1.4, 1.6, 1.8, 1.9, 2.1, 2.2]

    dept_expenses = {
        "R&D": 28, "Sales & Marketing": 22, "Operations": 18,
        "HR": 12, "Finance": 8, "IT": 7, "Legal": 5
    }

    assets = {"Cash": 12.4, "AR": 8.6, "Inventory": 5.2, "Fixed Assets": 24.8, "Intangibles": 6.1}
    liabilities = {"AP": 4.2, "Short-term Debt": 3.8, "Long-term Debt": 12.5, "Deferred Tax": 2.1}

    budget_vs_actual = {
        "Revenue": {"budget": 68.0, "actual": 71.8},
        "COGS": {"budget": 28.0, "actual": 27.2},
        "OpEx": {"budget": 22.0, "actual": 23.4},
        "EBITDA": {"budget": 18.0, "actual": 21.2},
        "Net Income": {"budget": 12.0, "actual": 14.2},
    }

    return {
        "months": [m.strftime("%b %Y") for m in months],
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "cashflow": cashflow,
        "dept_expenses": dept_expenses,
        "assets": assets,
        "liabilities": liabilities,
        "budget_vs_actual": budget_vs_actual,
        "kpis": {
            "revenue": "$71.8M",
            "revenue_delta": "+12.4%",
            "ebitda": "$21.2M",
            "ebitda_delta": "+18.0%",
            "net_income": "$14.2M",
            "net_income_delta": "+15.6%",
            "cash": "$12.4M",
            "cash_delta": "+8.2%",
            "burn_rate": "$1.8M/mo",
            "runway": "6.9 months",
            "dso": "43 days",
            "current_ratio": "2.14x",
        }
    }

data = generate_financial_data()

# ─── Chart Builders ───────────────────────────────────────────────────────────
CHART_BG = "#0d1428"
CHART_PAPER = "#0a0f1e"
GRID_COLOR = "rgba(99,179,237,0.07)"
TEXT_COLOR = "#718096"
ACCENT = "#63b3ed"

def chart_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(family="Syne", size=14, color="#a0aec0"), x=0),
        paper_bgcolor=CHART_PAPER,
        plot_bgcolor=CHART_BG,
        font=dict(family="DM Sans", color=TEXT_COLOR),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor=GRID_COLOR, showline=False, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=GRID_COLOR, showline=False, tickfont=dict(size=11)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        hovermode="x unified",
    )

def revenue_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data["months"], y=data["revenue"],
        name="Revenue", marker_color="rgba(99,179,237,0.7)",
        marker_line_color="#63b3ed", marker_line_width=0.5
    ))
    fig.add_trace(go.Bar(
        x=data["months"], y=data["expenses"],
        name="Expenses", marker_color="rgba(252,129,129,0.6)",
        marker_line_color="#fc8181", marker_line_width=0.5
    ))
    fig.add_trace(go.Scatter(
        x=data["months"], y=data["profit"],
        name="Net Profit", mode="lines+markers",
        line=dict(color="#68d391", width=2.5),
        marker=dict(size=6, color="#68d391"),
    ))
    layout = chart_layout("Revenue vs Expenses vs Net Profit  (₹M)")
    layout["barmode"] = "group"
    layout["margin"] = dict(l=10, r=10, t=50, b=10)
    fig.update_layout(**layout)
    return fig

def cashflow_chart():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["months"], y=data["cashflow"],
        fill="tozeroy",
        fillcolor="rgba(99,179,237,0.12)",
        line=dict(color="#63b3ed", width=2),
        mode="lines",
        name="Free Cash Flow"
    ))
    fig.add_hline(y=1.5, line_dash="dash", line_color="rgba(246,173,85,0.5)", annotation_text="Target $1.5M")
    fig.update_layout(**chart_layout("Monthly Free Cash Flow  ($M)"))
    return fig

def department_pie():
    dept = data["dept_expenses"]
    colors = ["#63b3ed","#68d391","#f6ad55","#fc8181","#b794f4","#76e4f7","#fbb6ce"]
    fig = go.Figure(go.Pie(
        labels=list(dept.keys()),
        values=list(dept.values()),
        hole=0.6,
        marker=dict(colors=colors, line=dict(color=CHART_BG, width=3)),
        textfont=dict(size=11, family="DM Sans"),
        hovertemplate="<b>%{label}</b><br>%{value}% of OpEx<extra></extra>"
    ))
    layout = chart_layout("OpEx Breakdown by Department")
    layout["showlegend"] = True
    layout["legend"] = dict(orientation="v", font=dict(size=10))
    fig.update_layout(**layout)
    return fig

def budget_vs_actual_chart():
    bva = data["budget_vs_actual"]
    cats = list(bva.keys())
    budgets = [bva[c]["budget"] for c in cats]
    actuals = [bva[c]["actual"] for c in cats]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cats, y=budgets, name="Budget",
        marker_color="rgba(99,179,237,0.4)",
        marker_line_color="#63b3ed", marker_line_width=1
    ))
    fig.add_trace(go.Bar(
        x=cats, y=actuals, name="Actual",
        marker_color="rgba(104,211,145,0.7)",
        marker_line_color="#68d391", marker_line_width=1
    ))
    layout = chart_layout("Budget vs Actual  ($M)")
    layout["barmode"] = "group"
    fig.update_layout(**layout)
    return fig

def balance_sheet_chart():
    assets = data["assets"]
    liabilities = data["liabilities"]

    fig = go.Figure()
    asset_colors = ["#63b3ed","#76e4f7","#90cdf4","#bee3f8","#ebf8ff"]
    liab_colors  = ["#fc8181","#feb2b2","#fed7d7","#fff5f5"]

    for i, (k, v) in enumerate(assets.items()):
        fig.add_trace(go.Bar(
            x=["Assets"], y=[v], name=k,
            marker_color=asset_colors[i % len(asset_colors)],
        ))
    for i, (k, v) in enumerate(liabilities.items()):
        fig.add_trace(go.Bar(
            x=["Liabilities"], y=[v], name=k,
            marker_color=liab_colors[i % len(liab_colors)],
        ))

    layout = chart_layout("Balance Sheet Snapshot  ($M)")
    layout["barmode"] = "stack"
    fig.update_layout(**layout)
    return fig

def waterfall_chart():
    fig = go.Figure(go.Waterfall(
        name="P&L Waterfall",
        orientation="v",
        measure=["absolute","relative","relative","relative","relative","total"],
        x=["Revenue","COGS","Gross Profit*","OpEx","EBIT*","Net Income"],
        textposition="outside",
        text=["+$71.8M","-$27.2M","=$44.6M","-$23.4M","=$21.2M","=$14.2M"],
        y=[71.8, -27.2, 0, -23.4, 0, 0],
        connector=dict(line=dict(color="rgba(99,179,237,0.3)")),
        increasing=dict(marker=dict(color="rgba(104,211,145,0.8)")),
        decreasing=dict(marker=dict(color="rgba(252,129,129,0.8)")),
        totals=dict(marker=dict(color="rgba(99,179,237,0.8)")),
        textfont=dict(color="#e2e8f0", size=10)
    ))
    fig.update_layout(**chart_layout("P&L Waterfall — FY 2024"))
    return fig

# ─── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are CFO.ai, an elite AI Chief Financial Officer assistant for a technology company. 
You have deep expertise in corporate finance, financial analysis, risk management, and strategic planning.

COMPANY FINANCIAL DATA (FY 2024):
- Annual Revenue: $71.8M (+12.4% YoY)
- EBITDA: $21.2M (29.5% margin, +18% YoY)
- Net Income: $14.2M (+15.6% YoY)
- Cash & Equivalents: $12.4M
- Monthly Burn Rate: $1.8M
- Cash Runway: ~6.9 months
- Days Sales Outstanding (DSO): 43 days
- Current Ratio: 2.14x
- Debt-to-Equity: 0.68x

MONTHLY REVENUE (in $M): Jan:4.2, Feb:4.5, Mar:4.1, Apr:4.8, May:5.2, Jun:5.6, Jul:5.3, Aug:5.8, Sep:6.1, Oct:6.4, Nov:6.8, Dec:7.2

DEPARTMENT OPEX SPLIT: R&D 28%, Sales & Marketing 22%, Operations 18%, HR 12%, Finance 8%, IT 7%, Legal 5%

BALANCE SHEET: Total Assets $57.1M | Total Liabilities $22.6M | Equity $34.5M

BUDGET vs ACTUAL: Revenue beat budget by +$3.8M | EBITDA beat by +$3.2M | OpEx over-budget by $1.4M

RESPONSE GUIDELINES:
- Be direct, executive-level, and data-driven
- Use specific numbers from the data when answering
- Structure responses with clear headers using ** for bold
- Highlight risks with ⚠️ and opportunities with ✅
- When discussing trends, reference the actual monthly data
- Give actionable recommendations
- Keep tone: confident, concise, insightful
- For forecasts, use realistic assumptions based on the data
- Always end with 1-2 strategic recommendations labeled as 💡 **Strategic Insight:**"""

# ─── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-family: Syne; font-size:1.4rem; font-weight:800; color:#63b3ed;'>CFO.ai</div>
        <div style='font-size:0.7rem; color:#4a5568; letter-spacing:0.1em; text-transform:uppercase;'>Executive Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("### 📊 Quick Stats")
    st.metric("Revenue", "$71.8M", "+12.4%")
    st.metric("EBITDA Margin", "29.5%", "+1.8pp")
    st.metric("Cash Runway", "6.9 mo", "-0.2 mo")
    st.metric("Current Ratio", "2.14x", "+0.08x")

    st.divider()
    st.markdown("### ⚡ Quick Questions")

    quick_questions = [
        "📈 Revenue trend analysis",
        "💰 Cash runway & burn rate",
        "⚠️ Top financial risks",
        "🎯 Q1 2025 forecast",
        "📊 EBITDA improvement tips",
        "🔄 Working capital status",
        "💡 Cost reduction opportunities",
        "📉 DSO optimization strategy",
    ]

    for q in quick_questions:
        if st.button(q, use_container_width=True, key=f"quick_{q}"):
            st.session_state.messages.append({"role": "user", "content": q.split(" ", 1)[1]})
            st.rerun()

    st.divider()
    st.markdown(f"""
    <div style='font-size:0.75rem; color:#4a5568; text-align:center;'>
        Tokens used: {st.session_state.total_tokens:,}<br>
        Messages: {len(st.session_state.messages)}
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ─── Main Layout ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="cfo-header">
    <h1>💼 CFO.ai — Executive Financial Intelligence</h1>
    <div class="subtitle">AI-Powered Chief Financial Officer · Powered by Claude</div>
    <div class="live-badge">● LIVE &nbsp;|&nbsp; FY 2024 Data &nbsp;|&nbsp; Last updated: Today</div>
</div>
""", unsafe_allow_html=True)

# ─── KPI Row ──────────────────────────────────────────────────────────────────
k = data["kpis"]
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1: st.metric("Annual Revenue", k["revenue"], k["revenue_delta"])
with col2: st.metric("EBITDA", k["ebitda"], k["ebitda_delta"])
with col3: st.metric("Net Income", k["net_income"], k["net_income_delta"])
with col4: st.metric("Cash & Equiv.", k["cash"], k["cash_delta"])
with col5: st.metric("Burn Rate", k["burn_rate"], "")
with col6: st.metric("Cash Runway", k["runway"], "")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Charts Row 1 ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📈 <span>Financial Performance</span></div>', unsafe_allow_html=True)
c1, c2 = st.columns([3, 2])
with c1:
    st.plotly_chart(revenue_chart(), use_container_width=True, config={"displayModeBar": False})
with c2:
    st.plotly_chart(cashflow_chart(), use_container_width=True, config={"displayModeBar": False})

# ─── Charts Row 2 ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🧩 <span>Cost Structure & Budget</span></div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    st.plotly_chart(department_pie(), use_container_width=True, config={"displayModeBar": False})
with c4:
    st.plotly_chart(budget_vs_actual_chart(), use_container_width=True, config={"displayModeBar": False})

# ─── Charts Row 3 ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🏦 <span>Balance Sheet & P&L Waterfall</span></div>', unsafe_allow_html=True)
c5, c6 = st.columns(2)
with c5:
    st.plotly_chart(balance_sheet_chart(), use_container_width=True, config={"displayModeBar": False})
with c6:
    st.plotly_chart(waterfall_chart(), use_container_width=True, config={"displayModeBar": False})

st.divider()

# ─── AI Chat Section ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🤖 <span>Ask Your AI CFO</span></div>', unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(f'<div class="msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="💼"):
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about revenue, cash flow, risks, forecasts, budgets..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(f'<div class="msg-user">{prompt}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant", avatar="💼"):
        with st.spinner("Analyzing financial data..."):
            try:
                client = get_client()
                response = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=1200,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                )
                reply = response.content[0].text
                st.session_state.total_tokens += response.usage.input_tokens + response.usage.output_tokens
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.markdown(reply)
            except Exception as e:
                err = f"⚠️ Error connecting to AI: {str(e)}"
                st.error(err)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:30px 0 10px; color:#2d3748; font-size:0.78rem;'>
    CFO.ai &nbsp;·&nbsp; AI & Fintech Course Project &nbsp;·&nbsp; Powered by Claude (Anthropic)
    &nbsp;·&nbsp; Data is simulated for academic purposes
</div>
""", unsafe_allow_html=True)
