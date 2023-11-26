import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# URL Target
url = "https://wedew.id/tema"

# Inisialisasi webdriver chrome
# Define chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

# Melakukan request get kedalam url target
driver.get(url)

next_page = driver.find_element(
    By.CSS_SELECTOR,
    "body > div.container > div:nth-child(5) > nav > ul > li:last-child",
)

while True:
    button_items = driver.find_elements(
        By.CSS_SELECTOR, "div.row.theme-list > div[data-request-data] > a.theme-item"
    )
    links_item = [link.get_attribute("href") for link in button_items]

    # Melakukakn looping kedalam tiap item theme
    for link_item in links_item:
        driver.get(link_item)
        # Mendapatkan judul template wedding
        title_item = driver.find_element(
            By.CSS_SELECTOR, "body > div.page-header > div > h1"
        ).text

        # Membuat folder untuk menyimpan data template
        save_dir = os.path.join("wedew", title_item)
        os.mkdir(save_dir)

        # Mendownload gambar preview template
        img_desktop = driver.find_element(
            By.CSS_SELECTOR, "div.theme-detail-preview-desktop > img"
        )
        img_mobile = driver.find_element(
            By.CSS_SELECTOR, "div.theme-detail-preview-mobile > img"
        )
        url_img_desktop = img_desktop.get_attribute("src")
        with open(
            os.path.join(
                save_dir, f"{title_item} Desktop.{url_img_desktop.split('.')[-1]}"
            ),
            "wb",
        ) as file:
            file.write(requests.get(url_img_desktop).content)

        url_img_mobile = img_mobile.get_attribute("src")
        with open(
            os.path.join(
                save_dir, f"{title_item} Mobile.{url_img_mobile.split('.')[-1]}"
            ),
            "wb",
        ) as file:
            file.write(requests.get(url_img_mobile).content)

        # Menyimpan tab utama
        main_tab = driver.current_window_handle

        # Melakukan redirect ke halaman preview
        preview_button = driver.find_element(By.LINK_TEXT, "Preview")
        driver.get(preview_button.get_attribute("href"))
        see_full = driver.find_element(By.LINK_TEXT, "Lihat Penuh")
        see_full.click()

        # Dapatkan semua tab
        all_tabs = driver.window_handles

        for tab in all_tabs:
            if tab != main_tab:
                driver.switch_to.window(tab)
                # Menyimpan page source
                with open(
                    os.path.join(save_dir, f"{title_item}.html"), "w", encoding="utf-8"
                ) as file:
                    file.write(driver.page_source)

                driver.close()
                break

        driver.switch_to.window(main_tab)

    if "disabled" not in next_page.get_attribute("class"):
        next_page.click()
    else:
        break

time.sleep(5)
driver.close()
