from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def webdriver_init():
        
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-features=UseChromeML")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
      
    options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2,
                                           'profile.managed_default_content_settings.javascript': 2})

    driver = webdriver.Chrome(options=options)
    
    driver.get('https://www.last.fm/search/albums')
    
    return driver

def hello(driver, album):
    
    search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'site-search')))
    search_bar.click()
    
    search_bar.send_keys(album)
    search_bar.submit()
    
    right_tab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mantle_skin"]/div[2]/div/div[3]/nav/ul/li[3]/a')))
    right_tab.click()
    
    album = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, album)))
    album.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'header-new-title')))
    html = driver.page_source
    # driver.save_screenshot('album_page.png')
    
    reset = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Last.fm')))
    reset.click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'spike_intro')))
    return_to_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'masthead-search-toggle')))
    return_to_search.click()
    
    driver.save_screenshot('album_page.png')
    
    return html

album = ['Insano', 'Blonde', 'Continuum', 'Room for Squares', 'Heavier Things']

hi = webdriver_init()

for i in album:
    hello(hi, i)
    
# {
#     "music project": [],
#     "artist": [],
#     "spotify logged": [],
#     "runtime": [],
#     "release date": [],
#     "genre tags": []
# }
