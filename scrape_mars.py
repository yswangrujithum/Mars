# dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
from flask import Flask, render_template
import time
import numpy as np
from selenium import webdriver

app = Flask(__name__)

def scrape():
    #splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #NASA news title
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2018%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find_all('div', class_="slide")
    for result in results:
        title_lead = result.find('div', class_="content_title")
        title = title_lead.find('a').text
        body_lead = result.find('div', class_="rollover_description")
        body = body_lead.find('div', class_="rollover_description_inner").text
        
    # Feature Images
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(url_jpl)
    soup2 = BeautifulSoup(response.text, 'html.parser')
    images = soup2.find_all('a', class_="fancybox")
    pic_source = []
    for image in images:
        picture = image['data-fancybox-href']
        pic_source.append(picture)
       
    featured_image_url = "https://www.jpl.nasa.gov" + pic_source[2]

    # Mars Weather
    weather_url = "https://twitter.com/marswxreport?lang=en"
    weather = requests.get(weather_url)
    soup3 = BeautifulSoup(weather.text, 'lxml')
    contents = soup3.find_all("div", class_="content")
    weather_mars = []
    for content in contents:
        tweet = content.find("div", class_="js-tweet-text-container").text
        weather_mars.append(tweet)
    mars_weather = weather_mars[8]
    
    # Mars Facts
    fact_url = "https://space-facts.com/mars/"
    table = pd.read_html(fact_url)
    table[0]
    df_facts = table[0]
    df_facts.columns = ["Facts", "Values"]
    df_facts.set_index(["Facts"])
    fact_html = df_facts.to_html()
    fact_html = fact_html.replace("\n", "")
    df_facts.to_html('fact_table.html')
    
    # Mars Hemisphere
    hemisphere_image_urls = []
    
    ## Cerberus
    cerberus = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    response = requests.get(cerberus)
    soup4 = BeautifulSoup(response.text, 'html.parser')
    cerberus_pic = soup4.find_all('div', class_="wide-image-wrapper")
    for pic in cerberus_pic:
        pic1 = pic.find('li')
        full_picture1 = pic1.find('a')['href']
    cerberus_title = soup4.find('h2', class_='title').text 
    cerberus_info = {"Title": cerberus_title, "url": full_picture1}
    hemisphere_image_urls.append(cerberus_info)
    
    ## Schiaparelli 
    schiaparelli = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    response = requests.get(schiaparelli)
    soup5 = BeautifulSoup(response.text, 'lxml')
    schiaparelli_pic = soup5.find_all('div', class_="wide-image-wrapper")
    for pic in schiaparelli_pic:
        pic2 = pic.find('li')
        full_picture2 = pic2.find('a')['href']
    schiaparelli_title = soup5.find('h2', class_='title').text
    schiaparelli_info = {"Title": schiaparelli_title, "url": full_picture2}
    hemisphere_image_urls.append(schiaparelli_info)
    
    ## Syrtis
    syrtis = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    response = requests.get(syrtis)
    soup6 = BeautifulSoup(response.text, 'lxml')
    syrtis_pic = soup6.find_all('div', class_="wide-image-wrapper")
    for pic in syrtis_pic:
        pic3 = pic.find('li')
        full_picture3 = pic3.find('a')['href']
    syrtis_title = soup6.find('h2', class_='title').text
    syrtis_info = {"Title": syrtis_title, "url": full_picture3}
    hemisphere_image_urls.append(syrtis_info)
    
    ## Valles Marineris
    valles = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    response = requests.get(valles)
    soup7 = BeautifulSoup(response.text, 'lxml')
    valles_pic = soup7.find_all('div', class_="wide-image-wrapper")
    for pic in valles_pic:
        pic4 = pic.find('li')
        full_picture4 = pic4.find('a')['href']
    valles_title = soup7.find('h2', class_='title').text
    valles_info = {"Title": valles_title, "url": full_picture4}
    hemisphere_image_urls.append(valles_info)
    
    return hemisphere_image_urls
    
    

    
