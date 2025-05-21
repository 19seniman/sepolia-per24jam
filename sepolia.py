import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import schedule

load_dotenv()

EMAIL = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_PASSWORD")

def claim_faucet():
    print("Starting faucet claim process...")

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # remove this if you want to see the browser
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://cloud.google.com/application/web3/faucet/ethereum/sepolia")
        time.sleep(5)

        # Click sign in with Google
        google_signin = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in with Google')]")
        google_signin.click()
        time.sleep(5)

        # Switch to login tab
        driver.switch_to.window(driver.window_handles[1])

        # Fill email
        email_input = driver.find_element(By.XPATH, '//input[@type="email"]')
        email_input.send_keys(EMAIL)
        email_input.send_keys(u'\ue007')  # ENTER key
        time.sleep(3)

        # Fill password
        password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
        password_input.send_keys(PASSWORD)
        password_input.send_keys(u'\ue007')  # ENTER key
        time.sleep(8)

        # Switch back
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)

        # Wait and click on "Request Tokens" or similar
        claim_button = driver.find_element(By.XPATH, '//button[contains(text(), "Request")]')
        claim_button.click()
        print("Faucet claimed successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

# Schedule to run once every 24 hours
schedule.every(24).hours.do(claim_faucet)

print("Scheduler started. Waiting for next run...")
while True:
    schedule.run_pending()
    time.sleep(60)
