from bs4 import BeautifulSoup
import requests
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

google_doc_link = "https://docs.google.com/forms/d/e/1FAIpQLSch8Gf69SObY17cMs_6p02eDauEsHQEnefER5GqdMXx3mUNjQ/viewform"
zillow_link = 'https://appbrewery.github.io/Zillow-Clone/'

z_response = requests.get(zillow_link)
z_webpage = z_response.text
soup = BeautifulSoup(z_webpage, "html.parser")
addresses_anchor = soup.select(".ListItem-c11n-8-84-3-StyledListCardWrapper .property-card-link")
address_links = [link['href'] for link in addresses_anchor]

prices = soup.select(".PropertyCardWrapper__StyledPriceLine")
prices_stripped = [price.text for price in prices]
prices_pref = [price.replace("+/mo", "") for price in prices_stripped]
prices_pref_1 = [price.replace("/mo", "").replace("1 bd", "").replace("+ 1bd", "") for price in prices_stripped]
prices_pref_2 = [price.replace("+", "").strip() for price in prices_pref_1]
addy = soup.findAll("address")
addresses = [place.text.strip().replace("|", "") for place in addy]
driver.get(google_doc_link)
time.sleep(1)

for i in range(len(addresses)):
    address_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                                  '1]/div/div[1]/input')
    address_field.send_keys(addresses[i])
    price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                                '1]/div/div[1]/input')
    price_field.send_keys(prices_pref_2[i])
    link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                               '1]/div/div[1]/input')
    link_field.send_keys(address_links[i])
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()
    time.sleep(1)
    another_response = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_response.click()
