import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# URL Target
url = "https://wedew.id/tema"
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options)
driver.implicitly_wait(10)
driver.get(url)

# try:
#     next_page = driver.find_element(
#         By.CSS_SELECTOR,
#         "nav > ul.pagination > li.page-item > a[aria-label='pagination.next']",
#     )
#     driver.get(next_page.get_attribute('href'))
# except:
#     print('Tidak ada')

# print(next_page.click())

# while True:
#     try:
#         next_page = driver.find_element(
#             By.CSS_SELECTOR,
#             "nav > ul.pagination > li.page-item > a[aria-label='pagination.next']",
#         )
#         link_next_page = next_page.get_attribute('href')
#         print(link_next_page)
#         driver.get(link_next_page)
#     except NoSuchElementException:
#         print('selesai...')
#         break

while True:
    try:
        current_url = driver.current_url
        next_page = driver.find_element(
            By.CSS_SELECTOR,
            "nav > ul.pagination > li.page-item > a[aria-label='pagination.next']",
        )
        link_next_page = next_page.get_attribute('href')
        button_items = driver.find_elements(
            By.CSS_SELECTOR, "div.row.theme-list > div[data-request-data] > a.theme-item"
        )
        links_item = [link.get_attribute("href") for link in button_items]
        for link_item in links_item:
            driver.get(link_item)
            title_item = driver.find_element(
                By.CSS_SELECTOR, "body > div.page-header > div > h1"
            ).text
            print(title_item)
        print(link_next_page)
        driver.get(link_next_page)
    except NoSuchElementException:
        print('Selesai ...')
        break

# next_page.click()
# if "disabled" not in next_page.get_attribute("class"):
#     next_page.click()
#     print('bisa di klik')
# else:
#     print('tidak bisa di klik')
#     break

time.sleep(5)
driver.quit()
