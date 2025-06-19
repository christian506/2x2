import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Smoking Dashboard", layout="wide")

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("smoking.csv")

df = load_data()
years = sorted(df["Year"].astype(int).unique())
countries = sorted(df["Country"].unique())
metrics = [
    "Data.Percentage.Total",
    "Data.Percentage.Male",
    "Data.Percentage.Female",
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("Settings")
yr_min, yr_max = st.sidebar.slider("Period", min_value=years[0], max_value=years[-1],
                                   value=(years[0], years[-1]))
sel_ctrs = st.sidebar.multiselect("Origins", countries, countries)
item1 = st.sidebar.selectbox("Item 1", metrics, index=0)
item2 = st.sidebar.selectbox("Item 2", metrics, index=1)

# ── Filter ────────────────────────────────────────────────────────────────────
df_f = df[
    (df["Year"] >= yr_min) & (df["Year"] <= yr_max) &
    df["Country"].isin(sel_ctrs)
]

# ── Row 1 ─────────────────────────────────────────────────────────────────────
r1c1, r1c2 = st.columns(2)

with r1c1:
    cnt = df_f.groupby("Country").size().reset_index(name="count")
    fig1 = px.bar(cnt, x="Country", y="count")
    fig1.update_layout(height=300, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig1, use_container_width=True)

with r1c2:
    fig2 = px.scatter(df_f, x=item1, y=item2, color="Country")
    fig2.update_layout(height=300, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2 ─────────────────────────────────────────────────────────────────────
r2c1, r2c2 = st.columns(2)

with r2c1:
    t1 = df_f.groupby("Year")[item1].mean().reset_index()
    fig3 = px.line(t1, x="Year", y=item1, markers=True)
    fig3.update_layout(height=300, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    t2 = df_f.groupby("Year")[item2].mean().reset_index()
    fig4 = px.line(t2, x="Year", y=item2, markers=True)
    fig4.update_layout(height=300, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig4, use_container_width=True)
