import streamlit as st
import os
import pandas as pd
import sys
from collections import deque
from script import main  # Import the main function from your existing script

class StreamlitLogger:
    """Custom Streamlit logger to display the last 15 print statements in a scrollable window."""
    def __init__(self):
        self.log_lines = deque(maxlen=10)  # Store only the last 15 lines
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
st.title("📂 Upload Excel File and Start Automated Keywords Download")

# Create tabs for file upload and login credentials
tab1, tab2 = st.tabs(["Upload File", "Login Credentials"])

# Make buttons inactive during script execution
if 'run_button' in st.session_state and st.session_state.run_button == True:
    st.session_state.running = True
else:
    st.session_state.running = False

with tab1:
    uploaded_file = st.file_uploader("Upload an XLSX file with keywords", type=["xlsx"])

with tab2:
    st.subheader("🔐 Enter Login Credentials")
    login = st.text_input("Login", placeholder="Enter your login")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

if uploaded_file:
    df = process_keywords_from_xlsx(uploaded_file)
    
    if df:
        st.success("✅ File uploaded successfully!")
        st.subheader("📄 Detected Sheets")
        
        # Display available sheets
        for i, sheet in enumerate(df.sheet_names, start=1):
            st.write(f"**Sheet #{i}: {sheet}**")
        
        # Select a sheet to display contents
        selected_sheet = st.selectbox("Select a sheet to view contents:", df.sheet_names, disabled=st.session_state.running)
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

        if login and password and df:
            # Checkbox widget
            on_cloud = st.checkbox("Deployed on cloud?", disabled=st.session_state.running)
            if st.button(label="Start Processing", disabled=st.session_state.running, key='run_button'):
                st.write("Running script...")
                sys.stdout = logger  # Redirect print statements
                main(keys_msk, keys_spb, login, password, on_cloud)  # Pass the login and password to your script
                st.success("🚀 Processing completed! Click ↖️ to get your data")
        else:
            st.subheader("⚠️ Upload keywords in required format and enter login and password before running the script")

        # Initialize session state
        if 'download_click' not in st.session_state:
            st.session_state.download_click = False
            # Check if download was clicked
        if st.session_state.download_click:
            # Perform actions or display information without resetting the app state
            st.success("✅ Download complete!")