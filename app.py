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

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to a temporary directory."""
    save_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

def process_keywords_from_xlsx(file_path):
    """Read and process keywords from an uploaded Excel file without headers."""
    try:
        df = pd.ExcelFile(file_path)
        return df
    except Exception as e:
        st.error("Error processing the file. Ensure it is a valid XLSX file.")
        return None

# Streamlit UI
st.title("📂 Upload Excel File and Start Keywords Download Automation")

uploaded_file = st.file_uploader("Upload an XLSX file with keywords", type=["xlsx"])

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    df = process_keywords_from_xlsx(file_path)
    
    if df:
        st.success("File uploaded successfully!")
        st.subheader("📄 Detected Sheets")
        
        # Display sheets in a more readable format
        for i, sheet in enumerate(df.sheet_names, start=1):
            st.write(f"**Sheet #{i}: {sheet}**")
        
        # Option to display sheet contents without headers
        selected_sheet = st.selectbox("Select a sheet to view contents:", df.sheet_names)
        if selected_sheet:
            st.dataframe(df.parse(selected_sheet, header=None).rename(columns={0: 'Keyword'}).head(5))
    
    logger = StreamlitLogger()  # Create an instance of the logger
    
    if st.button("Start Processing"):
        st.write("Running script...")
        
        # Redirect print statements to be displayed below the button
        sys.stdout = logger
        
        main()  # Calls the main function from the existing script
        
        st.success("Processing completed!")
