from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import cv2
import numpy as np
import urllib
import pytesseract

def setup_driver():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    return driver

driver = setup_driver()

url = "https://www.pinksale.finance/solana/launchpad/9cUXubaDQukuadJSakbEUbG3oiPsKm7RC1sfb2oHMQu8"
driver.get(url)

# Scroll to a more reliable nearby element first
nearby_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, 'footer')),  # Change this tag to a more appropriate one if needed
    message="wait for a known nearby element"
)
driver.execute_script("arguments[0].scrollIntoView(true);", nearby_element)

# Now wait for the canvas to appear
canvas = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[6]/div[2]/div/div/canvas")),
    message="wait for canvas"
)

# Execute any further operations on the canvas
sleep(3)  # Wait for any animations to complete if necessary

canvas_data_url = canvas.screenshot_as_base64
data_url = f"data:image/png;base64,{canvas_data_url}"

response = urllib.request.urlopen(data_url)
image_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# Apply OCR to extract text from the entire image
custom_config = r'--oem 3 --psm 11'
text = pytesseract.image_to_string(image, config=custom_config)
print("Extracted Text:", text)

cv2.imshow('OCR Results', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

driver.quit()
