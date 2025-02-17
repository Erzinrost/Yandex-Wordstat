**Yandex Wordstat Automated Keyword Data Downloader**
=====================================================

***Functional as of February 2025***

This project is a **Streamlit-based web application** that automates the process of downloading keyword data from [**Yandex Wordstat**](https://wordstat.yandex.ru/), a popular keyword research tool.

The application allows users to:\
✅ Upload an **Excel file** containing keywords\
✅ Enter their **Yandex login credentials**\
✅ **Automatically fetch** keyword statistics for specific regions (**Moscow & Saint Petersburg**)\
✅ **Download the results** as a CSV file

This tool is particularly useful for **marketers, SEO specialists, and researchers**, simplifying the process of retrieving **keyword trends and search volume data** from Yandex Wordstat.

### 📌 **Why Use This Tool?**

Yandex Wordstat provides **search volume data** based on user queries, helping businesses assess **market demand, customer interest, and marketing trends**. However, analyzing **a single keyword is not enough**---gathering insights across multiple keywords is crucial.

Since manually retrieving large keyword datasets is **time-consuming**, this project was developed to **automate and streamline** the process, especially when handling **large keyword lists**.

* * * * *

🚀 **Features**
---------------

🔹 **Excel File Upload** -- Upload an Excel file with keywords categorized into specific sheets (`MSK` for Moscow and `SPB` for Saint Petersburg).\
🔹 **Automated Keyword Retrieval** -- Uses **Selenium** to log into Yandex Wordstat, select regions, and fetch keyword statistics.\
🔹 **Dynamic Region Selection** -- Supports Moscow & Saint Petersburg, including their **respective surrounding regions**.\
🔹 **Real-Time Logging** -- Displays the **last 10 log messages** in a scrollable interface for **live status updates**.\
🔹 **Downloadable Results** -- Saves the fetched keyword data as a **CSV file** for easy access.\
🔹 **Local & Cloud Deployment** -- Designed to work **locally** or on **Streamlit Cloud**, but due to Yandex's security measures, local use is recommended.

* * * * *

🛠 **How It Works**
-------------------

### **1️⃣ Upload an Excel File**

-   The Excel file must contain **two sheets**:
    -   **MSK** → Keywords for **Moscow & its region**
    -   **SPB** → Keywords for **Saint Petersburg & its region**
-   Each sheet should have **keywords listed in the first column** (no headers required).

### **2️⃣ Enter Yandex Login Credentials**

-   Provide your **Yandex username & password** to access Wordstat.
-   If additional login verification (e.g., CAPTCHA, push codes) is required, you can **manually enter** them in the automated **Chrome window** controlled by Selenium.

### **3️⃣ Choose Deployment Environment**

-   Select whether the app is running **locally** or on **Streamlit Cloud**.
-   If using **Streamlit Cloud**, be aware of potential issues:
    -   Yandex may require **manual verification** (CAPTCHA, push codes).
    -   No manual control over **unexpected UI changes**.

### **4️⃣ Run the Processing**

-   The script will **log into Yandex Wordstat**, select the specified regions, and fetch **keyword search volume data**.
-   The data is extracted **directly from the page source** to **minimize web scraping risks**.

### **5️⃣ Download the Results**

-   Once the process is complete, **download** the keyword data as a **CSV file**.

* * * * *

🏗 **Code Structure**
---------------------

📂 **`script.py`** -- Core logic for Selenium automation

-   **Browser Setup** -- Configures Chrome for **local or cloud deployment**
-   **Login Handling** -- Automates login to Yandex Wordstat
-   **Keyword Processing** -- Fetches data for selected regions
-   **Timer & Banner Handling** -- Manages UI pop-ups & delays

📂 **`app.py`** -- Streamlit-based UI

-   **File Upload** -- Handles Excel file input
-   **Real-Time Logging** -- Displays script progress
-   **Download Button** -- Provides the CSV download option

* * * * *

📌 **Installation**
-------------------

Run the following commands one after another in your terminal:

### **1️⃣ Clone the Repository and Set Directory**
```
git clone https://github.com/Erzinrost/Yandex-Wordstat.git
```
```
cd Yandex-Wordstat
```
### **2️⃣ Install Dependencies**
```
pip install -r requirements.txt
```
### **3️⃣ Run the Streamlit App**
```
python -m streamlit run app.py 
```
* * * * *

📖 **Usage Instructions**
-------------------------

1️⃣ Open **terminal** and run the commands above.\
2️⃣ Upload an **Excel file** containing keywords in **MSK & SPB sheets**.\
3️⃣ Enter your **Yandex login credentials**.\
4️⃣ Select whether the app is running **locally or on Streamlit Cloud**.\
5️⃣ Click **"Start Processing"** to begin fetching keyword data.\
6️⃣ Once completed, **download the results** as a **CSV file**.

* * * * *

🔧 **Requirements**
-------------------

📌 Python **3.8+**\
📌 **Selenium**\
📌 **Streamlit**\
📌 **Pandas**\
📌 **Openpyxl** (for Excel file processing)\
📌 **Webdriver Manager** (for ChromeDriver management)

* * * * *

⚠️ **Potential Issues & Vulnerabilities**
-----------------------------------------

1️⃣ **Yandex UI Changes**

-   The script relies on **XPath locators**, which may **change over time**.
-   However, alternative locators are included in the code, making updates **straightforward**.

2️⃣ **Frequent Logins & Security Checks**

-   Logging into Yandex **too frequently** may trigger **CAPTCHA or push-code verification**.
-   **Local execution is recommended**, as **manual input** is possible if needed.

* * * * *

🤝 **Contributing**
-------------------

This project is **not actively maintained** but is updated **as needed**.\
Feel free to **open an issue** or **submit a pull request** for improvements or bug fixes.

* * * * *

📌 **Notes:**
-------------------

-   **Cloud deployment is not fully reliable** due to Yandex's security measures and lack of manual control.
-   **Local execution is thus recommended** with opened Chrone window automated by Selenium for **better control & stability**.
