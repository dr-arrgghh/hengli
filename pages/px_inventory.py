import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, handle_file_upload

st.title("PX Inventory")

# Handle file upload or use default
uploaded_file = handle_file_upload()

# Load data
df_change = load_data(uploaded_file, sheet_index=2, skiprows=0, nrows=368)
df_change["Date"] = pd.to_datetime(df_change["Unnamed: 2"], format="%m-%d")
df_change["Date"] = df_change["Date"].dt.strftime("%b")
df_change_filtered = df_change.loc[:,  "Δ Stock Change":"Δ Stock Change (Forecast): adjusted by Supply"][2:]
df_change_filtered.columns = ["2020", "2021", "2022", "2023", "2024", "2025", "2025 ΔS Adjusted"]

df_change_long = df_change_filtered.copy()
df_change_long["Date"] = df_change["Date"]  # Add Date back for plotting
df_change_long = df_change_long.melt(id_vars=["Date"], var_name="Metric", value_name="Δ Inventory")

# Sidebar for metric selection
metrics = df_change_long["Metric"].unique().tolist()

selected_metrics = st.sidebar.multiselect("Select Year (Δ Inventory)", metrics, default=metrics)

# Filter data based on selection
df_change_plot = df_change_long[df_change_long["Metric"].isin(selected_metrics)]

df_change_plot = df_change_plot.dropna(subset=["Δ Inventory"])

# Plot Production Trends
fig = px.line(df_change_plot, x="Date", y="Δ Inventory", color="Metric",
              title="Δ Inventory",
              labels={"Δ Inventory": "Δ Inventory (KT)", "Date": "Date", "Metric": "Year"})

fig.update_traces(line=dict(dash='dash'), selector=dict(name='2025 ΔS Adjusted'))

df = load_data(uploaded_file, sheet_index=2, skiprows=0, nrows=368)
df["Date"] = pd.to_datetime(df["Unnamed: 2"], format="%m-%d")
df["Date"] = df["Date"].dt.strftime("%b")
df_filtered = df.loc[:,  "Stock":"Stock (Forecast): adjusted by Supply"]
df_filtered.columns = ["2020", "2021", "2022", "2023", "2024", "2025", "2025 ΔS Adjusted"]

df_long = df_filtered.copy()
df_long["Date"] = df["Date"]  # Add Date back for plotting
df_long = df_long.melt(id_vars=["Date"], var_name="Metric", value_name="Inventory")

# Sidebar for metric selection
new_metrics = df_long["Metric"].unique().tolist()

new_selected_metrics = st.sidebar.multiselect("Select Year (Inventory)", metrics, default=new_metrics)

# Filter data based on selection
df_plot = df_long[df_long["Metric"].isin(new_selected_metrics)]

df_plot = df_plot.dropna(subset=["Inventory"])

# Plot Production Trends
ifig = px.line(df_plot, x="Date", y="Inventory", color="Metric",
              title="Inventory",
              labels={"Inventory": "Inventory (KT)", "Date": "Date", "Metric": "Year"})

ifig.update_traces(line=dict(dash='dash'), selector=dict(name='2025 ΔS Adjusted'))

st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(ifig, use_container_width=True)


