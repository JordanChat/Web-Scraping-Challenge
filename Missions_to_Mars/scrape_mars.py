from bs4 import BeautifulSoup as bs 
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import time
import os 
import requests

def scrape():
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')
    slide_title = soup.find_all('li', class_ = 'slide')

    news_title = slide_title[0].find('div', class_ = 'content_title')
    
    title1 = news_title.text.strip()
    
    article_body = slide_title[0].find('div', class_ = 'article_teaser_body')
    
    news_p = article_body.text.strip()

    browser.quit()

    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    table = pd.read_html(url)
    
    mars_info = table[0]
    mars_info = mars_info.rename(columns = {0: 'About Mars', 1: 'Information'})
    mars_info = mars_info.set_index('About Mars')
    mars_info = mars_info.to_html()

    browser.quit()

    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url3)
    hemisphere_image_urls = []
    soup = bs(browser.html, 'html.parser')
    hemisphere_stuff = soup.find_all('div', class_ = 'item')
    image_url3 = 'https://astrogeology.usgs.gov/'

    for stuff in hemisphere_stuff:
        hemisphere_titles = stuff.find('h3').text
        image_url88 = stuff.find('a', class_ = 'itemLink product-item')['href']
        browser.visit(image_url3 + image_url88)
        image_url88 = browser.html
        soup = bs(image_url88, 'html.parser')
        img_url = image_url3 + soup.find('img', class_ = 'wide-image')['src']
        hemisphere_image_urls.append({
            'hemisphere_titles': title, 
            'image_url': img_url})

    scraped_stuff = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_info": mars_info,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return scraped_stuff

    
    