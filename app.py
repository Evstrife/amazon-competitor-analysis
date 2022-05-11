import streamlit as st
import pandas as pd
import numpy as np
# scraper 
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


def scrape_review(asin):
    review_date = []
    review_text = []
    overall_rate = []
    helpful_vote = []
    # open website
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    product_asin = asin
    web = 'https://www.amazon.com/dp/' + product_asin
    driver.get(web)
    driver.implicitly_wait(5)
    # find all review button
    all_review_button= driver.find_element(By.XPATH,'//a[@data-hook="see-all-reviews-link-foot"]')
    all_review_button.click()
    # find all review cards
    items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="a-section celwidget"]')))

    for item in items:

        # find review_text
        body = item.find_element(By.XPATH,'.//span[@data-hook="review-body"]/span')
        review_text.append(body.text)
        #find review_time and location
        date = item.find_element(By.XPATH,'.//span[@data-hook="review-date"]')
        review_date.append(date.text)
        #find overall_rate out of five stars
        rate = item.find_element(By.XPATH,'.//i[@data-hook="review-star-rating"]').get_attribute("class")
        overall_rate.append(rate[26:27])
        #find # of people find review helpful
        helpful = item.find_element(By.XPATH,'.//span[@data-hook="helpful-vote-statement"]')
        helpful_vote.append(helpful.text.split()[0])
    
    driver.quit()
    data = {
            'text':review_text,
           'rate':overall_rate,
            'vote':helpful_vote,
            'time':review_date,
            }
    review = pd.DataFrame(data)
    return review


# app title
st.title('Amazon Product Competence Analysis')
# asin input
with st.form("my_form"):
    asin = st.text_input("Input ASIN:", value="", max_chars=10, key=None, type="default",help = "Amazon unique product ID")
    submit = st.form_submit_button("Get me the Analysis")
# review output
load_dotenv()
st.write('Top reviews')
if submit:
    data = scrape_review(asin)
    st.dataframe(data,width = None, height = None)




