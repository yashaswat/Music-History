from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import selenium

url = 'https://genius.com/'

driver = webdriver.Chrome()
driver.get(url)

print(driver.find_element(By.NAME, 'q'))
'''<input name="q" placeholder="Search lyrics &amp; more" autocomplete="off" required="" class="PageHeaderSearch-desktop-sc-4bc00535-2 jZunYq">'''