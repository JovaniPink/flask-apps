#!/usr/bin/env python3

# Import Splinter and BeautifulSoup
# https://splinter.readthedocs.io/en/latest/#
from splinter import Browser

# https://beautiful-soup-4.readthedocs.io/en/latest/
from bs4 import BeautifulSoup as soup

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html
import pandas as pd

# https://docs.python.org/3/library/datetime.html
import datetime as dt

from app import app, mongo, celery


@celery.task(bind=True)
def scrape_all(self):
    with app.app_context():
        # This is important, I'm running a celery.task to run the scraping request
        # in the background of the app and not hold up the response. But also updating
        # the frontend with statuses of the computation to show the user feedback.
        # https://www.distributedpython.com/2018/09/28/celery-task-states/
        self.update_state(state="PENDING")

        # Initiate headless driver for deployment
        browser = Browser("chrome", executable_path="chromedriver", headless=True)

        news_title, news_paragraph = mars_news(browser)

        # Run all scraping functions and store results in a dictionary
        store_data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "hemispheres": hemispheres(browser),
            "last_modified": dt.datetime.now(),
        }

        # Stop webdriver and return data
        browser.quit()

        # Call the upsert within the worker
        mongo.db.mars_app.update({}, store_data, upsert=True)

        # Update that the function was completed.
        self.update_state(state="SUCCESS")

        return "Scraping Successful!"


def mars_news(browser):
    # ### Scrape Mars News
    # Visit the mars nasa news site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, "html.parser")

    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        slide_elem.find("div", class_="content_title")

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_="content_title").get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # ### Featured Images
    # Visit URL
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id("full_image")
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_elem = browser.links.find_by_partial_text("more info")
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, "html.parser")

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one("figure.lede a img").get("src")
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"

    return img_url


def mars_facts():
    #### Mars Facts
    try:
        # Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' .read_html() function.
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        return None

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html
    return df.to_html()


def scrape_hemisphere(html_text):
    # parse html text
    hemisphere_soup = soup(html_text, "html.parser")

    try:
        title_elem = hemisphere_soup.find("h2", class_="title").get_text()
        sample_elem = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None

    return {"title": title_elem, "img_url": sample_elem}


def hemispheres(browser):
    #### Hemispheres
    # Visit URL
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_url = []

    for i in range(4):
        browser.find_by_css("a.product-item h3")[i].click()
        hemisphere_data = scrape_hemisphere(browser.html)
        hemisphere_image_url.append(hemisphere_data)
        browser.back()

    return hemisphere_image_url
