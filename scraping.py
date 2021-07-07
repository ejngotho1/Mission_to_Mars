
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# In[2]
# define function to initialize browser, create dictionary and exit the browser

def scrape_all():

# set executable path to NASA Mars News
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # srtting our news and paragraph variables
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
       "news_title": news_title,
       "news_paragraph": news_paragraph,
       "featured_image": featured_image(browser),
       "facts": mars_facts(),
       "last_modified": dt.datetime.now()
    }
    # stop wbdriver and return data
    browser.quit()
    return data
# In[3]:

def mars_news(browser):

# lets visit the url
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

# add try/except for error handling
    try:    
        slide_elem = news_soup.select_one('div.list_text')   # variable looks for <div> and its descedants (other elements within <div>)
                                                     # div.select one points to <div> with class 'list_text' li
  
# In[5]:
# we have our text/code in slide_elem---we will look for <div> element and class=content_title in this variable
        slide_elem.find('div', class_='content_title')   # output is an html containing content title inside <div. element

# In[6]:
# the title is somewhere in the html code... thats all we need not the html stuff
# first we will find <a> tag and save it in an object ---news_title
        news_title = slide_elem.find('div', class_='content_title').get_text()    # .get_text only returns the text

# In[7]:
# now lets look for the summary (teser) using find
# when we find 'teser' from DevTools we get the first summary/teser----article_teaser_body
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# In[8]:

# FEATURED IMAGE

# when we open the NASA page, the first image we see is the Featured Image----we want the fullblown image (use its link for url)
# we will first visit the webpage/url---a new page opens with full blown image
def featured_image(browser):    
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
# ## Using buttons

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
    try:
        img_url_rel = img_soup.find('img',class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
# In[14]:
# use base URL to create absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ## Getting Mars Facts
# ### We will be scrapping table content
# ### A table is made up of smaller containers (tbody) nested in the table tag
# ###  tr is the tag for each table---table data is stored in td tags----these esablish the columns

#In[16]:

# MARS FACTS

def mars_facts():

    try:
# instead of scraping each row, we read the html <td> tags using pythons panda
        df = pd.read_html('https://galaxyfacts-mars.com')[0]  # this is the mars facts webpage (0 - tells panda to pull first table)

    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']

    df.set_index('description', inplace=True)

    # convert dataframe into html format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # if running a script, print scraped data
    print(scrape_all()) 