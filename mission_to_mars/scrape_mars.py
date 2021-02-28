from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import os

def scrape():
    # Setup Executive path & initilaze browser

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Add an empty dictionary to store web scrapping

    mars_data = {}

    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    soup = bs(browser.html, 'html.parser')

    latest_title = soup.find_all('div', class_='content_title')[1].text
    mars_data["latest title"] = latest_title
    print(f'The title of the latest article is: {latest_title}')

    p_text = soup.find('div', class_='article_teaser_body' ).get_text()
    mars_data["article_text"] = p_text
    print(f'The paragraph of the article reads: {p_text}')

    # Visit JPL Mars Images

    jpl_url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(jpl_url)
    soup = bs(browser.html, 'html.parser')

    featured_img = soup.find('img', class_ = 'BaseImage object-contain')['src']
    mars_data["mars_image"] = featured_img
    print(featured_img)

    # Visit Mars Facts url

    facts_url = 'https://space-facts.com/mars/'
    
    mars_facts = pd.read_html(facts_url)
    mars_facts_df = mars_facts[0]
    mars_df = mars_facts_df.rename(columns={0:"Attribute", 1:"Value"})
    html_table = mars_df.to_html()
    mars_data["facts_about_mars"] = html_table

    # Visit Hemisphere URL

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    soup = bs(browser.html, 'html.parser')

    results = soup.find_all('div', class_='item')


    hemi_image_urls = []
    base_url = "https://astrogeology.usgs.gov"

    for result in results:
        title = result.find('h3').text
        img__url_combo = base_url + result.find('a')['href']
        soup_2 = bs(browser.html, 'html.parser')
        hemi_img_url = soup_2.find('ul').li.a['href']
        hemi_img_dict = {'title': title, 
                'img_url': hemi_img_url}
        hemi_image_urls.append(hemi_img_dict)   

    mars_data['mars_hemispheres'] = hemi_image_urls

    return mars_data

  