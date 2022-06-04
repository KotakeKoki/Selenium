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
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests 
import pandas as pd
import sys
import datetime
import re

# +
#https://www.ncbi.nlm.nih.gov/home/about/policies/
#上記ページの"Guidelines for Scripting Calls to NCBI Servers"には"Do not overload NCBI's systems. "Make no more than 3 requests every 1 second."
#一つずつクエリを送り、クリックのたびに数秒待つ分には問題ないと解釈し、以下のコードを記す。
options = Options()
options.headless = True

browser= webdriver.Chrome(options=options)
df = pd.DataFrame()
doc_df = pd.DataFrame()



#keywords.txtファイルに改行区切りでkeywordを入れておく。
with open('keywords.txt') as f:
    for line in f.readlines():
        try:
            url= "https://pubmed.ncbi.nlm.nih.gov/"
            browser.get(url)
            sleep(1)
            search_win = browser.find_element(By.CLASS_NAME,"term-input.tt-input")
            search_win.send_keys(line)
            
            try: 
                search_button = browser.find_element(By.CLASS_NAME,"search-btn")
                search_button.click()
                sleep(3)
            except:
                pass
            
            hit = browser.find_element(By.CLASS_NAME,"results-amount").text
            print(hit)
            hit_num = re.sub(r"\D", "", hit)
            print(hit_num)
            
            num = int(int(hit_num)/10)
            
            if num >100:
                print("too many articles to read.I'll get only first 1,000.")
                num = 100
                
            for i in range(num):
                try: 

                    #for i in range(len(docs)):
                    for i in range(10):
                        docs = browser.find_elements(By.CSS_SELECTOR,'a[data-ga-category="result_click"]')

                        doc = {}
                        doc_button = docs[i]
                        doc_button.click()
                        name= browser.find_element(By.CLASS_NAME,"heading-title")
                        year = browser.find_element(By.CLASS_NAME,"cit")
                        journal = browser.find_element(By.ID,"full-view-journal-trigger")
                        doc_url = browser.current_url
                        print("OK1")

                        try:
                            abstract = browser.find_element(By.CLASS_NAME,"abstract-content.selected")
                        except:
                            abstract = browser.find_element(By.CLASS_NAME,"empty-abstract")

                        print("OK2")
                        print(abstract.text)


                        doc["name"] = name.text
                        doc["year"] = re.split('[;: ]', year.text)[0]
                        doc["url"] = doc_url
                        doc["journal"] = journal.text
                        doc["abstract"] = abstract.text

                        if "df" in globals():
                            doc_df = pd.DataFrame(doc,index = [0])
                            df = pd.concat([doc_df,df],axis=0)
                            print("a")
                        else:
                            df= pd.DataFrame(doc,index = [0])
                        print("3")
                        sleep(2)
                        browser.back()
                        sleep(3)
                    #10記事抜き出したら次のページへ
                    next_btn = browser.find_element(By.CLASS_NAME,"button-wrapper.next-page-btn")
                    next_btn.click()
                    sleep(5)               
                
                except:
                     print("error")
                     browser.quit()



        except:
            print("error2")
            pass

dt_now = datetime.datetime.now()
df.to_csv(dt_now.strftime('%Y_%m_%d_%H_%M')+".csv",index = False)
browser.quit()
# -

df

# <h1>Seleniumの強み</h1>

# +
#url = "https://www.ncbi.nlm.nih.gov/gene/5468/ortholog/?scope=7776"

#res = requests.get(url)
#soup = BeautifulSoup(res.text,"html.parser")
#soup

#javascriptのせいで、オルソログのページのHTMLはBeautiful　Soupでは上手く取得できない。
#Seleniumから以下のよう(page_source)にする。すると人間が見たままのページのHTMLが出る。
#ここにSeleniumの強みがある。
#browser= webdriver.Chrome()
#browser.get(url)
#source_code = browser.page_source#これを参照しながらfind_elementをすれば良い。
#tag = browser.find_element_by_css_selector('a[data-ga-label="Rattus norvegicus"]')
#tag.click()
#categoryItems = soup.find("dl",attrs={"id":"summaryDl"})
# -






