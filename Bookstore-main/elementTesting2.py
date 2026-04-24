from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("http://127.0.0.1:8000/login/")

driver.find_element(By.ID, "username").send_keys("Faria Fahmida")
driver.find_element(By.ID, "password").send_keys("Fahmidasarmin@1999")

time.sleep(5)

driver.find_element(By.XPATH, '//*[@id="submit"]').click()


time.sleep(5)
