#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pymongo
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


# In[9]:


client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 


# In[12]:


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    collection.drop()

    newsURL = 'https://mars.nasa.gov/news/'
    browser.visit(newsURL)
    newsHTML = browser.html
    newsSoup = bs(newsHTML,'lxml')
    newsTitle = newsSoup.find("div",class_="content_title").text
    newsParagraph = newsSoup.find("div", class_="rollover_description_inner").text

    jurl = 'https://www.jpl.nasa.gov/missions?mission_target=Mars'
    browser.visit(jurl)
    jhtml = browser.html
    jpl_soup = bs(jhtml,"html.parser")
    image_url = jpl_soup.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
    base_link = "https:"+jpl_soup.find('div', class_='jpl_logo').a['href'].rstrip('/')
    feature_url = base_link+image_url
    featured_image_title = jpl_soup.find('h1', class_="media_feature_title").text.strip()

    mhurl = 'https://marshemispheres.com/cerberus.html'
    browser.visit(mhurl)  
    mhtml = browser.html 
    mh_soup = bs(mhtml,"html.parser") 
    results = mh_soup.find_all("div",class_='item')
    hemisphere_image_urls = []
    for result in results:
            product_dict = {}
            titles = result.find('h3').text
            end_link = result.find("a")["href"]
            image_link = "https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg" + end_link    
            browser.visit(image_link)
            html = browser.html
            soup= bs(html, "html.parser")
            downloads = soup.find("div", class_="downloads")
            image_url = downloads.find("a")["href"]
            product_dict['title']= titles
            product_dict['image_url']= image_url
            hemisphere_image_urls.append(product_dict)


    browser.quit()

    mars_data ={
        'newsTitle' : newsTitle,
        'summary': newsParagraph,
        'featured_image': feature_url,
        'featured_image_title': featured_image_title,
        'weather': mars_weather,
        'fact_table': mars_fact_html,
        'hemisphere_image_urls': hemisphere_image_urls,
        'newsURL': newsURL,
        'jpl_url': jurl,
        'weather_url': turl,
        'fact_url': murl,
        'hemisphere_url': mhurl,
        }
    collection.insert(mars_data)


# In[ ]:




