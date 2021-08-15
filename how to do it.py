Challenge:
We work at an importer and the price of our products is linked to the quotation of: Dollar, Euro and Gold.
We need to automatically get the quotation for these 3 items on the internet and find out how much we should charge for our products, considering a contribution margin that we have in our database.

Data base: https://drive.google.com/drive/folders/blablabla

For that, let's create a web automation: we'll use selenium and webdriver.

# Step 1 - Get on the internet
#Chrome -> chromedriver
#Firefox -> geckodriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

# Step 2 - Get dollar exchange rate
# go to google
browser.get('https://www.google.com/')
# search "dollar exchange rate"
browser.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("dollar exchange rate")

browser.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
# get the number that appears in the google result
dollar_exchangerate = browser.find_element_by_xpath(
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(dollar_exchangerate)

# Step 3 - Get euro exchange rate
browser.get('https://www.google.com/')
# search "euro exchange rate"
browser.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("euro exchange rate")

browser.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
# get the number that appears in the google result
euro_exchangerate = browser.find_element_by_xpath(
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(euro_exchangerate)

# Step 4 - Get gold exchange rate

# enter the melhor cambio website
browser.get('https://www.melhorcambio.com/ouro-hoje')
# get the exchange rate
gold_exchangerate = browser.find_element_by_xpath('//*[@id="comercial"]').get_attribute("value")
gold_exchangerate = gold_exchangerate.replace(",", ".")
print(gold_exchangerate)

# Step 5 - Import and update the database
import pandas as pd

chart = pd.read_excel('Products.xlsx')
display(chart)

# update the exchange rate
# where there is a column "Coin = Dollar"
# chart.loc[rows, column]

chart.loc[chart["Coin"] == "Dollar", "Exchange Rate"] = float(dollar_exchangerate)

chart.loc[chart["Coin"] == "Euro", "Exchange Rate"] = float(euro_exchangerate)

chart.loc[chart["Coin"] == "Gold", "Exchange Rate"] = float(gold_exchangerate)

# update the Purchase Price -> Original Base Price * exchange rate
chart["Purchase Price"] = chart["Original Base Price"] * chart["Exchange Rate"]

# update the sale price -> purchase price * margin
chart["Sale Price"] = chart["Purchase Price"] * chart["Margin"]

# chart["Sale Price"] = chart["Sale Price"].map("{:.2f}".format)

display(chart)

# Step 6 - Export the updated database
chart.to_excel("New Products.xlsx", index=False)
