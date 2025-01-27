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
album = 'High Visceral, Pt. 1'

driver = webdriver.Chrome()
driver.get(url)

'''<input id="site-search" class="search-field" type="text" name="q" placeholder="Search for music…" value="" required="">'''
search_bar = driver.find_element(By.ID, 'site-search')

search_bar.click()
search_bar.send_keys(album)
search_bar.submit()

'''<a href="/music/Frank+Ocean/Blonde" title="Blonde" class="link-block-target">Blonde</a>'''
album = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.LINK_TEXT, album)))
album.click()

html = driver.page_source
driver.save_screenshot('album_page.png')
#print(driver.current_url)

driver.quit()

soup = BeautifulSoup(html, 'html.parser')

artist = soup.find('span', attrs={'itemprop':'name'}).text

metadata = unique(soup.find_all('dd', attrs={'class':'catalogue-metadata-description'}))
#print(metadata)

runtime = metadata[0].text
release = metadata[1].text

album_info = [artist, runtime.strip(), release.strip()]
print(album_info)
