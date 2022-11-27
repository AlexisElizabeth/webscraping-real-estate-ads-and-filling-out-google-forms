import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
URL = "https://forms.gle/wAyCxCvtCukRehcT7"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

if __name__ == "__main__":
    response = requests.get(
        "https://www.zillow.com/homes/San-Francisco,-CA_rb/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
        headers=header)

    data = response.text

    soup = BeautifulSoup(data, "html.parser")

    all_address_elements = soup.select(".StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0 address")
    all_addresses = []
    for link in all_address_elements:
        all_addresses.append(link.text)
    print(all_addresses)

    all_prices = []
    all_price_elements = soup.select(".List-c11n-8-73-8__sc-1smrmqp-0 span")
    for price in all_price_elements:
        if "$" in price.text:
            all_prices.append(price.text)
    all_prices.remove('$2,699+ 2 bds')
    all_prices.remove('$2,699+ 2 bds')
    print(all_prices)
    
    all_links = []
    all_link_elements = soup.select(".ListItem-c11n-8-73-8__sc-10e22w8-0 a")
    for link in all_link_elements:
        if "www.zillow.com" in link["href"]:
            all_links.append(link["href"])
        else:
            all_links.append(f'https://www.zillow.com{link["href"]}')
    all_links = all_links[::2]

    driver_service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=driver_service)

    for i in range(len(all_links)):
        driver.get(URL)
        time.sleep(2)

        address_input = driver.find_elements(By.CSS_SELECTOR, value=".Xb9hP input")[0]
        price_input = driver.find_elements(By.CSS_SELECTOR, value=".Xb9hP input")[1]
        link_input = driver.find_elements(By.CSS_SELECTOR, value=".Xb9hP input")[2]
        submit_button = driver.find_element(By.CSS_SELECTOR, value=".l4V7wb span")

        address_input.send_keys(all_addresses[i])
        price_input.send_keys(all_prices[i])
        link_input.send_keys(all_links[i])
        submit_button.click()
        time.sleep(2)
