import streamlit as st
import pandas as pd
import io

DEFAULT_FILE = r"data\1、China PX Supply Demand Balance.xlsx"  # Replace with actual default file path

@st.cache_data
def load_data(file, sheet_index, skiprows, nrows):
    """Loads an Excel file and returns a DataFrame."""
    
    # 🔹 Convert file-like object to readable format
    if isinstance(file, bytes):
        file = io.BytesIO(file)  # Convert bytes to BytesIO for Pandas
    
    xls = pd.ExcelFile(file)  # Now it can read both file paths and uploaded files
    return pd.read_excel(xls, sheet_name=xls.sheet_names[sheet_index], skiprows=skiprows).head(nrows)

def handle_file_upload():
    """Manages file upload persistence across pages and uses a default file if none is uploaded."""
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
        
    with st.sidebar.expander("Choose an Excel File"):
        uploaded_file = st.sidebar.file_uploader("Choose an Excel File", type=["xlsx"])

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file

    # 🔹 Return correct file type (raw bytes for uploaded file, string path for default)
    if st.session_state.uploaded_file:
        return st.session_state.uploaded_file.getvalue()  # Convert uploaded file to bytes
    else:
        return DEFAULT_FILE  # Return the default file path
