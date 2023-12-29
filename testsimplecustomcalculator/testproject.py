import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load settings
with open('testappsettings.json') as config_file:
    config = json.load(config_file)

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get(config["webAppUrl"])

try:
    # Wait for the input elements to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number']"))
    )

    # Theme validation (optional)
    theme = config["theme"]
    body = driver.find_element(By.TAG_NAME, "body")
    bgColor = body.value_of_css_property("background-color")
    expectedBgColor = "rgba(240, 240, 240, 1)" if theme == "Light" else "rgba(26, 26, 26, 1)"
    assert bgColor == expectedBgColor, f"Background color does not match {theme} theme."

    # Find elements
    operand1 = driver.find_element(By.CSS_SELECTOR, "input[type='number']:first-of-type")
    operand2 = driver.find_element(By.CSS_SELECTOR, "input[type='number']:last-of-type")
    operation = driver.find_element(By.CSS_SELECTOR, "select")
    calculate_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']:first-of-type")

    # Test addition
    operand1.clear()
    operand2.clear()
    operand1.send_keys("5")
    operand2.send_keys("3")
    operation.send_keys("add")
    calculate_button.click()

    # Wait for and verify result
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p"))
    )
    result = driver.find_element(By.CSS_SELECTOR, "p").text
    assert "8" in result, "Calculation result is incorrect."

    print("Test passed. Calculator functionality is working as expected.")

finally:
    driver.quit()
