from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from bs4 import BeautifulSoup

def unique(list):
    
    unique_list = []
    
    for i in list:
        if i not in unique_list:
            unique_list.append(i)

    return unique_list

url = 'https://www.last.fm/search/albums'
album = 'RUAB'

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument("--disable-extensions")
options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2,
                                          'profile.managed_default_content_settings.javascript': 2})

driver = webdriver.Chrome(options=options)
driver.get(url)

'''<input id="site-search" class="search-field" type="text" name="q" placeholder="Search for music…" value="" required="">'''
search_bar = driver.find_element(By.ID, 'site-search')
#search_bar = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'site-search')))

search_bar.click()
search_bar.send_keys(album)
search_bar.submit()

'''<a href="/music/Frank+Ocean/Blonde" title="Blonde" class="link-block-target">Blonde</a>'''
album = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, album)))
album.click()

WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'header-new-title')))

html = driver.page_source
driver.save_screenshot('album_page.png')

driver.quit()

soup = BeautifulSoup(html, 'html.parser')

artist = soup.find('span', attrs={'itemprop':'name'}).text

metadata = soup.find_all('dd', attrs={'class':'catalogue-metadata-description'})

try:
    if metadata:
        runtime = metadata[0].text
        release = metadata[1].text
    
        album_info = [artist, runtime.strip(), release.strip()]
        print(album_info)
        
    else:
        album_info = [artist, 'NA', 'NA']
        print(album_info)

except IndexError:
    print('Error')
    