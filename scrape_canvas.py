import cv2
import numpy as np
import urllib
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def setup_driver():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    return driver

driver = setup_driver()

url = "https://www.pinksale.finance/solana/launchpad/9cUXubaDQukuadJSakbEUbG3oiPsKm7RC1sfb2oHMQu8"
driver.get(url)

# Use a static nearby element to scroll first if necessary
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
sleep(3)  # Allow any animations to finish

canvas_data_url = canvas.screenshot_as_base64
data_url = f"data:image/png;base64,{canvas_data_url}"

response = urllib.request.urlopen(data_url)
image_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # Convert image to grayscale and detect edges
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray_image, 100, 200)

# # Find contours
# contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Optionally visualize contours
# for contour in contours:
#     cv2.drawContours(image, [contour], -1, (0, 255, 0), 3)
#     print(cv2.contourArea(contour) )
    


# total_area = sum(cv2.contourArea(contour) for contour in contours)
# print(total_area)
# total_area+=0.000001
# slice_percentages = [(cv2.contourArea(contour) / total_area) * 100 for contour in contours]

# # Print slice percentages
# for i, percentage in enumerate(slice_percentages, 1):
#     print(f"Slice {i}: {percentage:.2f}%")







blue_channel, green_channel, red_channel = cv2.split(image)

# Edge detection on each color channel
edges_blue = cv2.Canny(blue_channel, 100, 200)
edges_green = cv2.Canny(green_channel, 100, 200)
edges_red = cv2.Canny(red_channel, 100, 200)

# Combine the edges from each color channel
combined_edges = cv2.bitwise_or(cv2.bitwise_or(edges_blue, edges_green), edges_red)

# Optionally, you can adjust the thresholds for each color channel if different channels
# have different levels of contrast or if you want to emphasize certain features:
# edges_blue = cv2.Canny(blue_channel, lower_blue, upper_blue)
# edges_green = cv2.Canny(green_channel, lower_green, upper_green)
# edges_red = cv2.Canny(red_channel, lower_red, upper_red)

# Find contours on the combined edge image
contours, _ = cv2.findContours(combined_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# For visualization, draw contours on the original image
output_image = image.copy()
cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)

# Display the result
cv2.imshow('Contours', output_image)





cv2.waitKey(0)
cv2.destroyAllWindows()

driver.quit()
