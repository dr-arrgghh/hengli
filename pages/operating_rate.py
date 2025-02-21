import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, handle_file_upload

st.title("Plant Operating Rate")

# Handle file upload or use default
uploaded_file = handle_file_upload()

# Load data
df = load_data(uploaded_file, sheet_index=2, skiprows=0, nrows=368)
df["Date"] = pd.to_datetime(df["Unnamed: 2"], format="%m-%d")
df["Date"] = df["Date"].dt.strftime("%b")
df_filtered = df.loc[:,  "OR: CCF":"OR: Predict"][2:]
df_filtered.columns = ["2020", "2021", "2022", "2023", "2024", "2025", "2025 Estimate"]

df_long = df_filtered.copy()
df_long["Date"] = df["Date"]  # Add Date back for plotting
df_long = df_long.melt(id_vars=["Date"], var_name="Metric", value_name="Operating Rate")

metrics = df_long["Metric"].unique().tolist()

selected_metrics = st.sidebar.multiselect("Select Year", metrics, default=metrics)

# Filter data based on selection
df_plot = df_long[df_long["Metric"].isin(selected_metrics)]

df_plot = df_plot.dropna(subset=["Operating Rate"])

# Plot Production Trends
or_fig = px.line(df_plot, x="Date", y="Operating Rate", color="Metric",
              title="PX Operating Rate",
              labels={"Operating Rate": "Operating Rate (%)", "Date": "Date", "Metric": "Year"})

or_fig.update_traces(line=dict(dash='dash'), selector=dict(name='2025 Estimate'))

or_fig.update_layout(yaxis_tickformat='%')

df_by_plant = load_data(uploaded_file, sheet_index=12, skiprows=2, nrows=38)

# Reshape Data
id_vars = ["CCF Name", "Location", "Capacity (kta)"]
value_vars = df_by_plant.columns[7:]
df_by_plant_melted = df_by_plant.melt(id_vars=id_vars, var_name="Month", value_name="Operating Rate")
df_by_plant_melted["Month"] = pd.to_datetime(df_by_plant_melted["Month"], format="%Y/%m", errors="coerce")
# df_by_plant_melted["Operating Rate"] = df_by_plant_melted["Operating Rate"] * 100

# Sidebar Filter
with st.sidebar.expander("Choose an Excel File"):
    selected_plants = st.sidebar.multiselect("Select Plants", ["All"] + df_by_plant["CCF Name"].unique().tolist())

# Apply filtering
if selected_plants and "All" not in selected_plants:
    df_by_plant_melted = df_by_plant_melted[df_by_plant_melted["CCF Name"].isin(selected_plants)]

fig = px.line(df_by_plant_melted, x="Month", y="Operating Rate", color="CCF Name",
              title="PX Operating Rate By Plant",
              labels={"Month": "Time", "Operating Rate": "Operating Rate (%)"})

fig.update_layout(yaxis_tickformat='%')

st.plotly_chart(or_fig)
st.plotly_chart(fig)

# # Show data table (optional)
# st.subheader("Turnaround Data")
# st.dataframe(df_by_plant_melted)
