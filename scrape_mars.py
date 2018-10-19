# dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
from flask import Flask, render_template
import time
import numpy as np
import json
from selenium import webdriver


def init_browser():
    #splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():  
    #NASA news title
    browser = init_browser()
    mars_collection = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_collection["news_title"] = soup.find('div', class_="content_title").get_text()
    mars_collection["news_snip"] = soup.find('div', class_="rollover_description_inner").get_text()
    
    # Feature Images
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    response = browser.html
    soup2 = BeautifulSoup(response, 'html.parser')
    images = soup2.find_all('a', class_="fancybox")
    pic_source = []
    for image in images:
        picture = image['data-fancybox-href']
        pic_source.append(picture)
       
    mars_collection["featured_image_url"] = "https://www.jpl.nasa.gov" + pic_source[2]

    # Mars Weather
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    response = browser.html
    soup3 = BeautifulSoup(response, 'html.parser')
    weather = soup3.find_all("div", class_="js-tweet-text-container")
    weather_mars = []
    for content in weather:
        current_weather = content.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        weather_mars.append(current_weather)
    mars_collection["mars_weather"] = weather_mars[8]

    
    # Mars Facts
    fact_url = "https://space-facts.com/mars/"
    df_facts = pd.read_html(fact_url)[0]
    df_facts.columns = ["Facts", "Values"]
    clean_table = df_facts.set_index(["Facts"])
    mars_table = clean_table.to_html()
    mars_table = mars_table.replace("\n", "")
    mars_collection["fact_table"] = mars_table
    
    
    # Mars Hemisphere
    hemisphere_image_urls = []
    
    ## Cerberus
    cerberus = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    browser.visit(cerberus)
    response4 = browser.html
    soup4 = BeautifulSoup(response4, 'html.parser')
    cerberus_pic = soup4.find_all('div', class_="wide-image-wrapper")
    for pic in cerberus_pic:
        pic1 = pic.find('li')
        full_picture1 = pic1.find('a')['href']
    cerberus_title = soup4.find('h2', class_='title').get_text()
    cerberus_info = {"Title": cerberus_title, "url": full_picture1}
    hemisphere_image_urls.append(cerberus_info)
    
    ## Schiaparelli 
    schiaparelli = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(schiaparelli)
    response5 = browser.html
    soup5 = BeautifulSoup(response5, 'html.parser')
    schiaparelli_pic = soup5.find_all('div', class_="wide-image-wrapper")
    for pic in schiaparelli_pic:
        pic2 = pic.find('li')
        full_picture2 = pic2.find('a')['href']
    schiaparelli_title = soup5.find('h2', class_='title').get_text()
    schiaparelli_info = {"Title": schiaparelli_title, "url": full_picture2}
    hemisphere_image_urls.append(schiaparelli_info)
    
    ## Syrtis
    syrtis = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(syrtis)
    response6 = browser.html
    soup6 = BeautifulSoup(response6, 'html.parser')
    syrtis_pic = soup6.find_all('div', class_="wide-image-wrapper")
    for pic in syrtis_pic:
        pic3 = pic.find('li')
        full_picture3 = pic3.find('a')['href']
    syrtis_title = soup6.find('h2', class_='title').get_text()
    syrtis_info = {"Title": syrtis_title, "url": full_picture3}
    hemisphere_image_urls.append(syrtis_info)
    
    ## Valles Marineris
    valles = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(valles)
    response7 = browser.html
    soup7 = BeautifulSoup(response7, 'html.parser')
    valles_pic = soup7.find_all('div', class_="wide-image-wrapper")
    for pic in valles_pic:
        pic4 = pic.find('li')
        full_picture4 = pic4.find('a')['href']
    valles_title = soup7.find('h2', class_='title').get_text()
    valles_info = {"Title": valles_title, "url": full_picture4}
    hemisphere_image_urls.append(valles_info)
    
    ## Collection of information about Mars
    mars_collection["hemisphere_image"] = hemisphere_image_urls
    
    return mars_collection
    
    
    

    
