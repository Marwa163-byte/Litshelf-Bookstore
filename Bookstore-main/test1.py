from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

try:
    # Setup Chrome driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Maximize window to ensure visibility
    driver.maximize_window()

    # Navigate to URL
    driver.get("http://127.0.0.1:8000/shop_book_details/91ece4cf-35c4-44c3-9c15-dc67bbeff1c3/")

    # Keep browser open for 5 seconds
    time.sleep(5)

except Exception as e:
    print("An error occurred:", e)

finally:
    # Properly close the browser
    driver.quit()
    print("done")