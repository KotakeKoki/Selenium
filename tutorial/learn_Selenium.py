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

# <h1>Tutorial2</h1>

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

# <h1>Tutorial3</h1>

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

# <h1>Tutorilal4</h1>

# +
#Go back the site of tutorilal.
import requests
from bs4 import BeautifulSoup

url = "https://scraping-for-beginner.herokuapp.com/ranking/"
res = requests.get(url)

res
# -

soup = BeautifulSoup(res.text,"html.parser")
#soup

# +
#First of all,Get a name of first tourist area
#"u_areaListRankingBox"class contains informations of one area

spots = soup.find_all("div",attrs={"class":"u_areaListRankingBox"})
spot = spots[0]
#spot.find_all("div",attrs={"class":"u_title"})
#Confirm the class has only one text
spot_name = spot.find("div",attrs={"class":"u_title"})
spot_name
# -

spot_name.text

#remove unnecessary information
spot_name.find("span",attrs={"class":"badge"}).extract()

spot_name

spot_name = spot_name.text.replace("\n","")
spot_name

#Get the Score
eval_num = spot.find("div",attrs={"class":"u_rankBox"}).text
eval_num =eval_num.replace("\n" , "")

spot

categoryItems = spot.find("div",attrs = {"class","u_categoryTipsItem"})
categoryItems

categoryItems = categoryItems.find_all("dl")
categoryItems

#Get only "楽しさ"
categoryItem = categoryItems[0]
categoryItem

#It's useful
category = categoryItem.dt.text
category

#Get the Score
rank = float(categoryItem.span.text)
rank

# +
#make the dictionary
details = {}

categoryItem = categoryItems[0]
category = categoryItem.dt.text
rank = float(categoryItem.span.text)
details[category] = rank

details

# +
#Write the repetetion code

for categoryItem in categoryItems:
    category = categoryItem.dt.text
    rank = float(categoryItem.span.text)
    details[category] = rank
details
# -

datum = details 
datum["観光地名"] = spot_name
datum["評価点"] = eval_num
datum

# +
#Get Informations of All site 

soup = BeautifulSoup(res.text,"html.parser")
data = []

spots = soup.find_all("div",attrs={"class":"u_areaListRankingBox"})
for spot in spots:
    spot_name = spot.find("div",attrs={"class":"u_title"})
    spot_name.find("span",attrs={"class":"badge"}).extract()
    spot_name = spot_name.text.replace("\n","")
    eval_num = spot.find("div",attrs={"class":"u_rankBox"}).text
    eval_num =eval_num.replace("\n" , "")

    categoryItems = spot.find("div",attrs = {"class","u_categoryTipsItem"})
    categoryItems = categoryItems.find_all("dl")


    details = {}

    categoryItem = categoryItems[0]
    category = categoryItem.dt.text
    rank = float(categoryItem.span.text)
    details[category] = rank

    for categoryItem in categoryItems:
        category = categoryItem.dt.text
        rank = float(categoryItem.span.text)
        details[category] = rank

    datum = details 
    datum["観光地名"] = spot_name
    datum["評価点"] = eval_num
    data.append(datum)
# -

data

import pandas as pd
df = pd.DataFrame(data)

df

#Sort the col_name
df.columns

df = df[['観光地名', '評価点','楽しさ', '人混みの多さ', '景色', 'アクセス']]

df.to_csv("観光地情報.csv",index = False)

# <h1>Tutorilal5</h1>

import requests
from bs4 import BeautifulSoup

url = "https://scraping-for-beginner.herokuapp.com/image/"
res = requests.get(url)

soup = BeautifulSoup(res.text,"html.parser")
soup

image_tag = soup.find("img")
image_tag["src"]
#check the src of img

#plus root URL
root_url = "https://scraping-for-beginner.herokuapp.com"
img_url = root_url + image_tag["src"]
img_url

#Preserve the image.
from PIL import Image
import io

#Binary to Image
img = Image.open(io.BytesIO(requests.get(img_url).content))
img

img.save("sample.jpg")

# +
soup = BeautifulSoup(res.text,"html.parser")
image_tags = soup.find_all("img")

#get the index number(enumerate)
for i,img_tag in enumerate(image_tags):
    root_url = "https://scraping-for-beginner.herokuapp.com"
    img_url = root_url + img_tag["src"]
    img = Image.open(io.BytesIO(requests.get(img_url).content))
    img.save(f"sample{i}.jpg")
# -




