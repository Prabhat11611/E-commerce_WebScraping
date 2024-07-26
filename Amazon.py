import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
# Used in Fetching the data from the next page.
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Initialize lists to store data
product_names = []
ratings = []
total_ratings = []
prices = []

browser = webdriver.Chrome("C:/Users/win11/Desktop/Sem-VI PBL/Power BI/chromedriver.exe")
browser.get("https://www.amazon.in")

search = browser.find_element_by_id("twotabsearchtextbox")
search.send_keys("Home Decor")
search.send_keys(Keys.RETURN)
time.sleep(2)

def scrape():
    # Find all the product elements
    products_details = browser.find_elements_by_xpath("//div[@data-component-type='s-search-result']")

    # Extract and print the details of each product
    for product in products_details:
        product_name = product.find_element_by_xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']").text
        product_names.append(product_name)

        try:
            rating = product.find_element_by_xpath(".//span[@class='a-icon-alt']").get_attribute('textContent')
        except:
            rating = "N/A"
        ratings.append(rating)
        
        try:
            total_rating = product.find_element_by_xpath(".//span[@class='a-size-base s-underline-text']").get_attribute('textContent')
        except:
            total_rating = "N/A"
        total_ratings.append(total_rating)

        try:
            price = product.find_element_by_xpath(".//span[@class='a-price-whole']").text
        except:
            price = "N/A"
        prices.append(price)
        
        print("Product Name:", product_name)
        print("Rating:", rating)
        print("Total Ratings:", total_rating)
        print("Price:", price)
        print()
scrape()

# The link present in the below line needs to be changed for different different products (by their 2nd page link).
# browser.get("https://www.amazon.in/s?k=Lehenga&page=2&crid=16APPYLD73URX&qid=1711908288&sprefix=%2Caps%2C251&ref=sr_pg_2")
# browser.get("https://www.amazon.in/s?k=Saree&page=2&qid=1711945827&ref=sr_pg_2")
# browser.get("https://www.amazon.in/s?k=Makeup&page=2&qid=1711949443&ref=sr_pg_2")
browser.get("https://www.amazon.in/s?k=Home+Decor&page=2&crid=C3MBYXXDR4MN&qid=1711957639&sprefix=home+de%2Caps%2C522&ref=sr_pg_2")

for i in range(2,3):
    time.sleep(2)
    current_url = browser.current_url
    base_url = current_url.split('&page=')[0]
    index = current_url.split('&ref=sr_pg_')[1].split('&')[0]  # Extract the index value from the current URL
    next_page = base_url + "&page=" + str(i) + "&ref=sr_pg_" + index
    browser.get(next_page)
    print(next_page)
    time.sleep(2)
    scrape()
    time.sleep(2)


# https://www.amazon.in/s?k=Lehenga&page=3&crid=16APPYLD73URX&qid=1711908288&sprefix=%2Caps%2C251&ref=sr_pg_3


data = {'Product Name': product_names, 'Rating': ratings, 'Total Ratings':total_ratings, 'Price': prices}
df = pd.DataFrame(data)
print(df)

# Save DataFrame to a CSV file
df.to_csv('Trial_Data.csv', index=False)

# # Quit the browser session
# browser.quit()