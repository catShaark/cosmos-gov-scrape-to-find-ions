import re


from bs4 import BeautifulSoup
from selenium import webdriver

import time

# url of the page we want to scrape
url = "https://cosmoshub-1.bigdipper.live/validator/"





def get_validator_acc(hub_version,valoper):
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('/home/khanh/chromedriver')
    driver.get(url.replace("1", str(hub_version)) + valoper)






    # this is just to ensure that the page is loaded
    time.sleep(5)

    html = driver.page_source

    # this renders the JS code and stores all
    # of the information in static HTML code.

    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")
    driver.close()
    return soup.find('a', {'href': re.compile("/account/cosmos*")}).contents[0]







