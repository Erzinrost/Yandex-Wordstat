# Yandexx Wordstat Automated Keyword Data Downloader

Workable as of February 2025

This project is a Streamlit-based web application that automates the process of downloading keyword data from [**Yandex Wordstat**](https://wordstat.yandex.ru/), a popular keyword research tool. The application allows users to upload an Excel file containing keywords, enter their Yandex login credentials, and automatically fetch keyword statistics for specified regions (e.g., Moscow and Saint Petersburg). The results are then made available for download as a CSV file.

Wordstat provides data on the number of searches by Yandex users using various keywords over time and across regions. Thus, these figures may be a good proxy for potential market demand, customer interest or some marketing trends. Therefore it is an important tool for marketers, market researchers and businesses in general. However, the problem is that it is not possible to assess the market sentiment in any particular niche with just a few keywords, hence many of them should be considered. For that purpose keyword download automation comes in quite handy, especially if the related semantics are particularly large. Thus, this program has been developed to help with keywords sequential download automation.

## Features

- **Excel File Upload**: Users can upload an Excel file containing keywords in specific sheets (e.g., `MSK` for Moscow and `SPB` for Saint Petersburg).
- **Automated Keyword Processing**: The application uses **Selenium** to automate the process of logging into Yandex Wordstat, selecting regions, and fetching keyword statistics.
- **Dynamic Region Selection**: The application supports dynamic region selection for Moscow and Saint Petersburg, including their respective surrounding regions.
- **Real-Time Logging**: A custom logger displays the last 10 log messages in a scrollable window, providing real-time feedback on the script's progress.
- **Downloadable Results**: The fetched keyword data is compiled into a CSV file, which users can download directly from the app.
- **Cloud Deployment Ready**: The application is designed to work both locally and on cloud platforms like Streamlit Cloud, with options to handle different environments.

## How It Works

1. **Upload Excel File**: Users upload an Excel file containing keywords in specific sheets (`MSK` for Moscow and `SPB` for Saint Petersburg).
2. **Enter Login Credentials**: Users provide their Yandex login credentials to access Wordstat.
3. **Select Deployment Environment**: Users can specify whether the app is running locally or on the cloud.
4. **Start Processing**: The application uses Selenium to automate the process of logging into Yandex Wordstat, selecting regions, and fetching keyword statistics.
5. **Download Results**: Once the processing is complete, users can download the results as a CSV file.

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

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/automated-keyword-downloader.git
   cd automated-keyword-downloader
