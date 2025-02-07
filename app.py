import streamlit as st
import os
import pandas as pd
import sys
from collections import deque
from script import main  # Import the main function from your existing script

class StreamlitLogger:
    """Custom Streamlit logger to display the last 15 print statements in a scrollable window."""
    def __init__(self):
        self.log_lines = deque(maxlen=15)  # Store only the last 15 lines
        self.output_container = st.empty()
        self.show_output = True  # Default to showing output

    def write(self, message):
        if message.strip():  # Avoid empty lines
            self.log_lines.append(message)
            if self.show_output:
                self.output_container.text_area("Log Output:", "\n".join(self.log_lines), height=250)

    def flush(self):
        pass  # Required for compatibility with sys.stdout

    def toggle_output(self, show):
        self.show_output = show
        if not show:
            self.output_container.empty()
        else:
            self.output_container.text_area("Log Output:", "\n".join(self.log_lines), height=250)

def process_keywords_from_xlsx(file):
    """Read and process keywords from an uploaded Excel file without headers."""
    try:
        xls = pd.ExcelFile(file, engine='openpyxl')
        return xls
    except Exception as e:
        st.error(f"Error processing the file: {e}")
        return None

# Streamlit UI
st.title("\U0001F4C2 Upload Excel File and Start Automated Keywords Download")

uploaded_file = st.file_uploader("Upload an XLSX file with keywords", type=["xlsx"])

if uploaded_file:
    df = process_keywords_from_xlsx(uploaded_file)
    
    if df:
        st.success("File uploaded successfully!")
        st.subheader("\U0001F4C4 Detected Sheets")
        
        # Display available sheets
        for i, sheet in enumerate(df.sheet_names, start=1):
            st.write(f"**Sheet #{i}: {sheet}**")
        
        # Select a sheet to display contents
        selected_sheet = st.selectbox("Select a sheet to view contents:", df.sheet_names)
        if selected_sheet:
            sheet_data = df.parse(selected_sheet, header=None)
            sheet_data = sheet_data.rename(columns={0: 'Keyword'})  # Rename first column
            st.dataframe(sheet_data.head(5))
            
        # Read keywords from two specific sheets if they exist
        keys_msk = []
        keys_spb = []
        if 'MSK' in df.sheet_names and not df.parse('MSK', header=None).empty:
            keys_msk = df.parse('MSK', header=None).iloc[:, 0].dropna().tolist()
        
        if 'SPB' in df.sheet_names and not df.parse('SPB', header=None).empty:
            keys_spb = df.parse('SPB', header=None).iloc[:, 0].dropna().tolist()
        
        # Log detected keywords count
        st.write(f"Detected {len(keys_msk)} keywords in MSK sheet.")
        st.write(f"Detected {len(keys_spb)} keywords in SPB sheet.")
        
        logger = StreamlitLogger()
        
        if st.button("Start Processing"):
            st.write("Running script...")
            sys.stdout = logger  # Redirect print statements
            main(keys_msk, keys_spb)  # Call the main function from the existing script
            st.success("Processing completed!")
