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

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests 
import pandas as pd

browser= webdriver.Chrome()


url = "https://www.ncbi.nlm.nih.gov/"
browser.get(url)

search_win = browser.find_element(By.ID,"term")
search_win.send_keys("Chgb")

search_button = browser.find_element(By.ID,"search")
search_button.click()

gene = browser.find_element(By.ID,"feat_gene_title")
gene.click()


# +
res = requests.get(url)
res

soup = BeautifulSoup(res.text,"html.parser")
#soup
gene ={}

name = browser.find_element(By.CLASS_NAME,"title")
gene_url = browser.current_url
#categoryItems
#categoryItems = categoryItems.find_all("dl")

gene["name"] = name.text
gene["url"] = gene_url

#gene["Summary"] = 
gene

# +
res = requests.get(gene_url)
res
soup = BeautifulSoup(res.text,"html.parser")
soup

#summaryのテーブル構造を抽出
categoryItems = soup.find("dl",attrs={"id":"summaryDl"})
categoryItems = categoryItems.find_all("dd")

gene["gene_type"] = categoryItems[4].text
gene["summary"] = categoryItems[9].text
gene
# -

Location = soup.find("div",attrs={"class":"gt_cont_contents"})
gene["Location"] = Location.find_all("span")[1].text

df = pd.DataFrame(gene,index = [0])
df

df.to_csv("gene.csv",index = False)
