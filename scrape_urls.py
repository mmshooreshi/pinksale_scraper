import os
import argparse
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from time import sleep
import csv
from colorama import init
init(autoreset=True)


# Create a backup directory if it doesn't exist
backup_dir = "INPUTS/backup"
if not os.path.exists(backup_dir):
    os


SOLANA_MAINNET_VALUE = "501424"
DROPDOWN_XPATH = "/html/body/div[1]/div/div[3]/main/div/div/div[2]/div[1]/div/div[2]/select"
WEEKS_XPATH = "/html/body/div[1]/div/div[3]/main/div/div/div[2]/div[1]/div/div[1]/div/div[{}]"

def countdown_sleep(seconds: int) -> None:
    """Sleep countdown with a print output."""
    for sec in range(seconds, 0, -1):
        print(sec)
        sleep(1)

def select_option(driver, xpath: str, value: str) -> None:
    """Select an option from a dropdown menu."""
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    select = Select(dropdown)
    select.select_by_value(value)


links={}
def scrape_data_for_week(driver, week_index: int, included_weeks: list): 
    """Scrape data for a specific week and save it to a CSV file."""
    # Click on the week item to load its data
    week_element = driver.find_element(By.XPATH, WEEKS_XPATH.format(week_index))
    week_element.click()
    countdown_sleep(2)  # Wait for data to load

    # Define the base XPath for the items you're interested in
    base_xpath = "/html/body/div[1]/div/div[3]/main/div/div/div[2]/div[2]/div[{}]"
    # Define the XPaths for text and href within each item
    text_xpaths = ["/div[1]", "/div[2]", "/div[3]"]
    href_xpaths = ["/div[3]/a"]
    
    csv_name = week_element.text.replace(' ','-').replace('/','-')
    week_number=str(csv_name.split('-')[1])
    print(week_number,included_weeks)
    if week_number not in included_weeks:
        return included_weeks
    # Open a CSV file to write data
    with open(f'INPUTS/{csv_name}.csv', 'w', newline='', encoding='utf-8') as file:
        links[f"{csv_name}"]=[]
        writer = csv.writer(file)
        # Write the headers
        # writer.writerow(['Content 1', 'Content 2', 'Content 3', 'Link'])
        # id,name,symbol,total_raised,finish_time,?,url_button,url
        writer.writerow(['ID','NAME','SYMBOL','TOTAL_RAISED','FINISH_TIME','URL_BUTTON','URL'])

        
        # Collect all data
        
        for i in range(1, 100):  # Loop through the first 10 div elements
            try:
                row = []
                for text_path in text_xpaths:
                    text_element = driver.find_element(By.XPATH, base_xpath.format(i) + text_path)
                    print(text_element.text)
                    txtArray = text_element.text.split('\n')
                    for item in txtArray:
                        row.append(item)
                        
                href_element = driver.find_element(By.XPATH, base_xpath.format(i) + href_xpaths[0])
                row.append(href_element.get_attribute('href'))
                

                # Write row to CSV
                writer.writerow(row)
                links[f"{csv_name}"].append(href_element.get_attribute('href'))
            except:
                pass
    with open(f'INPUTS/{csv_name}_links.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['url'])

        # Write each URL to the file
        urls = links[f"{csv_name}"]
        print (urls)
        for url in urls:
            writer.writerow([url])
    included_weeks = [week for week in included_weeks if week != week_number]
    return included_weeks
    # print(links)
        


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Scrape Pinksale data.')
    # parser.add_argument('num_weeks', type=int, help='Number of weeks to process')
    parser.add_argument('included_weeks', type=str, help='Included weeks')
    
    args = parser.parse_args()
    included_weeks = args.included_weeks.split(',')
    
    backup_dir = "INPUTS/backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    for filename in os.listdir("INPUTS"):
        if filename.endswith(".csv"):
            src = os.path.join("INPUTS", filename)
            dst = os.path.join(backup_dir, filename)
            if os.path.exists(dst):
                base, ext = os.path.splitext(dst)
                counter = 1
                new_dst = f"{base}_{counter}{ext}"
                while os.path.exists(new_dst):
                    counter += 1
                    new_dst = f"{base}_{counter}{ext}"
                dst = new_dst
            shutil.move(src, dst)
    driver = uc.Chrome()

    try:
        driver.get('https://www.pinksale.finance/leaderboards')
        select_option(driver, DROPDOWN_XPATH, SOLANA_MAINNET_VALUE)
        countdown_sleep(4)

        # Iterate over weeks
        for week_index in range(1, 20):
            included_weeks = scrape_data_for_week(driver, week_index, included_weeks)
            if len(included_weeks) == 0:
                break

    finally:
        driver.quit()

if __name__ == '__main__':
    main()
