from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

url = 'https://www.last.fm/search/albums'
album = 'Blonde'

driver = webdriver.Chrome()
driver.get(url)

'''<input id="site-search" class="search-field" type="text" name="q" placeholder="Search for music…" value="" required="">'''
search_bar = driver.find_element(By.ID, 'site-search')

search_bar.click()
search_bar.send_keys(album)
search_bar.submit()

'''<a href="/music/Frank+Ocean/Blonde" title="Blonde" class="link-block-target">Blonde</a>'''
#album = driver.find_element(By.CLASS_NAME, 'link-block-target')
album = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, album)))
album.click()

html = driver.page_source
#driver.save_screenshot('album_page.png')
#print(driver.current_url)

driver.quit()
