from selenium import webdriver
from bs4 import BeautifulSoup
import time

url = "https://finance.yahoo.com/quote/BBD/options"

driver = webdriver.Firefox()  # or Chrome()
driver.get(url)
time.sleep(5)  # wait for JS to load

soup = BeautifulSoup(driver.page_source, "html.parser")
rows = soup.select("table tbody tr")

options_data = []
for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 10:
        strike = cols[2].text.strip()
        last_price = cols[3].text.strip()
        bid = cols[4].text.strip()
        ask = cols[5].text.strip()
        volume = cols[8].text.strip()
        options_data.append((strike, last_price, bid, ask, volume))


print(options_data)
driver.quit()
