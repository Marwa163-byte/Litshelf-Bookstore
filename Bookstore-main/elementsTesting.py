from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("http://127.0.0.1:8000/signup/")

driver.find_element(By.ID, "username").send_keys("Faria Fahmida")
driver.find_element(By.ID, "email").send_keys("fariafahmida@gmail.com")
driver.find_element(By.ID, "password1").send_keys("Fahmidasarmin@1999")
driver.find_element(By.ID, "password2").send_keys("Fahmidasarmin@1999")

time.sleep(5)

driver.find_element(By.XPATH, "//button[text()='Submit']").click()


time.sleep(5)
