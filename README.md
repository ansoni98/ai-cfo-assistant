# 💼 CFO.ai — AI-Powered Chief Financial Officer Assistant

> **AI & Fintech Course Project** — An executive-grade, AI-powered financial intelligence dashboard built with Streamlit and Claude (Anthropic).

---

## 🚀 Live Demo
Deploy on Streamlit Cloud → **[Your App Link Here]**

---

## 📌 Project Overview

CFO.ai is an intelligent financial assistant that combines:
- **6 interactive Plotly charts** (revenue, cashflow, OpEx, budget vs actual, balance sheet, P&L waterfall)
- **Real-time AI chat** powered by Claude (Anthropic) with full financial context
- **Executive KPI dashboard** with key metrics
- **Quick-question sidebar** for instant financial insights
- **Dark, premium UI** designed for management-level presentation

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App | Streamlit |
| AI Engine | Anthropic Claude (claude-opus-4-5) |
| Charts | Plotly |
| Data | Pandas + NumPy (simulated FY2024 data) |
| Deployment | Streamlit Cloud |
| Version Control | GitHub |

---

## 📂 Project Structure

```
ai_cfo_assistant/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .gitignore                # Excludes secrets from Git
├── .streamlit/
│   ├── config.toml           # Dark theme configuration
│   └── secrets.toml          # API key (NOT committed to GitHub)
└── README.md                 # This file
```

---

## ⚙️ Setup Instructions

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-cfo-assistant.git
cd ai-cfo-assistant
```

### Step 2 — Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Add Your API Key
Create the file `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```
> ⚠️ Never commit this file! It's in `.gitignore` for safety.

### Step 5 — Run Locally
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push your code to GitHub (without `secrets.toml`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New App** → select your repo → set main file as `app.py`
4. Go to **Settings → Secrets** and paste:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Click **Deploy** — live in ~2 minutes!

---

## 📊 Features

### Dashboard KPIs
- Annual Revenue with YoY growth
- EBITDA & Net Income
- Cash & Equivalents
- Monthly Burn Rate & Cash Runway

### Charts (6 total)
1. **Revenue vs Expenses vs Net Profit** — grouped bar + line combo
2. **Monthly Free Cash Flow** — area chart with target line
3. **OpEx Breakdown** — interactive donut chart by department
4. **Budget vs Actual** — grouped bar comparison
5. **Balance Sheet Snapshot** — stacked bar (assets vs liabilities)
6. **P&L Waterfall** — Revenue → COGS → EBIT → Net Income

### AI CFO Chat
Ask questions like:
- *"What is our cash runway and should we be concerned?"*
- *"Analyze the revenue trend and forecast Q1 2025"*
- *"Where should we cut costs to improve EBITDA margin?"*
- *"What are the top 3 financial risks we face?"*
- *"How does our DSO compare to industry benchmarks?"*

---

## 🎓 Academic Context

This project demonstrates the intersection of:
- **Artificial Intelligence** — LLM integration for financial reasoning
- **Fintech** — AI-augmented CFO decision support
- **Data Visualization** — Executive-grade financial dashboards
- **Software Engineering** — Full-stack web application deployment

---

## 📝 License
MIT License — built for educational purposes.
