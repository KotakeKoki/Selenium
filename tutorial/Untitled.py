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
# #! pip install Selenium

# +
# #!brew install 
# -

from selenium import webdriver
from time import sleep


browser = webdriver.Chrome()

browser.quit()

browser = webdriver.Chrome()
url = "https://scraping-for-beginner.herokuapp.com/login_page"
browser.get(url)

browser.find_element_by_id("username")




