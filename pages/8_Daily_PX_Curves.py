import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Daily PX Curves (12 Mths)")

@st.cache_data
def load_price_data():
    file_path = "data\px_curves.xlsx"
    df = pd.read_excel(file_path)
    df["Date"] = pd.to_datetime(df["Virtual Day"], format="%Y-%m-%d")
    return df

# Load the data from the default file
df_prices = load_price_data()

# Sidebar filter: Select multiple dates
available_dates = df_prices['Date'].dt.date.unique()  # Get unique dates
selected_dates = st.sidebar.multiselect("Select Dates", available_dates)

# Check if no dates are selected
if not selected_dates:
    st.warning("Please select at least one date to compare.")
else:
    # Filter data based on selected dates
    df_filtered = df_prices[df_prices['Date'].dt.date.isin(selected_dates)]

    # Ensure 'Contract' is a string and 'Price' is numeric
    df_filtered["Contract"] = df_filtered["Contract"].astype(str)
    df_filtered["Price"] = pd.to_numeric(df_filtered["Price"], errors='coerce')

    # Check for NaN values in 'Price' column and remove them if present
    if df_filtered["Price"].isnull().any():
        st.warning("There are NaN values in the price data. These will be ignored in the plot.")
        df_filtered = df_filtered.dropna(subset=["Price"])

    # Extract the month and year from 'Contract' (in the format YYYY-MM-DD)
    def extract_year_month(contract_value):
        contract_date = pd.to_datetime(contract_value)
        return contract_date.year, contract_date.month

    # Apply extraction logic to the 'Contract' column
    df_filtered['Contract Year'], df_filtered['Contract Month'] = zip(*df_filtered['Contract'].apply(extract_year_month))

    selected_year = selected_dates[0].year
    selected_month = selected_dates[0].month

    # Remove contracts that are before the selected month in the selected year
    df_filtered = df_filtered[~((df_filtered['Contract Year'] == selected_year) & (df_filtered['Contract Month'] <= selected_month))]

    # Add a new column 'Date Label' for each selected date to avoid the lines connecting across dates
    df_filtered['Date Label'] = df_filtered['Date'].dt.date.astype(str)

    # Plot daily prices for the selected dates and contract months (Jan-Dec)
    st.subheader(f"Price Curves for selected dates: {selected_dates}")
    fig = px.line(df_filtered, x="Contract", y="Price", color="Date Label",
                  title=f"Price Changes for selected dates: {selected_dates}",
                  labels={"Contract": "Contract Month (Jan-Dec)", "Price": "Price ($)", "Date Label": "Selected Date"})

    # Show the plot
    st.plotly_chart(fig)

    # Show the filtered data in a table
    st.subheader("Price Data")
    st.dataframe(df_filtered)