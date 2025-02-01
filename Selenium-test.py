from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

def webdriver_init():
        
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2,
                                          'profile.managed_default_content_settings.javascript': 2})

    driver = webdriver.Chrome(options=options)
    return driver

def target_html(driver, url, album):
        
    driver.get(url)

    # <input id="site-search" class="search-field" type="text" name="q" placeholder="Search for music…" value="" required="">
    search_bar = driver.find_element(By.ID, 'site-search')
    search_bar.click()
    
    search_bar.send_keys(album)
    search_bar.submit()

    # <a href="/music/Frank+Ocean/Blonde" title="Blonde" class="link-block-target">Blonde</a>
    album = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, album)))
    album.click()

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'header-new-title')))
    html = driver.page_source
    
    driver.save_screenshot('album_page.png')
    driver.quit()
    
    return html

def fetch_album_info(album):
    
    url = 'https://www.last.fm/search/albums'
    
    driver = webdriver_init()

    album_page_html = target_html(driver, url, album)
    soup = BeautifulSoup(album_page_html, 'html.parser')

    artist = soup.find('span', attrs={'itemprop':'name'}).text
    
    tags_list = soup.find_all('li', attrs={'class':'tag'})
    genre_tags = []
    
    for tag in tags_list[:3]:
        genre_tags.append(tag.text)
        
    metadata = soup.find_all('dd', attrs={'class':'catalogue-metadata-description'})

    try:
        if metadata:
            runtime = metadata[0].text
            release = metadata[1].text

            album_info = [artist, runtime.strip(), release.strip(), genre_tags]
            print(album_info)

        else:
            album_info = [artist, 'NA', 'NA', genre_tags]
            print(album_info)

    except IndexError:
        print('Error')

album = str(input('Enter album name to fetch info: '))
fetch_album_info(album)