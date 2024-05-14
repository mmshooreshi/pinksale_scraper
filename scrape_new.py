from colorama import init
init(autoreset=True)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
from time import sleep
import csv
import os
import traceback
import sys
from datetime import datetime


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# print(f"{RED}   {RESET}")
# print(f"{GREEN}   {RESET}")
# print(f"{YELLOW}   {RESET}")

def setup_driver():
    # Setting up undetected_chromedriver to avoid detection
    options = uc.ChromeOptions()
    # options.add_argument('--headless')  # Run headless if you don't need a browser UI
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    return driver


basefolder ='INPUTS'
basefolderOUTPUT ='OUTPUTS'


from selenium.webdriver.common.by import By


def text_is_not_zero(locator):
    """Returns a method that checks if the text of the element at the given locator is not '0'."""
    def _predicate(driver):
        element_text = driver.find_element(locator[0], locator[1]).text.strip()
        return element_text != "0"
    return _predicate

def scrape_data(driver, urls, filename):
    total_count = len(urls)
    collected_data = []
    failed_urls=[]
    i=0
    for url in urls:
        driver.get(url)
        i=i+1

        try:
            
            print(f"{YELLOW} - - - - - - - ** {i} / {total_count} ** - - - - - - - {RESET}\n")
            locator = (By.XPATH, "//div[contains(text(), 'Total supply')]/following-sibling::div/div")
            totalSupplyTemp = driver.find_element(locator[0], locator[1]).text.strip()
            if totalSupplyTemp == '0':
                print(f"The total supply is '{totalSupplyTemp}' :(((( Let's wait . . . ")
                WebDriverWait(driver, 10).until(
                    text_is_not_zero(locator),
                    message="The element's text did not change from '0' within the time limit."
                )
                totalSupplyTemp = driver.find_element(locator[0], locator[1]).text.strip()
                print(f"The total supply is '{totalSupplyTemp}'. {GREEN} yo0ho0 --> {RESET} {YELLOW} .. . . . {RESET} ")
                sleep(1)
            
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Total Contributors')]"))
            )

            # Parse data from side panels
            side_panel_data = parse_side_panel(driver)
            # Parse data from token and pool panels
            token_data = parse_token_panel(driver)
            pool_data = parse_pool_panel(driver)
            
            
            # Combine all parsed data into a dictionary
            data_entry = {**side_panel_data, **token_data, **pool_data}
            collected_data.append(data_entry)
            print(f"{GREEN} \n{data_entry} {RESET}")
            save_data(data_entry, filename)
            sleep(0.1)
        except Exception as e:
            print(f"{RED} Failed to process {url}: {str(e)} {RESET}")
            failed_urls.append(url)
    if failed_urls != []:
        print(f"\n\n {RED} FAILED: {YELLOW} {failed_urls} {RESET}")
    return collected_data, failed_urls



def parse_side_panel(driver):
    audits = ""
    info = {}
    j=1
    try:
        audits =driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/main/div/div/div[2]/div[1]/div[3]/div[1]/div[3]').text        
        info["audits"]=audits.replace('\n','|')
    except:
        print("ERR MAIN PANEL: audits (1)")
        j=0
    if j==0:
        try:
            audits =driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/main/div/div/div[2]/div[1]/div[2]/div[1]/div[3]').text
            info["audits"]=audits.replace('\n','|')
        except:
            print("ERR MAIN PANEL: audits (2)")



        
    try:
        side_panel = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/main/div/div/div[2]/div[2]/div/div[3]')
        items = side_panel.find_elements(By.XPATH, ".//div[contains(@class, 'py-2')]")
        for item in items:
            label = item.find_element(By.XPATH, ".//div[1]").text.strip().lower().replace(' ', '_')
            value = item.find_element(By.XPATH, ".//div[2]").text.strip()
            if label in ['max_buy','min_buy']:
                value=value.split()[0]
            info[label] = value
        
    except:
        print("ERR SIDE PANEL")
        
    return info

def parse_token_panel(driver):
    try:
        token_panel = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[3]/div[2]/div/div[2]')
        
        data= {
            'token_address': token_panel.find_element(By.XPATH, "//a[contains(@href, 'solscan.io')]").get_attribute('href').split('/')[-1],
            'token_name': token_panel.find_element(By.XPATH, "//div[contains(text(),'Name')]/following-sibling::div").text,
            'token_symbol': token_panel.find_element(By.XPATH, "//div[contains(text(),'Symbol')]/following-sibling::div").text,
            'token_decimals': token_panel.find_element(By.XPATH, "//div[contains(text(),'Decimals')]/following-sibling::div").text,
            'token_total_supply': None
        }
    except:
        print("ERR TOKEN PANEL")

    try:
        data['token_total_supply']= token_panel.find_element(By.XPATH, "//div[contains(text(),'Total supply')]/following-sibling::div/div").text
    except:
        print("ERR TOKEN PANEL: token_total_supply")
        
    return data

