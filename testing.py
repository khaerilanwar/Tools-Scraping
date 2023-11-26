import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# URL Target
url = "https://wedew.id/tema"
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options)
driver.implicitly_wait(10)
driver.get(url)
next_page = driver.find_element(
    By.CSS_SELECTOR,
    "body > div.container > div:nth-child(5) > nav > ul > li:last-child",
)
# while True:
#     button_items = driver.find_elements(
#         By.CSS_SELECTOR, "div.row.theme-list > div[data-request-data] > a.theme-item"
#     )
#     links_item = [link.get_attribute("href") for link in button_items]
#     for link_item in links_item:
#         driver.get(link_item)
#         title_item = driver.find_element(
#             By.CSS_SELECTOR, "body > div.page-header > div > h1"
#         ).text
#         print(title_item)
#     if "disabled" not in next_page.get_attribute("class"):
#         next_page.click()
#     else:
#         break
time.sleep(5)
driver.quit()
