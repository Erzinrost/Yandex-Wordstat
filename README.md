# Yandex Wordstat Automated Keyword Data Downloader

*Workable as of February 2025*

This project is a Streamlit-based web application that automates the process of downloading keyword data from [**Yandex Wordstat**](https://wordstat.yandex.ru/), a popular keyword research tool. The application allows users to upload an Excel file containing keywords, enter their Yandex login credentials, and automatically fetch keyword statistics for specified regions (e.g., Moscow and Saint Petersburg). The results are then made available for download as a CSV file. Overall, this project is designed to simplify the process of fetching keyword data from Yandex Wordstat, making it easier for marketers, SEO specialists, and researchers to gather insights into keyword trends across different regions (in the current version only Moscow, Saint Petersburg and their respective regions are available).

Wordstat provides data on the number of searches by Yandex users using various keywords over time and across regions. Thus, these figures may be a good proxy for potential market demand, customer interest or some marketing trends. Therefore it is an important tool for marketers, market researchers and businesses in general. However, the problem is that it is not possible to assess the market sentiment in any particular niche with just a few keywords, hence many of them should be considered. For that purpose keyword download automation comes in quite handy, especially if the related semantics are particularly large. Thus, this program has been developed to help with keywords sequential download automation.

## Features

- **Excel File Upload**: Users can upload an Excel file containing keywords in specific sheets (e.g., `MSK` for Moscow and `SPB` for Saint Petersburg).
- **Automated Keyword Processing**: The application uses **Selenium** to automate the process of logging into Yandex Wordstat, selecting regions, and fetching keyword statistics.
- **Dynamic Region Selection**: The application supports dynamic region selection for Moscow and Saint Petersburg, including their respective surrounding regions.
- **Real-Time Logging**: A custom logger displays the last 10 log messages in a scrollable window, providing real-time feedback on the script's progress.
- **Downloadable Results**: The fetched keyword data is compiled into a CSV file, which users can download directly from the app.
- **Cloud Deployment Ready**: The application is designed to work both locally and on cloud platforms like Streamlit Cloud, with options to handle different environments. Nonetheless, due to technical constrains cloud deployment is prone to bugs and unpredicted behaviour, therefore local usage is recommended.

## How It Works

1. **Upload Excel File**: Users upload an Excel file containing keywords in specific sheets (`MSK` for Moscow and region and `SPB` for Saint Petersburg and region). The Excel file should contain two sheets:
**MSK**: Keywords for Moscow and its region;
**SPB**: Keywords for Saint Petersburg and its region.
Each sheet should have keywords listed in the first column without headers.
3. **Enter Login Credentials**: Users provide their Yandex login credentials to access Wordstat. In the case of additonal login checks you may enter them manually in the automated Chrome window controlled by Selenium.
4. **Select Deployment Environment**: Users can specify whether the app is running locally or on the Streamlit Cloud. In the latter case deployment may be problematic because:
   - Yandex has strict control for their services automation and when loggign in additional checks (e.g. push codes, CAPTCHA) may be required;
   - No manual control over automation is possible in the case of interface changes or other unpredicted scenarios.
5. **Check "Deployed on cloud" checkbox**: Check this one if you are trying to run the app on Streamlit Cloud - in that case Chromium instead of Chrome is used, and you have to [deploy it yourself](https://share.streamlit.io/).
6. **Start Processing**: The application uses Selenium to automate the process of logging into Yandex Wordstat, selecting regions, and fetching keyword statistics. The latter is taken directly from the source code, but it is also possible to adjust the code slightly to download files for each keyword and then concatenate them together without the need for webscrapping.
7. **Download Results**: Once the processing is complete, users can download the results as a CSV file.

## Code Structure

- **`script.py`**: Contains the core logic for setting up the Selenium browser, logging into Yandex Wordstat, processing keywords, and fetching data for specified regions.
  - **Browser Setup**: Configures the Chrome browser with appropriate options for headless or cloud deployment.
  - **Login Functionality**: Handles the login process to Yandex Wordstat.
  - **Keyword Processing**: Processes keywords for specified regions and fetches data dynamically.
  - **Timer and Banner Handling**: Includes decorators for timing functions and handling pop-up banners on the Wordstat website.

- **`app.py`**: The Streamlit-based web application that provides a user interface for uploading files, entering credentials, and starting the keyword processing.
  - **File Upload**: Allows users to upload an Excel file with keywords.
  - **Real-Time Logging**: Displays the last 10 log messages in a scrollable window.
  - **Download Button**: Provides a button to download the processed data as a CSV file.

## Requirements

- Python 3.8+
- Streamlit
- Selenium
- Pandas
- Openpyxl (for Excel file processing)
- Webdriver Manager (for managing ChromeDriver)

## Installation

Simply the the following commands one by one in your terminal:

1. Clone the repository:
   ```bash
   git clone https://github.com/Erzinrost/Yandex-Wordstat.git
   cd Yandex-Wordstat
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

- Open the app in your browser (usually at http://localhost:8501).
- Upload an Excel file with keywords in the MSK and SPB sheets.
- Enter your Yandex login credentials.
- Select whether the app is running locally or on the cloud.
- Click "Start Processing" to begin fetching keyword data.
- Once processing is complete, download the results as a CSV file.


## Contributing

This project is not maintained on a constant basis, but rather used and upgraded when there is practical need.
Nonetheless, contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
