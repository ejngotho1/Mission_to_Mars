

#Mission To Mars

# In[1]:
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# In[2]:
# set executable path to NASA Mars News
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# In[3]:
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# In[4]:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

# In[5]:
# we have our text/code in slide_elem---we will look for <div> element and class=content_title in this variable
slide_elem.find("div", class_='content_title')   # output is an html containing content title inside <div. element

# In[6]:
# the title is somewhere in the html code... thats all we need not the html stuff
# first we will find <a> tag and save it in an object ---news_title
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# In[7]:
# now lets look for the summary (teser) using find
# when we find 'teser' from DevTools we get the first summary/teser----article_teaser_body
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p
# # Featured Images
# ### after scraping text, lets now add images

# In[8]:
# when we open the NASA page, the first image we see is the Featured Image----we want the fullblown image (use its link for url)
# we will first visit the webpage/url---a new page opens with full blown image
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
# ## Using buttons

# In[9]:
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
# https://spaceimages-mars.com/image/featured/mars3.jpg

# In[10]:
# parse resulting html with soup
html = browser.html

img_soup = soup(html, 'html.parser')


# In[11]:
# we now need the relative image url
img_url_rel = img_soup.select_one('img',class_='fancybox-image').get('src')

img_url_rel

# In[12]:
# use base URL to create absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# Getting Mars Facts
# We will be scrapping table content
# A table is made up of smaller containers (tbody) nested in the table tag
# tr is the tag for each table---table data is stored in td tags----these esablish the columns

# In[13]:
# instead of scraping each row, we read the html <td> tags using pythons panda
df = pd.read_html('https://galaxyfacts-mars.com')[0]  # this is the mars facts webpage (0 - tells panda to pull first table)

df.columns=['description', 'Mars', 'Earth']

df.set_index('description', inplace=True)

df

# In[14]:
# we will need to add this clean table into a webpage--any changes on the table will be reflected in the webpage
# we will have to turn it back to html using .to_hmtl
df.to_html()
# Shut down the  browser
# Browser should always be shut else it will continue using computer resources

# In[15]:
# to shut down the browser
browser.quit()
# ## Mission to Mars Challenge using Starter Code

# In[16]:
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# In[17]:
# set executable path to NASA Mars News
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
# ### Visiting NASA News Site

# In[18]:
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# In[19]:
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

# In[20]:
slide_elem.find("div", class_='content_title')

# In[21]:
# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# In[22]:
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# JPL Space Featured Image

# In[23]:
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# In[24]:
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# In[25]:
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# In[26]:
# we now need the relative image url
img_url_rel = img_soup.select_one('img',class_='fancybox-image').get('src')

img_url_rel


# In[27]:
# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url
# ## Mars Facts

# In[28]:
df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()

# In[29]:
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df

# In[30]:
# convert the table data back to html code so we can use it in the web
df.to_html()

# In[31]:
# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# In[32]:
# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table)
# ## Scrape High Resolution Hemisphere Images and Titles

# In[33]:
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# In[34]:
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(4):
    #create empty dictionary
    hemispheres = {}
    browser.find_by_css('a.product-item h3')[i].click()
    element = browser.find_by_text('Sample').first
    img_url = element['href']
    title = browser.find_by_css("h2.title").text
    hemispheres["img_url"] = img_url
    hemispheres["title"] = title
    hemisphere_image_urls.append(hemispheres)
    browser.back()


# In[35]:
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# In[36]:
# 5. Quit the browser
browser.quit()

# In[ ]:




