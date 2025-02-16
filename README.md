# Yandex Wordstat Automated Keyword Data Downloader

🚀 **Last Tested: February 2025**

This **Streamlit-based web application** automates the process of downloading keyword data from [**Yandex Wordstat**](https://wordstat.yandex.ru/), a widely used keyword research tool. 

## 🔍 Overview

The application allows users to:

- Upload an **Excel file** containing keywords.
- Enter **Yandex login credentials**.
- Fetch keyword statistics for specific regions (**Moscow, Saint Petersburg, and surrounding areas**).
- Download the processed data as a **CSV file**.

This tool simplifies keyword data extraction for **SEO specialists, marketers, and researchers**, making it easier to analyze search trends.

⚠️ **Note:** Due to Yandex’s restrictions, automation may trigger additional verification steps (e.g., CAPTCHA, push codes). Local execution is recommended for manual intervention.

## ✨ Features

✅ **Excel File Upload** – Supports Excel files with keywords organized by region (`MSK` for Moscow, `SPB` for Saint Petersburg).  
✅ **Automated Keyword Processing** – Uses **Selenium** to log in, select regions, and retrieve keyword statistics.  
✅ **Dynamic Region Selection** – Fetch data for **Moscow, Saint Petersburg, and their surrounding areas**.  
✅ **Real-Time Logging** – Displays the last **10 log messages** in a scrollable UI.  
✅ **Downloadable Results** – Processed data is saved as a **CSV file** for easy analysis.  
✅ **Cloud Deployment Support** – Can run on **Streamlit Cloud**, though local usage is recommended due to automation constraints.

## 🛠 How It Works

1. **Upload an Excel file** (`.xlsx`) containing keywords:
   - `MSK` sheet → Keywords for **Moscow and its region**.
   - `SPB` sheet → Keywords for **Saint Petersburg and its region**.
   - Keywords should be listed in the **first column** without headers.
   
2. **Enter your Yandex login credentials** in the UI. If additional verification is required (e.g., CAPTCHA), complete it manually in the Selenium-controlled Chrome window.

3. **Select the deployment environment**:
   - Running **locally** → Recommended for better control.
   - Running **on the cloud** → Check the `"Deployed on cloud"` option (Chromium is used instead of Chrome).

4. **Start Processing**:
   - The script logs in, selects the appropriate region, and retrieves keyword statistics.
   - The data is **extracted from the source code**, but the script can be modified to download Wordstat files directly.

5. **Download Results**:
   - Once processing is complete, download the keyword data as a **CSV file**.

## 📂 Code Structure

### `script.py`
- **Browser Setup** – Configures **Selenium** for local or cloud execution.
- **Login Handling** – Automates login to **Yandex Wordstat**.
- **Keyword Processing** – Sequentially retrieves search statistics.
- **Region Selection** – Dynamically selects **Moscow** or **Saint Petersburg**.

### `app.py`
- **Streamlit UI** – Handles **file uploads, credential input, and process execution**.
- **Logging** – Displays the last **10 log messages** in real time.
- **Download Functionality** – Provides a **CSV download button**.

## ⚙️ Requirements

Ensure you have **Python 3.8+** installed.

Install dependencies using:

```bash
pip install -r requirements.txt
```

### Dependencies:
- **Streamlit** (for UI)
- **Selenium** (for browser automation)
- **Pandas** (for data processing)
- **Openpyxl** (for Excel file handling)
- **Webdriver Manager** (for ChromeDriver management)

## 🚀 Installation & Usage
Write the following commands one after another in your terminal:

1.  **Clone the repository**:
   ```
   git clone https://github.com/Erzinrost/Yandex-Wordstat.git
   ```
   ```
   cd Yandex-Wordstat
   ```

2.  **Install dependencies**:

   ```
    pip install -r requirements.txt
   ```

3.  **Run the application**:

    ```
    streamlit run app.py
    ```

5.  **Use the UI**:

    -   Upload your Excel file (`.xlsx`).
    -   Enter Yandex login credentials.
    -   Choose execution mode (local/cloud).
    -   Click **"Start Processing"**.
    -   Download the **CSV file** once processing is complete.

## ⚠️ Known Limitations & Vulnerabilities

1.  **UI Changes on Yandex Wordstat**

    -   The script relies on **XPaths** for automation, which can break if the UI changes.
    -   Alternative locators exist in the code for easy updates.
2.  **Frequent Logins May Trigger Verification**

    -   Repeated logins can prompt **CAPTCHA or push notifications**.
    -   On **local execution**, manual login intervention is possible.
3.  **Cloud Deployment Risks**

    -   No manual control in case of interface changes.
    -   CAPTCHA verification **cannot** be bypassed automatically.

* * * * *

🤝 Contributing

This project is **updated as needed** rather than actively maintained.\
However, **contributions are welcome**! Feel free to submit a **pull request** or report issues.
