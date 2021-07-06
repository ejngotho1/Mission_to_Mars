
# import depedencie
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set executable path to NASA Mars News
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# In[3]:
# letss visit the url
url = 'https://redplanetscience.com'

# instruct bs4 to visit url
browser.visit(url)

# use an optional clause to delay loading the page
# first look for elements with combination of <div> and <list_text>-----e.g. (ul.item_list) found as (<ul class='item_list')
# also tells  browser to wait for 1 sec before searching components

browser.is_element_present_by_css('div.list_text', wait_time=1) 

# In[4]:
# next we will tell bs4 to parse/analyse (using html.parser) text and store in an object (news_soup)

html = browser.html

news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')   # variable looks for <div> and its descedants (other elements within <div>)
                                                     # div.select one points to <div> with class 'list_text' li
   
# In[5]:
# we have our text/code in slide_elem---we will look for <div> element and class=content_title in this variable

slide_elem.find('div', class_='content_title')   # output is an html containing content title inside <div. element

# In[6]:
# the title is somewhere in the html code... thats all we need not the html stuff
# first we will find <a> tag and save it in an object ---news_title
news_title = slide_elem.find('div', class_='content_title').get_text()    # .get_text only returns the text

news_title
# In[7]:
# now lets look for the summary (teser) using find
# when we find 'teser' from DevTools we get the first summary/teser----article_teaser_body
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p
# Featured Images
# after scraping text, lets now add images
# In[8]:
# when we open the NASA page, the first image we see is the Featured Image----we want the fullblown image (use its link for url)
# we will first visit the webpage/url---a new page opens with full blown image
url = 'https://spaceimages-mars.com'
browser.visit(url)
# Using buttons
# In[9]:
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
# https://spaceimages-mars.com/image/featured/mars3.jpg

# In[12]:
# parse resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
# In[13]:
# we now need the relative image url
img_url_rel = img_soup.find('img',class_='fancybox-image').get('src')
img_url_rel
# In[14]:
# use base URL to create absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url
#----------------------------------------------------------------------------------
# ## Getting Mars Facts
# ### We will be scrapping table content
# ### A table is made up of smaller containers (tbody) nested in the table tag
# ###  tr is the tag for each table---table data is stored in td tags----these esablish the columns

# In[16]:
# instead of scraping each row, we read the html <td> tags using pythons panda
df = pd.read_html('https://galaxyfacts-mars.com')[0]  # this is the mars facts webpage (0 - tells panda to pull first table)

df.columns=['description', 'Mars', 'Earth']

df.set_index('description', inplace=True)

df
# In[18]:
# we will need to add this clean table into a webpage--any changes on the table will be reflected in the webpage
# we will have to turn it back to html using .to_hmtl
df.to_html()

# Shut down the  browser
# Browser should always be shut else it will continue using computer resources

# In[19]:
# to shut down the browser
browser.quit()
