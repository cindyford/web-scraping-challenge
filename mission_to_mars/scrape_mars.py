import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import requests
import pymongo



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)



def scrape_all():
    browser = init_browser()

    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser("chrome", **executable_path, headless=False)
    title, news = mars_news(browser)
    featured_image = featured_image_url(browser)
    weather = mars_weather(browser)
    html_df = facts_table(browser)
    hemispheres = hemisphere(browser)

    mars_data = {
        "title": title, 
        "news": news,
        "featured_image_url": featured_image,
        "mars_weather": weather,
        "table": html_df,
        "hemispheres" : hemispheres
    }

    return mars_data




def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url) 
    browser.is_element_present_by_tag('div.css-article_teaser_body', wait_time = 5)   
    html = browser.html
    soup = bs(html, 'lxml')
    results = soup.find_all('div', class_='content_title')[1] 
    title = results.find('a').text
    news = soup.find('div', class_='article_teaser_body').text

    return title, news

def featured_image_url(browser):
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url6 = 'https://www.jpl.nasa.gov'
    browser.visit(url2)
    html2 = browser.html
    soup2 = bs(html2, 'lxml')
    thumb = soup2.find('a', class_="button fancybox")
    featured_image  = url6 + thumb['data-fancybox-href']
    
    return featured_image

def mars_weather(browser):
    url4 = 'https://twitter.com/marswxreport'
    browser.visit(url4)
    browser.is_element_present_by_tag('div.css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0', wait_time = 5)
    html4 = browser.html
    soup4 = bs(html4, 'lxml')
    twitter = soup4.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    weather = twitter.span.text

    return weather

def facts_table(browser):
    url3 = "https://space-facts.com/mars/"
    tables = pd.read_html(url3)
    df = tables[0]
    df.columns = ["","Value"]
    html_df = df.to_html(index=False)

    return html_df

def hemisphere(browser):
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    hemispheres=[]
    html5 = browser.html
    soup5 = bs(html5, 'lxml')
    
    for i in range(4): 
        x = soup5.find_all('div', class_ = 'item')[i].h3.text
        browser.links.find_by_partial_text(x).click()
        browser.find_by_css('a.open-toggle').click()
        hemi_title = browser.find_by_tag('h2').text
        hemi_img = browser.find_by_css('img.wide-image')['src']
        hemisphere_img_urls = {
        'title': hemi_title,
        'img_url': hemi_img
        }
        hemispheres.append(hemisphere_img_urls)
        browser.back()



    return hemispheres







