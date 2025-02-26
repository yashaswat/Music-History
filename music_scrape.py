import random
import time
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import undetected_chromedriver as uc


# loading a random user agent for avoiding bot detection
def load_user_agent():
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
]
    return random.choice(user_agents)


# set-up webdriver options
def load_options(random_agent):
    
    options = uc.ChromeOptions()
    
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-features=UseChromeML")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=1")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-software-rasterizer")
    
    options.add_argument(f'user-agent={random_agent}')
    
    # block javascript and images
    options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2,
                                          'profile.managed_default_content_settings.javascript': 2})
    
    return options


# initialize webdriver with agent and options
def webdriver_init(url='https://www.last.fm/search/albums'):

    random_agent = load_user_agent()

    driver = uc.Chrome(options=load_options(random_agent), headless=True)
    driver.get(url)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# go to album page on last.fm, get html code and reset
def target_html(driver, album):

    wait = WebDriverWait(driver, 5)
    
    # click on the search bar
    search_bar = wait.until(EC.presence_of_element_located((By.ID, 'site-search')))
    search_bar.click()
    
    # clear existing text and enter album name
    search_bar.clear()
    search_bar.send_keys(album)
    search_bar.submit()
    
    # go to the "album" tab on search
    album_tab = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mantle_skin"]/div[2]/div/div[3]/nav/ul/li[3]/a')))
    album_tab.click()
    
    time.sleep(1)
    
    # click album
    album = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, album)))
    album.click()
    
    # wait for page load and fetch html
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header-new-title')))
    html = driver.page_source
    driver.save_screenshot('Screenshots/album_page.png')
    
    time.sleep(1)
    
    # return to site home page
    homepage_return = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Last.fm')))
    homepage_return.click()
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'spike_intro')))
    
    # reset to search bar
    back_to_searchbar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'masthead-search-toggle')))
    back_to_searchbar.click()
    
    time.sleep(1)
    
    driver.save_screenshot('Screenshots/reset.png')
    
    return html

# extract relevant info about album from html
def fetch_album_info(driver, album):

    album_page_html = target_html(driver, album)
    soup = BeautifulSoup(album_page_html, 'html.parser')

    artist = soup.find('span', attrs={'itemprop':'name'}).text # artist name
    
    tags_list = soup.find_all('li', attrs={'class':'tag'}) # all genre tags
    genre_tags = []
    
    for tag in tags_list[:5]:
        genre_tags.append(tag.text)
        
    metadata = soup.find_all('dd', attrs={'class':'catalogue-metadata-description'}) # runtime and release date

    try:
        if metadata:
            runtime = metadata[0].text
            release = metadata[1].text

            album_info = [artist, runtime.strip(), release.strip(), genre_tags]
            return album_info

        else:
            album_info = [artist, 'NA', 'NA', genre_tags]
            return album_info

    except IndexError:
        print('Error')


if __name__ == '__main__':
    
    # testing code
    
    test_album = str(input('Enter Album to search: '))
    driver = webdriver_init()

    album = ['Insano', 'Blonde', 'Continuum', f'{test_album}', 'Room for Squares', 'Heavier Things']

    for album in album:
        fetch_album_info(driver, album)