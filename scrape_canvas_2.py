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
img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)


# resize
scale = 0.5;
h, w = img.shape[:2];
h = int(h*scale);
w = int(w*scale);
img = cv2.resize(img, (w,h));

# hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV);
h,s,v = cv2.split(hsv);
h = cv2.medianBlur(h, 5);

# find values
cv2.namedWindow("Hue");
# cv2.setMouseCallback("Hue", clicky);
while True:
    cv2.imshow("Hue", h);
    if cv2.waitKey(1) == ord('q'):
        break;

# threshold (102, 60, 14)
slices = [];
ranges = [102, 60, 14];
for r in ranges:
    mask = cv2.inRange(h, r-1, r+1);
    slices.append(np.sum(mask == 255));

# convert slices to percentages
percents = [];
total = sum(slices);
for s in slices:
    percent = (s / total) * 100;
    percents.append(round(percent, 1));
print(percents);

# convert to angles
angles = [];
total = 360;
for p in percents:
    angles.append(p * total / 100);
print(angles);
# Convert image to grayscale and detect edges


driver.quit()





