import os
import ssl
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from functools import wraps
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import streamlit as st
from webdriver_manager.core.os_manager import ChromeType

# Ensure SSL is properly loaded in case of any environment-specific issues
ssl._create_default_https_context = ssl._create_unverified_context

# Constants
# directory = os.path.expanduser("~/downloads/") # in case you want to download each file instead of parsing from the source code
# directory_processed = directory + "Wordstat/"
# os.makedirs(directory_processed, exist_ok=True)
login_url = "https://wordstat.yandex.ru/"
default_wait = 15
sleep_time = 3
global_inception_time = time.time()

def timer(func):
    """Calculate time taken by a function to execute and also time elapsed since the session's inception"""
    def wrapper(*args, **kwargs):

        # Record the start time and declare the time since the inception of the session
        global global_inception_time
        start_time = time.time()
        
        # Call the function
        result = func(*args, **kwargs)
        
        # Record the end time
        end_time = time.time()
        
        # Calculate the total time passed since the start of the session and taken by a function
        time_taken_globally = end_time - global_inception_time
        time_taken = end_time - start_time
        
        # Convert time_taken into hours, minutes, and seconds
        hours_global = int(time_taken_globally // 3600)
        minutes_global = int((time_taken_globally % 3600) // 60)
        seconds_global = int(time_taken_globally % 60)
        hours = int(time_taken // 3600)
        minutes = int((time_taken % 3600) // 60)
        seconds = int(time_taken % 60)
        
        # count time elapsed in hours, minutes, and seconds
        if str(func.__name__) == "process_keyword":
            print(f"Time elapsed: {hours_global} hours, {minutes_global} minutes, and {seconds_global} seconds.")
        else:
            print(f"Function '{func.__name__}' took {hours} hours, {minutes} minutes, and {seconds} seconds to run.")
        
        return result
    
    return wrapper

def close_banner(func):
    """Decorator to close the popping banner before executing the function
    which clicks through Wordstat webpage."""
    @wraps(func)  # This preserves the original function's metadata (e.g., name, docstring)
    def wrapper(browser, *args, **kwargs):
        """Wrapper function to close the banner if not already closed."""
        # Different ways to click the close button
        xpaths = [
            """//*[@id="page"]/div/div[2]/div/div[3]/div[1]/button[1]""",
            """//*[@id="page"]/div/div[2]/div/div[3]/div[1]/button[1]/span"""
        ]
        # Execute function if there is no banner
        try:
            time.sleep(sleep_time)
            return func(browser, *args, **kwargs)
        # Otherwise try to close banner, which doesn't allow the function to run
        except Exception as e:
            for attempt, xpath in enumerate(xpaths, start=1):
                try:
                    WebDriverWait(browser, default_wait).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    ).click()
                    print(f"Banner closed")
                    break  # Stop after successfully closing the banner
                except Exception as e:
                    print(f"Attempt {attempt} failed to close banner with xpath: {xpath}")
            
            # Execute the original function after closing the banner
            return func(browser, *args, **kwargs)
    
    return wrapper

def setup_browser(on_cloud):
    """Setup Chrome browser for Selenium on Streamlit Cloud."""

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-Advertisement")
    options.add_argument("--disable-popup-blocking") 
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled") # Avoid detection as bot
    #options.add_argument("--headless") # if no interaction Chrome window needed
    #options.add_argument("--user-data-dir=/Users/mac/Library/Application Support/Google/Chrome/Default") # if you know path to your Chrome cookies
    #options.add_argument("--profile-directory=Default") # use Chrome already logged in Yandex

    # Use Chromium if deploying app on Streamlit cloud
    if on_cloud:
        try:
            def get_driver():
                options.add_argument("--headless")
                return webdriver.Chrome(
                    service=Service(
                        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                    ),
                    options=options,
                )
            browser = get_driver()
            print('App is deployed on cloud')
        except: 
            service = Service(ChromeDriverManager().install())
            browser = webdriver.Chrome(service=service, options=options)
            print('App is not deployed on cloud but locally')
    # Or usual Chrome otherwise
    else:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
        print('App is deployed locally')


    # Enter a word to start session
    time.sleep(sleep_time)
    browser.get(login_url)
    WebDriverWait(browser, default_wait).until(
        EC.presence_of_element_located((By.CLASS_NAME, "textinput__control"))
    ).send_keys("Start session")
    WebDriverWait(browser, default_wait).until(
        EC.presence_of_element_located((By.CLASS_NAME, "textinput__control"))
    ).send_keys(Keys.ENTER)

    return browser

def login_to_wordstat(browser, login, password):
    """Logs into Wordstat."""

    try:
        # Enter login and password
        browser.find_element(By.CLASS_NAME, 'Textinput-Control').send_keys(login)
        time.sleep(sleep_time)
        browser.find_element(By.CLASS_NAME, 'Textinput-Control').send_keys(Keys.ENTER)
        time.sleep(sleep_time)
        print("Login entered")
        browser.find_element(By.CLASS_NAME, 'Textinput-Control').send_keys(password)
        time.sleep(sleep_time)
        browser.find_element(By.CLASS_NAME, 'Textinput-Control').send_keys(Keys.ENTER)
        time.sleep(sleep_time)
        print("Password entered")
        try:
            browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[2]/div/ul/li/div/a/div/div/div[2]"""))))
            print("Account selection confirmed")
        except Exception as e:
            pass
    except Exception as e:
        print("Login failed. Please check credentials or website accessibility.", e)
        browser.quit()

def get_latest_file(directory, prefix="wordstat_dynamic"):
    """Uploads the latest file with the specified prefix from a directory
    and then deletes that source file."""
    files = [f for f in os.listdir(directory) if f.startswith(prefix)]
    if not files:
        print("No files found with prefix", prefix)
        return None
    files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
    latest_file = os.path.join(directory, files[0])
    try:
        df = pd.read_csv(latest_file, delimiter=';')
        os.remove(latest_file)
        return df
    except Exception as e:
        print("Error reading or deleting the source file")
        return None

@close_banner
@timer
def process_keyword(browser, keyword):
    """Process a single keyword for a specified region."""
    # Actions to perform
    actions = {
        "Clear input": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="page"]/div/div[2]/div/div[2]/span/span[2]""")))),
        "Write keyword": lambda: WebDriverWait(browser, default_wait).until(EC.presence_of_element_located((By.CLASS_NAME, 'textinput__control'))).send_keys(keyword.strip()),
        "Enter keyword": lambda: WebDriverWait(browser, default_wait).until(EC.presence_of_element_located((By.CLASS_NAME, 'textinput__control'))).send_keys(Keys.ENTER)
    }

    # Enter the keyword to obtain results or pass in case of no data
    try:
        print(f"Processing keyword: '{keyword}'")
        for key in actions.keys():
            actions[key]()

        df = {
            'Период': [],
            'Число запросов': [],
            'Доля от всех запросов, %': []
        }
        time.sleep(10)
        elements = browser.find_elements(By.CLASS_NAME, 'table__content-cell')
        for element in elements:
            df['Период'].append(element.text)
        elements = browser.find_elements(By.CLASS_NAME, 'table__level-cell')
        for i, element in enumerate(elements, start=1):
            if i % 2 != 0:
                df['Число запросов'].append(element.text.strip().replace(" ", ""))
            else:
                df['Доля от всех запросов, %'].append(element.text.strip().replace(" ", ""))
        df = pd.DataFrame(df)

        return df

    except Exception as e:
        print("No data to download")

