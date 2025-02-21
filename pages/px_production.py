import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, handle_file_upload

st.title("PX Production")

# Handle file upload or use default
uploaded_file = handle_file_upload()

# Load data
df = load_data(uploaded_file, sheet_index=2, skiprows=0, nrows=368)
df["Date"] = pd.to_datetime(df["Unnamed: 2"], format="%m-%d")
df["Date"] = df["Date"].dt.strftime("%b")
df_filtered = df.loc[:,  "Production: CCF":"Production: Predict"]
df_filtered.columns = ["2020", "2021", "2022", "2023", "2024", "2025", "2025 Estimate"]

df_long = df_filtered.copy()
df_long["Date"] = df["Date"]  # Add Date back for plotting
df_long = df_long.melt(id_vars=["Date"], var_name="Metric", value_name="Production")

# Sidebar for metric selection
metrics = df_long["Metric"].unique().tolist()

selected_metrics = st.sidebar.multiselect("Select Production Metrics", metrics, default=metrics)

# Filter data based on selection
df_plot = df_long[df_long["Metric"].isin(selected_metrics)]

df_plot = df_plot.dropna(subset=["Production"])

# Plot Production Trends
fig = px.line(df_plot, x="Date", y="Production", color="Metric",
              title="PX Production Trends",
              labels={"Production": "Production Volume", "Date": "Date", "Metric": "Production Type"})

fig.update_traces(line=dict(dash='dash'), selector=dict(name='2025 Estimate'))

st.plotly_chart(fig, use_container_width=True)

