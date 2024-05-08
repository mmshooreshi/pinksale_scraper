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


def setup_driver():
    # Setting up undetected_chromedriver to avoid detection
    options = uc.ChromeOptions()
    # options.add_argument('--headless')  # Run headless if you don't need a browser UI
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    return driver


basefolder ='/Users/mmtishooreshi/MYFILES/DEVV/scrape/INPUTS'
basefolderOUTPUT ='/Users/mmtishooreshi/MYFILES/DEVV/scrape/OUTPUTS'


from selenium.webdriver.common.by import By

def scrape_data_new(driver, urls):
    data = []
    
    # Navigate to the page
    driver.get(urls[0])
    print(" . . . . . waiting for main div . . . . . . ")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "main div")))
    

    
    # Locating panels using text and relative paths
    try:
        print(" . . . . . waiting for canvas . . . . . . ")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[8]/div[2]')))        
        print("Main div founded ^________^ yo0o0o ho0o0o")
        
        # Token Panel Information
        token_panel = driver.find_elements(By.CSS_SELECTOR, "div[title='Token']")
        if token_panel:
            print(token_panel)            
            data['token_name'] = token_panel[0].find_element(By.XPATH, "//div[contains(text(), 'Name')]/following-sibling::div").text

        # Pool Information
        pool_panel = driver.find_elements(By.CSS_SELECTOR, "div[title='Pool info']")
        if pool_panel:
            print(pool_panel)            
            data['pool_address'] = pool_panel[0].find_element(By.XPATH, "//div[contains(text(), 'Address')]/following-sibling::div/a").get_attribute('href')
        
        # Side Panel Information
        side_panel = driver.find_elements(By.CSS_SELECTOR, "div[title='Status']")
        if side_panel:
            print(side_panel)
            data['current_status'] = side_panel[0].find_element(By.XPATH, "//following-sibling::div").text
        
    except NoSuchElementException as e:
        print(f"An element was not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return data        
    #     # Use text content and relative paths for more robust selectors
    #     token_panel = driver.find_element(By.XPATH, "//div[contains(text(), 'Token')]/ancestor::div[contains(@class, 'divide-y')]")
    #     pool_panel = driver.find_element(By.XPATH, "//div[contains(text(), 'Pool info')]/following-sibling::div[contains(@class, 'divide-y')]")

    #     # Example for side_panel if it has a specific class or unique text
    #     # This is hypothetical as the exact content or class name of side_panel is not provided
    #     side_panel = driver.find_element(By.XPATH, "//div[contains(@class, 'specific-class-for-side-panel') or contains(text(), 'Specific Text Identifier')]")

    #     data.append({
    #         'url': url,
    #         'side_panel': side_panel.text,  # Fetch text or any specific data required
    #         'token_panel': {
    #             'address': token_panel.find_element(By.XPATH, "//div[contains(text(), 'Address')]/following-sibling::div").text,
    #             'name': token_panel.find_element(By.XPATH, "//div[contains(text(), 'Name')]/following-sibling::div").text,
    #             'symbol': token_panel.find_element(By.XPATH, "//div[contains(text(), 'Symbol')]/following-sibling::div").text,
    #             'decimals': token_panel.find_element(By.XPATH, "//div[contains(text(), 'Decimals')]/following-sibling::div").text,
    #             'total_supply': token_panel.find_element(By.XPATH, "//div[contains(text(), 'Total supply')]/following-sibling::div").text
    #         },
    #         'pool_panel': {
    #             'address': pool_panel.find_element(By.XPATH, "//div[contains(text(), 'Address')]/following-sibling::div").text,
    #             'tokens_for_presale': pool_panel.find_element(By.XPATH, "//div[contains(text(), 'Tokens For Presale')]/following-sibling::div").text,
    #             'tokens_for_liquidity': pool_panel.find_element(By.XPATH, "//div[contains(text(), 'Tokens For Liquidity')]/following-sibling::div").text,
    #             'softcap': pool_panel.find_element(By.XPATH, "//div[contains(text(), 'SoftCap')]/following-sibling::div").text,
    #             'start_time': pool_panel.find_element(By.XPATH, "//div[contains(text(), 'Start time')]/following-sibling::div").text,
    #             'end_time': pool_panel.find_element(By.XPATH, "//div[contains(text(), 'End time')]/following-sibling::div").text,
    #             'listing_on': pool_panel.find_element(By.XPATH, "//div[contains(text(), 'Listing on')]/following-sibling::div").text,
    #             'liquidity_percent': pool_panel.find_element(By.XPATH, "//div[contains(text(), 'Liquidity percent')]/following-sibling::div").text,
    #             'liquidity_lockup_time': pool_panel.find_element(By.XPATH, "//div[contains(text(), 'Liquidity Lockup Time')]/following-sibling::div").text
    #         }
    #     })

    # except Exception as e:
    #     print(f"An error occurred: {str(e)}")
    
    # return data


def text_is_not_zero(locator):
    """Returns a method that checks if the text of the element at the given locator is not '0'."""
    def _predicate(driver):
        element_text = driver.find_element(locator[0], locator[1]).text.strip()
        return element_text != "0"
    return _predicate

def scrape_data(driver, urls, filename):
    collected_data = []
    failed_urls=[]
    for url in urls:
        driver.get(url)
        try:
            print("- - - - - - - ** - - - - - - -\n")
            locator = (By.XPATH, "//div[contains(text(), 'Total supply')]/following-sibling::div/div")
            totalSupplyTemp = driver.find_element(locator[0], locator[1]).text.strip()
            if totalSupplyTemp == '0':
                print(f"The total supply is '{totalSupplyTemp}' :(((( Let's wait . . . ")
                WebDriverWait(driver, 10).until(
                    text_is_not_zero(locator),
                    message="The element's text did not change from '0' within the time limit."
                )
                totalSupplyTemp = driver.find_element(locator[0], locator[1]).text.strip()
                print(f"The total supply is '{totalSupplyTemp}'.  yo0ho0 --> .. . . . ")
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
            print(data_entry)
            save_data(data_entry, filename)
            sleep(0.1)
        except Exception as e:
            print(f"Failed to process {url}: {str(e)}")
            failed_urls.append(url)
    print("\n\n FAILED:", failed_urls)
    return collected_data, failed_urls

def parse_side_panel(driver):
    audits = ""
    info = {}
    try:
        audits =driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/main/div/div/div[2]/div[1]/div[3]/div[1]/div[3]').text
        info["audits"]=audits.replace('\n','|')
    except:
        print("ERR MAIN PANEL: audits")
        
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
        

    # urls = read_urls_from_csv(basefolder) 
    # result_data = scrape_data_new(driver, urls)
    
    # save_data(result_data)
    
    # Optionally, save or process the data here
    
    # print(result_data)
    driver.quit()

if __name__ == "__main__":
    main()