def parse_pool_panel(driver):
    pool_panel = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[3]/div[3]/div[2]')
    try:
        data = {
            'pool_address': pool_panel.find_element(By.XPATH, "//a[contains(@href, 'solscan.io')]").get_attribute('href'),
            'tokens_for_presale': None,
            'softcap': pool_panel.find_element(By.XPATH, "//div[contains(text(),'SoftCap')]/following-sibling::div").text.split()[0],
            'listing_on': None,
            'start_time': pool_panel.find_element(By.XPATH, "//div[contains(text(),'Start time')]/following-sibling::div").text.split()[0],
            'end_time': pool_panel.find_element(By.XPATH, "//div[contains(text(),'End time')]/following-sibling::div").text.split()[0],
            'liquidity_percent':None,
            'liquidity_lockup_time': None,
            'tokens_for_liquidity': None,
            'liquidity_unlocked_time': None     
            }
    except:
        print("ERR POOL PANEL")

    try:
        data['tokens_for_presale']= pool_panel.find_element(By.XPATH, "//div[contains(text(),'Tokens For Presale')]/following-sibling::div/div").text.split()[0]
    except:
        print("ERR POOL PANEL: tokens_for_presale")
                    
    try:
        data['listing_on']= pool_panel.find_element(By.XPATH, "//div[contains(text(),'Listing on')]/following-sibling::div/div/a").get_attribute('href')
    except:
        print("ERR POOL PANEL: listing_on")
        
    try:
        data['liquidity_percent']=pool_panel.find_element(By.XPATH, "//div[contains(text(),'Liquidity percent')]/following-sibling::div/div/div").text
    except:
        print("ERR POOL PANEL: liquidity_percent")
    
    try:
        data['liquidity_lockup_time']=pool_panel.find_element(By.XPATH, "//div[contains(text(),'Liquidity Lockup Time')]/following-sibling::div").text
    except:
        print("ERR POOL PANEL: liquidity_lockup_time")
      
    try:
        data['tokens_for_liquidity']=pool_panel.find_element(By.XPATH, "//div[contains(text(),'Tokens For Liquidity')]/following-sibling::div/div").text.split()[0]
    except:
        print("ERR POOL PANEL: tokens_for_liquidity")
    
    try:
        data['liquidity_unlocked_time']=pool_panel.find_element(By.XPATH, "//div[contains(text(),'Liquidity Unlocked Time')]/following-sibling::div").text
    except:
        print("ERR POOL PANEL: liquidity_unlocked_time")

    return data

def optional_find(element, xpath, attribute=None):
    try:
        found_element = element.find_element(By.XPATH, xpath)
        return found_element.get_attribute(attribute) if attribute else found_element.text
    except:
        return None


def save_data(data, filename):
    filename = filename.replace('_links.csv','_links_extracted_data.csv')
    fieldnames = ["audits","token_address", "token_name", "token_symbol", "token_decimals", "token_total_supply",
                  "pool_address", "tokens_for_presale", "tokens_for_liquidity", "softcap",
                  "start_time", "end_time", "listing_on", "liquidity_percent",
                  "liquidity_lockup_time", "liquidity_unlocked_time", "status", "sale_type","unsold_token", 
                  "min_buy", "max_buy", "current_rate", "current_raised","total_contributors", "claim_time", "hard_cap_per_user",  "max_allocation_requires"]
    
    # {'status': 'Ended', 'sale_type': 'Public', 'max_buy': '50 SOL', 'current_rate': '1 SOL = 687,604.867 BDUCK', 'current_raised': '880.0047 SOL (880.00%)', 'total_contributors': '893', 'token_address': 'https://solscan.io/account/CPqY8ZHmfzUKbc8p3Kdg7StddT3J9y8R2qxgbSxwmhV2', 'token_name': 'BlueDuck', 'token_symbol': 'BDUCK', 'token_decimals': '9', 'token_total_supply': '999,996,463.9592', 'pool_address': 'https://solscan.io/account/CPqY8ZHmfzUKbc8p3Kdg7StddT3J9y8R2qxgbSxwmhV2', 'tokens_for_presale': '605,095,541.4 BDUCK', 'softcap': '100 SOL', 'start_time': '2024.04.28 14:00 (UTC)', 'end_time': '2024.05.05 14:00 (UTC)', 'listing_on': 'https://raydium.io/swap/?inputCurrency=CPqY8ZHmfzUKbc8p3Kdg7StddT3J9y8R2qxgbSxwmhV2&outputCurrency=sol&fixed=in'}
    # Check if the file exists to decide whether to write the header
    file_exists = os.path.isfile(f"{basefolderOUTPUT}/{filename}")
    
    with open(f"{basefolderOUTPUT}/{filename}", 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
            writer.writerow(data)
        else:
            writer.writerow(data)

def main():
    driver = setup_driver()
    urls=[]
    

    if len(sys.argv) > 1:
        print("salam")
        print(sys.argv[1])
        urls =[sys.argv[1]]
        print(urls)
        result_data,failed_urls = scrape_data(driver, urls, f"datetime:{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")
        retry_result_data,twice_failed_urls = scrape_data(driver, failed_urls, f"datetime:{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")
        
    else:
        for filename in os.listdir(basefolder):
            urls=[]
            if filename.endswith("_links.csv"):
                filepath = os.path.join(basefolder, filename)                    
                with open(filepath, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)
                    for row in reader:
                        url = row[0]
                        urls.append(row[0])
            result_data,failed_urls = scrape_data(driver, urls, filename)
            retry_result_data,twice_failed_urls = scrape_data(driver, failed_urls, filename)
            
    driver.quit()

if __name__ == "__main__":
    main()




