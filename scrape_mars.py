from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


# VISIT SITE - get header and news
    url1 = "https://redplanetscience.com/"
    browser.visit(url1)
    
    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    # news title
    title_info = soup.find_all('div', class_='content_title')
    news_title = title_info[0].text

    # paragraph text
    p_info = soup.find_all('div', class_='article_teaser_body')
    news_p = p_info[0].text


# VISIT SITE - for images
    url2 = "https://spaceimages-mars.com/"
    browser.visit(url2)

    time.sleep(2)

    # Click to full image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')

    # image source
    image = soup.find_all('div', class_='floating_text_area')
    relative_img_path = image[0].a['href']
    featured_img_url = 'https://spaceimages-mars.com/' + relative_img_path
    

# GET FACT Table 
    table = pd.read_html('https://galaxyfacts-mars.com/')
    df = table[1]
    df.columns=['Item', 'Amount']
    
    # Convert to html
    html_table = df.to_html(index=False, header=False)

# URLS for each of the hemispheres

    thumb_link = soup.find_all('div', class_='item')
    imgs_link = []
    for i in thumb_link:
        img_link = i.find('a')['href']
        imgs_link.append('https://marshemispheres.com/' + img_link)



 # VISIT SITE - names of hemispheres 
    url3 = "https://marshemispheres.com/"
    browser.visit(url3)

    time.sleep(2)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_h = []

    results = soup.find_all('div', class_="collapsible results")
    diff_hemi = results[0].find_all('h3')
    for name in diff_hemi:
        mars_h.append(name.text)

   
# Use zip to add dictionaries to list - WORKED WHEN I GOT RID OF THIS
    # mars_zip = zip(mars_h, imgs_link)

    # hemisphere_image_url5 = []

    # for title, img_url in mars_zip:
    
    #     mars_dict = {}
    #     mars_dict['title'] = title
    #     mars_dict['img_url'] = img_url
    
    # hemisphere_image_url5.append(mars_dict)

    # Store in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_img_url,
        "mars_facts": html_table,
        "hemispheres": mars_h, 
        "hemisphere_image": imgs_link
    }

    # Test to see if it works
    print(f'Title: {news_title}')
    print(mars_data)
    # print(featured_image_url, flush=True)
    # print("https://marshemispheres.com/")
   

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__=="__main__":
    scrape_info()
