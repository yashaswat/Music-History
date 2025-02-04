from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

def webdriver_init(url='https://www.last.fm/search/albums'):
        
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-features=UseChromeML")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2,
                                          'profile.managed_default_content_settings.javascript': 2})

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    return driver

def target_html(driver, album):

    # <input id="site-search" class="search-field" type="text" name="q" placeholder="Search for music…" value="" required="">
    search_bar = driver.find_element(By.ID, 'site-search')
    search_bar.click()
    
    search_bar.send_keys(album)
    search_bar.submit()
    
    album_tab = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mantle_skin"]/div[2]/div/div[3]/nav/ul/li[3]/a')))
    album_tab.click()

    # <a href="/music/Frank+Ocean/Blonde" title="Blonde" class="link-block-target">Blonde</a>
    album = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, album)))
    album.click()

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'header-new-title')))
    html = driver.page_source
    driver.save_screenshot('Screenshots/album_page.png')
    
    homepage_return = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.LINK_TEXT, 'Last.fm')))
    homepage_return.click()
    
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'spike_intro')))
    
    back_to_searchbar = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'masthead-search-toggle')))
    back_to_searchbar.click()
    
    driver.save_screenshot('Screenshots/reset.png')
    
    return html

def fetch_album_info(driver, album):
    
    album_page_html = target_html(driver, album)
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
driver = webdriver_init()

album = ['Insano', 'Blonde', 'Continuum', 'Room for Squares', 'Heavier Things']

for album in album:
    fetch_album_info(driver, album)