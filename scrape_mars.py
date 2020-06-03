#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import time


# Windows Chrome Driver

# In[2]:


def init_browser():
    executable_path = {"executable_path": "C:/Users/MatthewS/Desktop/chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# Nasa Mars News

# In[3]:


url = 'https://mars.nasa.gov/news/'
#Use requests module to retrieve the webpage
response = requests.get(url)

#Create BeautifulSoup object
soup = BeautifulSoup(response.text, 'html.parser')


# In[4]:


#Retrieve article title and preview paragraph
news_title = soup.find('div', class_="content_title").find('a').text
news_p = soup.find('div', class_="rollover_description_inner").text

print(news_title)
print(news_p)


# JPL Mars - Featured Image

# In[5]:


# Run init_browser/driver.
browser = init_browser()

# Visit the url for JPL Featured Space Image.
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
browser.visit(jpl_url)
time.sleep(2)

browser.is_element_present_by_text("more info", wait_time=1)

# HTML Object.
html = browser.html

# Parse HTML with Beautiful Soup
image_soup = BeautifulSoup(html, "html.parser")

# Scrape image URL.
image_url = image_soup.find("figure", class_="lede")

# Concatentate https://www.jpl.nasa.gov with image_url.
featured_image_url = jpl_url

# Exit Browser.
browser.quit()


# In[6]:


print(featured_image_url)


# Mars Weather

# In[7]:


# Run init_browser/driver.
browser = init_browser()

# Visit the url for Mars Weather twitter account.
weather_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(weather_url)

#HTML Object
html = browser.html

#Parse HTML object with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

#Retrieve all elements with tweet information 
weather_tweets = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

for tweet in weather_tweets:
    
    #Assign tweet info to variable
    mars_weather = tweet.text
    
    # If tweet contains words sol and pressure, print the tweet
    if "sol" and "pressure" in mars_weather:
        print(mars_weather)
        break
    else:
        pass


# Mars Facts

# In[8]:


url = 'https://space-facts.com/mars/'
#Scrape table data from Mars webpage
tables = pd.read_html(url)
tables


# In[9]:


#Index the first dataframe object
df = tables[0]

#Set column names
df.columns = ['Description','Value']

#Set Description column as the index
df.set_index('Description', inplace=True)
df


# In[10]:


#Convert table into HTML table
html_table = df.to_html()
html_table


# In[11]:


#Remove unwanted new lines
html_table.replace('\n', '')


# Mars Hemishperes

# In[13]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#Open webpage using splinter
browser.visit(url)

#HTML object
html = browser.html

#Parse HTML object with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())


# In[14]:


#Create list for image urls
hemisphere_image_urls = []

#Extract base url from webpage url
base_url= (url.split('/search'))[0]


#Retrieve all items with hemisphere info
hemispheres = soup.find_all('div', class_='description')

for hemisphere in hemispheres:
    
    #Create an empty dictionary
    hemisphere_info = {}
    
    #Retrieve hemisphere title
    hem_title = hemisphere.find('h3').text
    
    #Add only hemisphere title into dictionary by splitting text 
    hemisphere_info['title'] = hem_title.split(' Enhanced')[0]
    
    #Retrieve route to detailed hemisphere webpage
    hem_route = hemisphere.find('a', class_='itemLink product-item')['href']
    
    #Concatenate base url with route
    hemisphere_link = base_url + hem_route
    
    #Open new url with splinter
    browser.visit(hemisphere_link)
    
    #HTML object
    html = browser.html
    
    #Parse HTML object with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    #Retrieve route to full resolution image
    image_url = soup.find('div', class_='downloads').find('ul').find('li').find('a')['href']
    
    #Add image url into dictionary
    hemisphere_info['img_url'] = image_url
    
    #Append dictionary to list
    hemisphere_image_urls.append(hemisphere_info)


# In[15]:


hemisphere_image_urls


# In[ ]:





# In[ ]:





# In[ ]:




