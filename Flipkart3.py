import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize lists to store data
product_names = []
ratings = []
total_ratings = []
prices = []

browser = webdriver.Chrome("C:/Users/win11/Desktop/Sem-VI PBL/Power BI/chromedriver.exe")
browser.get("https://www.flipkart.com/")

search = browser.find_element_by_class_name("Pke_EE")
search.send_keys("Home Decor")
search.send_keys(Keys.RETURN)
time.sleep(2)

def scrape():
    # Wait for the product elements to be loaded
    WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='_2B099V']")))

    # Find all the product elements
    products_details = browser.find_elements(By.XPATH, "//div[@class='_2B099V']")

    # Extract and print the details of each product
    for product in products_details:
        try:
            product_name = product.find_element(By.XPATH, ".//a[@class='IRpwTa']").text
        except:
            product_name = "N/A"
        product_names.append(product_name)

        try:
            rating = product.find_element(By.CLASS_NAME, "_3LWZlK").text
        except:
            rating = "N/A"
        ratings.append(rating)

        try:
            total_rating = product.find_element(By.CLASS_NAME, "_2_R_DZ").text
        except:
            total_rating = "N/A"
        total_ratings.append(total_rating)

        try:
            price = product.find_element(By.XPATH, ".//div[@class='_30jeq3']").text
        except:
            price = "N/A"
        prices.append(price)
        
        print("Product Name:", product_name)
        print("Rating:", rating)
        print("Total Ratings:", total_rating)
        print("Price:", price)
        print()

scrape()

for i in range(2, 3):
    time.sleep(2)
    # Once the page has loaded, fetch the URL
    current_url = browser.current_url
    # Method 1
    base_url = current_url.split('&page=')[0]
    next_page=base_url + "&page=" + str(i)
    # Method 2
    # next_page=f"{current_url}&page={i}"
    browser.get(next_page)
    print(next_page)
    time.sleep(2)
    scrape()
    time.sleep(2)

data = {'Product Name': product_names, 'Rating': ratings, 'Total Ratings':total_ratings, 'Price': prices}
df = pd.DataFrame(data)
print(df)

# Save DataFrame to a CSV file
df.to_csv('2Scraped_Data.csv', index=False)

# Quit the browser session
browser.quit()
