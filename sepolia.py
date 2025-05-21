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
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

def claim_faucet():
    print("🚀 Starting faucet claim process...")

    chrome_options = Options()
    # comment out headless to see the browser
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://cloud.google.com/application/web3/faucet/ethereum/sepolia")
        time.sleep(5)

        # Click "Sign in with Google"
        google_signin = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in with Google')]")
        google_signin.click()
        time.sleep(5)

        # Switch to login window
        driver.switch_to.window(driver.window_handles[1])

        # Fill in email
        email_input = driver.find_element(By.XPATH, '//input[@type="email"]')
        email_input.send_keys(EMAIL)
        email_input.send_keys(u'\ue007')  # Enter
        time.sleep(3)

        # Fill in password
        password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
        password_input.send_keys(PASSWORD)
        password_input.send_keys(u'\ue007')  # Enter
        time.sleep(8)

        # Switch back to faucet window
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)

        # Fill in the wallet address if field is available
        try:
            wallet_input = driver.find_element(By.XPATH, '//input[@aria-label="Wallet address"]')
            wallet_input.clear()
            wallet_input.send_keys(WALLET_ADDRESS)
            time.sleep(2)
        except:
            print("⚠️ Wallet address input not found or already filled.")

        # Click "Request" button
        claim_button = driver.find_element(By.XPATH, '//button[contains(text(), "Request")]')
        claim_button.click()
        print("✅ Faucet claimed successfully!")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
    finally:
        time.sleep(5)
        driver.quit()

# Run every 24 hours
schedule.every(24).hours.do(claim_faucet)

print("🕓 Scheduler started. Waiting for the next run...")
while True:
    schedule.run_pending()
    time.sleep(60)                                                  
