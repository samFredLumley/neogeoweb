
# coding: utf-8

# In[81]:

#user should input kijiji url and number of pages required (each page has ~20 listings)
#keep pages required <5 to avoid kijiji getting angry
url_main = 'https://www.kijiji.ca/b-maison-a-vendre/ville-de-montreal/c35l1700281'
pages_required = 5


# In[80]:

#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[82]:

#creates an array of the listings pages to be scraped
url_main_list = [url_main]
url_bits = url_main.split("montreal")
for i in range(pages_required - 1):
    url_new = url_bits[0] + 'montreal/page-' + str(i + 2) + url_bits[1]
    url_main_list.append(url_new)


# In[83]:

#requests and parses each listings page
soup_list = []
for url in url_main_list:
    page = requests.get(url)
    soup_list.append(BeautifulSoup(page.text, 'html.parser'))


# In[84]:

#scrapes all links to individual listing pages
url_list = []
for html_page in soup_list:
    listings = html_page.find_all("a", class_="title")
    for listing in listings:
        url_list.append('https://www.kijiji.ca' + listing.get('href'))


# In[85]:

#creates an array of parsed html for each individual listing page
page_list = []
for url in url_list:
    listing_page = requests.get(url)
    listing_page_soup = BeautifulSoup(listing_page.text, 'html.parser')
    page_list.append(listing_page_soup)


# In[110]:

#scrapes info boxes, lat, lon, image urls and no. bedrooms
info_list, lat_list, lon_list, bedroom_list, image_list = [] = ([] for i in range(5))
for entry in page_list:
    info = entry.select('div[class*="itemTitleWrapper"]')[0]
    info_list.append(info)
    
    lat = entry.select('meta[property="og:latitude"]')[0].get('content')
    lat_list.append(lat)
    
    lon = entry.select('meta[property="og:longitude"]')[0].get('content')
    lon_list.append(lon)
    
    bedrooms = entry.select('dd[class*="attributeValue"]')[0].contents[0][:1]
    bedroom_list.append(bedrooms)
    
    if entry.find('img'):
        image = entry.select('img[alt="Listing item"]')[0].get('src')
        image_list.append(image)
    else:
        image = 'na'
        image_list.append(image)


# In[107]:

#scrapes titles, prices, addresses and dates from the info boxes
title_list, price_list, address_list, date_list = ([] for i in range(4))
for attribute in info_list:
    title = attribute.select('h1')[0].contents[0]
    title_list.append(title)
    
    price = attribute.select('div[class*="priceContainer"]')[0].contents[0].contents[0]
    #some listings did not have a price (or the span that contains them). The if function avoids an error
    if price.find('span'):
        price_list.append(price)
    else:
        price_list.append(price.contents[0])
    
    address = attribute.select('span[class*="address"]')[0].contents[0]
    address_list.append(address)
    
    date = attribute.select('time')[0].get('title')
    date_list.append(date)


# In[108]:

#enters data into a pandas dataframe
data = ([url_list, title_list, price_list, address_list, date_list, lat_list, lon_list, image_list, bedroom_list])
df = pd.DataFrame(data).T
df.columns = ['URL', 'Title', 'Price', 'Address', 'Date listed', 'Latitude', 'Longitude', 'Image URL', 'No. bedrooms']
df.head();


# In[109]:

#saves dataframe to csv output file
df.to_csv('output.csv', index=False, header=True)


# In[ ]:



