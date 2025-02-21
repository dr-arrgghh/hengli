import streamlit as st

# --- PAGE SETUP --- #
daily_px_curves = st.Page(
    page="pages\daily_px_curves.py",
    title="Daily PX Curves",
    icon=":material/stacked_line_chart:",
)

daily_pxn_curves = st.Page(
    page="pages\daily_pxn_curves.py",
    title="Daily PXN Curves",
    icon=":material/stacked_line_chart:"
)

daily_naphtha_curves = st.Page(
    page="pages\daily_naphtha_curves.py",
    title="Daily Naphtha Curves",
    icon=":material/stacked_line_chart:"
)

operating_rate = st.Page(
    page="pages\operating_rate.py",
    title="Operating Rates",
    icon=":material/percent:",
    default=True
)

turnaround = st.Page(
    page=r"pages\turnaround.py",
    title="Turnarounds",
    icon=":material/power_settings_new:"
)

px_production = st.Page(
    page="pages\px_production.py",
    title="PX Production",
    icon=":material/precision_manufacturing:"
)

px_inventory = st.Page(
    page="pages\px_inventory.py",
    title="PX Inventory",
    icon=":material/inventory_2:"
)

# --- NAVIGATION SETUP --- #
# pg = st.navigation(pages=[daily_curves, operating_rate, turnaround])
pg = st.navigation(
    {
        "PX Fundamental Analysis": [px_inventory, px_production, operating_rate, turnaround],
        "Pricing Curves": [daily_px_curves, daily_pxn_curves, daily_naphtha_curves]
    }
)

st.sidebar.text("Made with ❤️ by Zizheng")

# --- RUN NAVIGATION --- #
pg.run()