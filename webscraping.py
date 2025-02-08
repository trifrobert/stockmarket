from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import time
import os

USERNAME = 'facbanibani'
PASSWORD = '?FtO`%EN33@1'
PROFILE_URL = 'https://x.com/tradertvshawn'
HASHTAG_TO_FIND = '#stickynote'

# Path to your ChromeDriver
chrome_driver_path = r"C:\Users\turca\Desktop\chromedriver-win64\chromedriver.exe"

# Create a Service object
service = Service(chrome_driver_path)

# Initialize WebDriver
driver = webdriver.Chrome(service=service)

driver.get(PROFILE_URL)
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[2]/button[1]/div")))
button.click()

def login(driver):
    driver.get('https://x.com/login')
    
    # Wait for login elements
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'text'))
    ).send_keys(USERNAME)
    
    # Handle multi-step login flow
    next_buttons = driver.find_elements(By.XPATH, "//span[contains(text(),'Next')]")
    if next_buttons:
        next_buttons[0].click()

    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    ).send_keys(PASSWORD)
    
    driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]").click()
    time.sleep(3)  # Allow login to complete

def is_tweet_from_today(tweet_element):
    try:
        # Find the time element which contains the tweet timestamp
        time_element = tweet_element.find_element(By.CSS_SELECTOR, 'time')
        timestamp = time_element.get_attribute('datetime')
        tweet_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        current_date = datetime.now()
        yesterday = current_date - timedelta(days=1)
        
        # Check if tweet is from today or yesterday
        is_today = (
            tweet_date.day == current_date.day and 
            tweet_date.month == current_date.month and 
            tweet_date.year == current_date.year
        )
        
        is_yesterday = (
            tweet_date.day == yesterday.day and 
            tweet_date.month == yesterday.month and 
            tweet_date.year == yesterday.year
        )

        if is_today:
            print("Found a tweet from today")
        elif is_yesterday:
            print("Found a tweet from yesterday")
            
        return is_today or is_yesterday
        
    except Exception as e:
        print(f"Error checking tweet date: {str(e)}")
        return False

def find_sticky_note(driver):
    driver.get(PROFILE_URL)
    
    # Wait for tweets to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))
        )
    except TimeoutException:
        print("No tweets found or loading timeout")
        return None

    print('\n')
    # Find all tweets using a more reliable selector
    tweets = driver.find_elements(By.CSS_SELECTOR, 'article')
    print('Tweets found    ', tweets)
    
    for tweet in tweets:
        # First check if the tweet is from today
        if not is_tweet_from_today(tweet):
            continue
            
        try:
            # Updated selector for tweet text using the provided class
            tweet_text_element = tweet.find_element(By.CSS_SELECTOR, 'div.css-146c3p1.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-1udbk01.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim')
            tweet_text = tweet_text_element.text.lower()
            if HASHTAG_TO_FIND.lower() in tweet_text:
                full_text = tweet.find_element(By.CSS_SELECTOR, 'div[lang]').text
                return full_text
        except Exception as e:
            print(f"Error processing tweet: {str(e)}")
            continue
    
    return None

def main():
    try:
        login(driver)
        sticky_note = find_sticky_note(driver)
        
        if sticky_note:
            print("Sticky Note Found:")
            print(sticky_note)
        else:
            print(f"No tweet containing '{HASHTAG_TO_FIND}' found")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        time.sleep(60)
        driver.quit()

if __name__ == "__main__":
    main()

