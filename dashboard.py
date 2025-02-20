import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import math

st.title("S&D Balance")

# @st.cache_data
# def load_data(file):
#     xls = pd.ExcelFile(file)  # Load the Excel file
#     # st.write("Available sheets:", xls.sheet_names)  # Display available sheets
#     df = pd.read_excel(xls, sheet_name=xls.sheet_names[12], skiprows=2).head(42)
#     # st.write(df.head())  # Use the first sheet
#     return df


# st.sidebar.title("Upload Operating Rate Data")
# uploaded_file = st.sidebar.file_uploader("Choose an Excel File", type=["xlsx"])

# if uploaded_file:
#     df = load_data(uploaded_file)

#     # Keep relevant columns (assuming first columns are 'CCF Name', 'Location', 'Capacity')
#     id_vars = ["CCF Name", "Location", "Capacity (kta)"]
#     value_vars = df.columns[3:]  # Assuming month columns start from 4th column

#     # Reshape Data (Convert Monthly Columns into Rows)
#     df_melted = df.melt(id_vars=id_vars, var_name="Month", value_name="Operating Rate")

#     # Convert "Month" Column to Datetime
#     df_melted["Month"] = pd.to_datetime(df_melted["Month"], format="%Y/%m", errors="coerce")

#     df_melted["Operating Rate"] = df_melted["Operating Rate"] * 100

#     # Sidebar Filter: Select Plant
#     selected_plants = st.sidebar.multiselect("Select Plants", ["All"] + df["CCF Name"].unique().tolist())

#     # Filter Data Based on Selection
#     if selected_plants and "All" not in selected_plants:
#         df_melted = df_melted[df_melted["CCF Name"].isin(selected_plants)]

#     # Line Chart for Operating Rates
#     st.subheader(f"Operating Rate Trends ({', '.join(selected_plants) if selected_plants else 'All Plants'})")
#     fig = px.line(df_melted, x="Month", y="Operating Rate", color="CCF Name",
#                   title="PX Plant Operating Rates Over Time",
#                   labels={"Month": "Time", "Operating Rate": "Operating Rate (%)"})

#     # Customize y-axis to display percentage
#     fig.update_layout(yaxis_tickformat='%')

#     # Show Chart
#     st.plotly_chart(fig)

#     # Show Data Table
#     st.subheader("Operating Rate Data")
#     st.dataframe(df_melted)

# else:
#     st.info("Upload an Excel file to visualize operating rates.")
