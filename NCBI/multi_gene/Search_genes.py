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
import sys
import re


# +
#mouseのオルソログの情報を持ってくる。
def mouse_Orthologs():
    ortholog = browser.find_element(By.LINK_TEXT,"mouse")
    ortholog.click()
    
#Rattusのオルソログを持ってくる。
def Rattus_Ortholog():
    ortholog = browser.find_element(By.LINK_TEXT,"all")
    ortholog.click()
    #tag = browser.find_element_by_css_selector('a[data-ga-label="Rattus norvegicus"]')
    tag = browser.find_element(By.CSS_SELECTOR,'a[data-ga-label="Rattus norvegicus"]')
    tag.click()
    #ここで新しいタブが開く。一旦新しいタブに操作を移動させたのち、昔のタブを消す。
    sleep(5)
    browser.switch_to.window(browser.window_handles[1])
    browser.switch_to.window(browser.window_handles[0])
    browser.close()
    browser.switch_to.window(browser.window_handles[0])

#同じ方法で各動物のオルソログを取ってくる関数も書けるだろう。


# +
browser= webdriver.Chrome()
df = pd.DataFrame()
gene = pd.DataFrame()

#Objective_genes.txtファイルに改行区切りで遺伝子名を入れておく。
with open('Objective_genes.txt') as f:
    for line in f.readlines():
        try:
            url= "https://www.ncbi.nlm.nih.gov/"
            browser.get(url)
            search_win = browser.find_element(By.ID,"term")
            search_win.send_keys(line)
            
            # searchボタンを押さなければいけない時と押さなくてもいい時がある(謎)これを解決
            try: 
                search_button = browser.find_element(By.ID,"search")
                search_button.click()
            except:
                pass
            
            #遺伝子名をAlso known asに指定される名前で検索してしまったとき、リンクのidが変わる問題を解決
            try: 
                gene = browser.find_element(By.ID,"feat_gene_title")
                gene.click()
            except:
                gene = browser.find_element(By.ID,"gene_title")
                gene.click()
            
            #humanの情報でいいときはここをコメントアウトする。ラットのオルソログがないものもあるので、その分エラーも増える。
            Rattus_Ortholog()
            #逆にマウスの情報が欲しい時は＃を消す
            #mouse_Orthologs()
            
            #gene一つずつ、辞書を作ってdfに入れては辞書を初期化する手法をとる。
            gene ={}
            name = browser.find_element(By.CLASS_NAME,"title")
            gene_url = browser.current_url
            
            gene["name"] = name.text
            gene["url"] = gene_url
            
            #Beautiful Soupで読み取るためのお膳立て(res)
            res = requests.get(gene_url)
            soup = BeautifulSoup(res.text,"html.parser")
            categoryItems = soup.find("dl",attrs={"id":"summaryDl"})
            categoryItems = categoryItems.find_all("dd")
            gene["gene_type"] = categoryItems[4].text
            gene["also_known_as"] = categoryItems[8].text
            gene["summary"] = categoryItems[9].text 
            #必要な情報が増える場合、ここで調節
            
            Location = soup.find("div",attrs={"class":"gt_cont_contents"})
            gene["Location"] = Location.find_all("span")[1].text
            #dfに個々の遺伝子のデータを順に追加していく。
            if "df" in globals():
                gene_df = pd.DataFrame(gene,index = [0])
                df = pd.concat([gene_df,df],axis=0)
            else:
                df= pd.DataFrame(gene,index = [0])
                
        #どこかしらでエラーが起きた場合はここへ。そのエラーを出力。
        except Exception as e:
            gene = {}
            gene["name"] = line
            gene["error"] = e
            gene_df = pd.DataFrame(gene,index = [0])
            df = pd.concat([gene_df,df],axis=0)
df.to_csv("gene.csv",index = False)
browser.quit()
# -

gene_df
df
#joined

# +
#url = "https://www.ncbi.nlm.nih.gov/gene/5468/ortholog/?scope=7776"

#res = requests.get(url)
#soup = BeautifulSoup(res.text,"html.parser")
#soup
#javascriptのせいで、オルソログのページはBeautiful　Soupでは上手く取得できない。
#Seleniumから以下のよう(page_source)にする。ここにSeleniumの強みがある。
#browser= webdriver.Chrome()
#browser.get(url)
#source_code = browser.page_source
#tag = browser.find_element_by_css_selector('a[data-ga-label="Rattus norvegicus"]')
#tag.click()
#categoryItems = soup.find("dl",attrs={"id":"summaryDl"})
# -




