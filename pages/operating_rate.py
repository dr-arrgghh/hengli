import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, handle_file_upload

st.title("Plant Operating Rate")

# Handle file upload or use default
uploaded_file = handle_file_upload()

# Load data
df = load_data(uploaded_file, sheet_index=12, skiprows=2, nrows=38)

# Reshape Data
id_vars = ["CCF Name", "Location", "Capacity (kta)"]
value_vars = df.columns[7:]
df_melted = df.melt(id_vars=id_vars, var_name="Month", value_name="Operating Rate")
df_melted["Month"] = pd.to_datetime(df_melted["Month"], format="%Y/%m", errors="coerce")
# df_melted["Operating Rate"] = df_melted["Operating Rate"] * 100

# Sidebar Filter
selected_plants = st.sidebar.multiselect("Select Plants", ["All"] + df["CCF Name"].unique().tolist())

# Apply filtering
if selected_plants and "All" not in selected_plants:
    df_melted = df_melted[df_melted["CCF Name"].isin(selected_plants)]

# Plot
st.subheader(f"Turnaround Trends ({', '.join(selected_plants) if selected_plants else 'All Plants'})")
fig = px.line(df_melted, x="Month", y="Operating Rate", color="CCF Name",
              title="PX Plant Turnaround Over Time",
              labels={"Month": "Time", "Operating Rate": "Operating Rate (%)"})

fig.update_layout(yaxis_tickformat='%')

st.plotly_chart(fig)

# # Show data table (optional)
# st.subheader("Turnaround Data")
# st.dataframe(df_melted)
