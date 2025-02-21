import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, handle_file_upload

st.title("PX Turnarounds")

# Handle file upload or use default
uploaded_file = handle_file_upload()

df = load_data(uploaded_file, sheet_index=2, skiprows=0, nrows=368)
df["Date"] = pd.to_datetime(df["Unnamed: 2"], format="%m-%d")
df["Date"] = df["Date"].dt.strftime("%b")
df_filtered = df.loc[:,  "TAR Capacity/month":"Import"].iloc[2:, :-1]
df_filtered.columns = ["2020", "2021", "2022", "2023", "2024", "2025"]

df_long = df_filtered.copy()
df_long["Date"] = df["Date"]  # Add Date back for plotting
df_long = df_long.melt(id_vars=["Date"], var_name="Metric", value_name="T/A Loss")

metrics = df_long["Metric"].unique().tolist()

selected_metrics = st.sidebar.multiselect("Select Year", metrics, default=metrics)

# Filter data based on selection
df_plot = df_long[df_long["Metric"].isin(selected_metrics)]

df_plot = df_plot.dropna(subset=["T/A Loss"])

# Plot Production Trends
or_fig = px.line(df_plot, x="Date", y="T/A Loss", color="Metric",
              title="T/A Loss",
              labels={"T/A Loss": "T/A Loss (KT)", "Date": "Date", "Metric": "Year"})


# Load data
df_by_plant = load_data(uploaded_file, sheet_index=11, skiprows=6, nrows=39)

# Reshape Data
id_vars = ["CCF Name", "Location", "Capacity (kta)"]
value_vars = df_by_plant.columns[7:]
df_by_plant_melted = df_by_plant.melt(id_vars=id_vars, var_name="Month", value_name="Turnaround")
df_by_plant_melted["Month"] = pd.to_datetime(df_by_plant_melted["Month"], format="%Y/%m", errors="coerce")

# Sidebar Filter
selected_plants = st.sidebar.multiselect("Select Plants", ["All"] + df_by_plant["CCF Name"].unique().tolist())

# Apply filtering
if selected_plants and "All" not in selected_plants:
    df_by_plant_melted = df_by_plant_melted[df_by_plant_melted["CCF Name"].isin(selected_plants)]

# Plot
st.subheader(f"Turnaround Trends ({', '.join(selected_plants) if selected_plants else 'All Plants'})")
fig = px.line(df_by_plant_melted, x="Month", y="Turnaround", color="CCF Name",
              title="PX Plant Turnaround",
              labels={"Month": "Time", "Turnaround": "TA (Days)"})


st.plotly_chart(or_fig)
st.plotly_chart(fig)

# # Show data table (optional)
# st.subheader("Turnaround Data")
# st.dataframe(df_by_plant_melted)
