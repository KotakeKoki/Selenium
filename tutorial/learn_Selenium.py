# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
#This is the script written accorting to the Youtube video (https://www.youtube.com/watch?v=f8FXUUQ4uRA)

# #! pip install Selenium

# +
# #!brew install webdriver
# -

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


browser = webdriver.Chrome()

browser = webdriver.Chrome()
url = "https://scraping-for-beginner.herokuapp.com/login_page"
browser.get(url)

#Get the element what I want by ID
elem_username = browser.find_element(By.ID,"username")
elem_username.send_keys("imanishi")


elem_password = browser.find_element(By.ID,"password")
elem_password.send_keys("kohei")

elem_button = browser.find_element(By.ID,"login-btn")
elem_button.click()
#Finish logged in


"""headless mode(Don't open the web browser)

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")

browser = webdriver.Chrome(options=options)
url = "https://scraping-for-beginner.herokuapp.com/login_page"
browser.get(url)
browser.quit()

"""

elem = browser.find_element(By.ID,"name")
elem.text

elem = browser.find_element(By.ID,"company")
elem.text


elem = browser.find_element(By.ID,"birthday")
elem.text

elem = browser.find_element(By.ID,"hobby")
hobby = elem.text
#replace character
hobby = hobby.replace("\n",",")
hobby

#Get the first table
elem_th = browser.find_element(By.TAG_NAME,"th")
elem_th.text

#Get multiple tables
elems_th = browser.find_elements(By.TAG_NAME,"th")
elems_th
#We could get 5 tables

elems_th[4].text

#make a dictionary 
keys = []
for elem_th in elems_th :
    key = elem_th.text
    keys.append(key)

keys

elems_td = browser.find_elements(By.TAG_NAME,"td")
values = []
for elem_td in elems_td :
    value = elem_td.text
    values.append(value)

values

# +
#Output CSV
import pandas as pd 
df = pd.DataFrame()

df["項目"] = keys
df["値"] = values

df
# -

df.to_csv("講師情報.csv")

# +
#Let's use Beautiful Soup
#Analyze the structure of HTML

import requests
from bs4 import BeautifulSoup

#url = "https://scraping-for-beginner.herokuapp.com/Udemy"
#The page accessed in that video doesn't exist,so I access to Ikegayalab instead of that.
#I'm not a member of that labolatory.
url = "http://www.yakusaku.jp/"
res = requests.get(url)
res
#<Response [200]> is OK.
# -

#Parser analyzes the structure of HTML
soup = BeautifulSoup(res.content,"html.parser")
soup

#more readable by indent
print(soup.prettify())

#Get multiple "p"tags
soup.find_all("p")

#Get a specified text by class
soup.find_all("p")

#Get a text of the first "p"tag
soup.find("p").text
#equal "soup.p.text"

soup.find_all("p",attrs={"class":"about_pad"})

soup.find_all("span",attrs={"class":"bold"})

#Another means of getting text(Use CSS selector)
#https://webliker.info/css-selector-cheat-sheet/
soup.select_one(".about_pad").text


