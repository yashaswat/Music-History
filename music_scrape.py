import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import undetected_chromedriver as uc

def webdriver_init(url='https://www.last.fm/search/albums'):
    
    # List of User-Agent strings
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
]

    random_agent = random.choice(user_agents)
        
    options = uc.ChromeOptions()
    # options.add_argument('--headless=new')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-features=UseChromeML")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=1")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-software-rasterizer")
    
    options.add_argument(f'user-agent={random_agent}')
    
    options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2,
                                          'profile.managed_default_content_settings.javascript': 2})

    driver = uc.Chrome(options=options)
    driver.get(url)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def target_html(driver, album):

    wait = WebDriverWait(driver, 10)
    
    # <input id="site-search" class="search-field" type="text" name="q" placeholder="Search for music…" value="" required="">
    search_bar = wait.until(EC.presence_of_element_located((By.ID, 'site-search')))
    search_bar.click()
    
    search_bar.send_keys(album)
    search_bar.submit()
    
    album_tab = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mantle_skin"]/div[2]/div/div[3]/nav/ul/li[3]/a')))
    album_tab.click()

    # <a href="/music/Frank+Ocean/Blonde" title="Blonde" class="link-block-target">Blonde</a>
    album = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, album)))
    album.click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header-new-title')))
    html = driver.page_source
    driver.save_screenshot('Screenshots/album_page.png')
    
    homepage_return = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Last.fm')))
    homepage_return.click()
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'spike_intro')))
    
    back_to_searchbar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'masthead-search-toggle')))
    back_to_searchbar.click()
    
    driver.save_screenshot('Screenshots/reset.png')
    
    return html

def fetch_album_info(driver, album):
    
    album_page_html = target_html(driver, album)
    soup = BeautifulSoup(album_page_html, 'html.parser')

    artist = soup.find('span', attrs={'itemprop':'name'}).text
    
    tags_list = soup.find_all('li', attrs={'class':'tag'})
    genre_tags = []
    
    for tag in tags_list[:5]:
        genre_tags.append(tag.text)
        
    metadata = soup.find_all('dd', attrs={'class':'catalogue-metadata-description'})

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
    
    test_album = str(input('Enter Album to search: '))
    driver = webdriver_init()

    album = ['Insano', 'Blonde', 'Continuum', f'{test_album}', 'Room for Squares', 'Heavier Things']

    for album in album:
        fetch_album_info(driver, album)