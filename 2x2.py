import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Smoking Dashboard", layout="wide")

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("smoking.csv")

df = load_data()
col = "Data.Percentage.Total"

# ── First row: Map & Gender box ───────────────────────────────────────────────
r1c1, r1c2 = st.columns(2)

with r1c1:
    # choropleth map
    mdf = df.groupby("Country")[col].mean().reset_index()
    fig_map = px.choropleth(
        mdf,
        locations="Country",
        locationmode="country names",
        color=col,
    )
    fig_map.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_map, use_container_width=True)

with r1c2:
    # gender box plot
    if "Data.Percentage.Male" in df and "Data.Percentage.Female" in df:
        gdf = df.melt(
            id_vars=["Country","Year"],
            value_vars=["Data.Percentage.Male","Data.Percentage.Female"],
            var_name="Gender", value_name="Rate"
        )
        gdf["Gender"] = gdf["Gender"].str.replace("Data.Percentage.","")
        fig_box = px.box(gdf, x="Gender", y="Rate", points="all")
        fig_box.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_box, use_container_width=True)

# ── Second row: Trend line & Top-10 bar ────────────────────────────────────────
r2c1, r2c2 = st.columns(2)

with r2c1:
    # trend over time
    tdf = df.groupby("Year")[col].mean().reset_index()
    fig_line = px.line(tdf, x="Year", y=col, markers=True)
    fig_line.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_line, use_container_width=True)

with r2c2:
    # top-10 countries
    t10 = df.groupby("Country")[col].mean().nlargest(10).reset_index()
    fig_bar = px.bar(t10, x="Country", y=col)
    fig_bar.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_bar, use_container_width=True)