@close_banner
@timer
def process_region(browser, keywords, region_actions, region_actions_alternative, region_name):

    """Processes all keywords for a specified region."""

    print(f"Processing region: '{region_name}'")

    for key in region_actions.keys():
        try:
            region_actions[key]()
            time.sleep(sleep_time)
            print(key)
        except Exception as e:
            region_actions_alternative[key]()
            print(key, "- used alternative way to click")

    region_data = pd.DataFrame()
    for i, key in enumerate(keywords):
        df = process_keyword(browser, key)
        if df is not None:
            df = df[list(df.dropna(axis=1, how='all').columns)]
            df['Ключ'] = key
            region_data = pd.concat([region_data, df], axis=0)
            print(f"{round((i + 1) / len(keywords) * 100, 2)}% completed for {region_name}")
    
    region_data['Регион'] = region_name
    return region_data

def main(keys_msk, keys_spb, login, password, on_cloud):
    browser = setup_browser(on_cloud)
    time.sleep(sleep_time)

    #Check if login manually or atomatically (i.e. using Chrome with cookies)
    if login and password:
        login_to_wordstat(browser, login, password)
    else:
        pass

    time.sleep(sleep_time)
    region_1 = "Moscow and region"
    # Define actions to chosee region
    msk_actions = {
        "Select region": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH,"""//*[@id="page"]/div/div[2]/div/div[3]/div[1]/div/div[1]/div[2]/div/button/span[2]""")))),
        "Cancel selection": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH,"""//*[@id="123"]/ol/li/span/label/span[3]""")))),
        "Select Moscow and its region": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH,"""//*[@id="123"]/ol/li/ol/li[1]/ol/li[1]/ol/li[1]/span/label/span[3]""")))),
        "Confirm selection": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.CLASS_NAME,"""button2__text""")))),
        "Choose dynamics option": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH,"""//*[@id="page"]/div/div[2]/div/span/label[2]""")))),
    }
    # Define alternative actions to chosee region BY.CLASS_NAME, "button2__text"
    # in case the first path to click is not accessible
    msk_actions_alternative = {
        "Select region": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="page"]/div/div[2]/div/div[3]/div[1]/div/div[1]/div[2]/div/button/span[1]"""))).click(),
        "Cancel selection": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="123"]/ol/li/span/label/span[3]"""))).click(),
        "Select Moscow and its region": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="123"]/ol/li/ol/li[1]/ol/li[1]/ol/li[1]/span/label/span[3]"""))).click(),
        "Confirm selection": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[4]/div/div/div/div/div[2]/div/div[2]/div/div[4]/button/span"""))).click(),
        "Choose dynamics option": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="page"]/div/div[2]/div/span/label[2]"""))).click(),
    }

    # Process region and save data locally
    if len(keys_msk) > 0:
        msk_data = process_region(browser, keys_msk, msk_actions, msk_actions_alternative, region_1)
        if not msk_data.empty:
            final_data = msk_data
    else:
        print("No data for Moscow and region")
        final_data = pd.DataFrame()

    region_2 = "Saint Petersburg and region"
    # Define actions to chosee region
    spb_actions = {
        "Select region": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH,"""//*[@id="page"]/div/div[2]/div/div[3]/div[1]/div/div[1]/div[3]/div/button/span[1]""")))),
        "Select all": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH,"""//*[@id="123"]/ol/li/span/label/span[1]/span""")))),
        "Cancel selection": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH,"""//*[@id="123"]/ol/li/span/label/span[3]""")))),
        "Select Northwestern Region": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH,"""//*[@id="123"]/ol/li/ol/li[1]/ol/li[2]/span/button""")))),
        "Select Saint Petersburg and its region": lambda: browser.execute_script("arguments[0].click();", WebDriverWait(browser, default_wait).until(
            EC.element_to_be_clickable((By.XPATH,"""//*[@id="123"]/ol/li/ol/li[1]/ol/li[2]/ol/li[1]/span/label/span[3]""")))),
        "Confirm selection": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.CLASS_NAME,"""button2__text"""))).click(),
    }

    # Define alternative actions to chosee region 
    # in case the first path to click is not accessible
    spb_actions_alternative = {
        "Select region": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="page"]/div/div[2]/div/div[3]/div[1]/div/div[1]/div[3]/div/button/span[2]"""))).click(),
        "Select all": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="123"]/ol/li/span/label/span[1]"""))).click(),
        "Cancel selection": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="123"]/ol/li/span/label/span[3]"""))).click(),
        "Select Northwestern Region": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="123"]/ol/li/ol/li[1]/ol/li[2]/span/button"""))).click(),
        "Select Saint Petersburg and its region": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="123"]/ol/li/ol/li[1]/ol/li[2]/ol/li[1]/span/label/span[3]"""))).click(),
        "Confirm selection": lambda: WebDriverWait(browser, default_wait).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[4]/div/div/div/div/div[2]/div/div[2]/div/div[4]/button"""))).click(),
    }
    
    # Process region and save data locally
    if len(keys_spb) > 0:
        spb_data = process_region(browser, keys_spb, spb_actions, spb_actions_alternative, region_2)
        if not spb_data.empty:
            final_data = pd.concat([final_data, spb_data], axis=0)
    else:
        print("No data for Saint Petersburg and region")
        final_data = pd.DataFrame()

    # Download button
    st.download_button(
        label="Download data as CSV",
        on_click=lambda: setattr(st.session_state, 'download_click', True),
        key="download_all",
        data=final_data.to_csv(sep=";", index=False).encode("utf-8-sig"),
        file_name="Wordstat.csv",
        mime="text/csv",
        )

    print("Sessions are completed.")
    time.sleep(sleep_time)
    browser.quit()

if __name__ == "__main__":
    main()