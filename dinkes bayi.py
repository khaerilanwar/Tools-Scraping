import time
import math
import requests
from libs.database import Database
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

# Define database SQL
db = Database("localhost", "root", "", "dinkes")

# Define requirements url to scrapping process
url_target = "https://ekohort.kemkes.go.id/login.php"
url_login = "https://ekohort.kemkes.go.id/xxxxxx"
url_after_login = "https://ekohort.kemkes.go.id/xxxxxxxxxx"
url_data_anak = "https://ekohort.kemkes.go.id/xxxxxxxxx"
url_page_data = "https://ekohort.kemkes.go.id/xxxxxxxxx"

# Define chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")

# Define chrome webdriver
driver = webdriver.Chrome(options=chrome_options)

# Use web driver wait while scrapping process
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(10)

# Name Input
# Provinsi = prov_id
# Kabupaten = kab_id
# Username = username
# Password = password

# Melakukan Login dengan Method Post Requests
data_login = {
    "prov_id": "xx",
    "kab_id": "xxxx",
    "username": "xxxxx",
    "password": "xxxxxxx",
}

# Kirim permintaan POST
response = requests.post(url_login, data=data_login)

if response.status_code == 200:
    print("Login Berhasil")
else:
    print("Login Gagal")

cookies = response.cookies

driver.get(url_after_login)

# Set cookie dari response
for cookie in cookies:
    driver.add_cookie({"name": cookie.name, "value": cookie.value})

# Getting to url data bayi
driver.get(url_data_anak)

# Memulai Scraping Data
total_data = (
    BeautifulSoup(driver.page_source, "html.parser")
    .select(
        "#panel-1 > div.panel-container.show > div > div > div.box.box-widget.widget-user-2 > div > h5 > i > span"
    )[0]
    .text
)

much_page = 294
max_much_page = math.ceil(int(total_data) / 10) - 4
num_data_page = 10000
num_data = 0
for x in range(much_page):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # button_next = driver.find_element(By.LINK_TEXT, "Next")
    table_container = soup.find("form", {"id": "form_rf_m_bayi"})
    # Temukan semua elemen <tr> yang merupakan anak langsung dari elemen <tbody>
    row_elements = table_container.select("#tbody_rf_m_bayi > tr")

    for row_element in row_elements:
        column = 0
        column_elements = row_element.find_all(recursive=False)
        clean_bayi_data = {}
        clean_nakes_data = {}
        for column_element in column_elements:
            # Action if column contain nakes data
            if column == 1:
                nakes_tables = column_element.find_all("table")
                key_nakes_data = ["penolong", "nakes"]
                iterate_number_key = 0
                for nakes_table in nakes_tables:
                    nakes_rows = nakes_table.find("tbody").find_all("tr")
                    nakes_data = {}
                    if nakes_rows:
                        for nakes_row in nakes_rows:
                            nakes_columns = nakes_row.find_all("td")
                            key = (
                                nakes_columns[0].text.strip().lower().replace(" ", "_")
                            )
                            value = (
                                nakes_columns[1].text.strip().lower().replace(" ", "_")
                            )
                            nakes_data[key] = value
                        else:
                            clean_nakes_data[
                                key_nakes_data[iterate_number_key]
                            ] = nakes_data
                        iterate_number_key += 1
                    else:
                        pass

            # Action if column contain bayi data part 1
            elif column == 2:
                # Define text from column element, clean teks from more space and split text with new line
                text_bayi_data = column_element.text.strip().split("\n")
                # Clean text bayi data from text null
                text_bayi_data = [item for item in text_bayi_data if item != ""]
                # Clean more space with each string from list data
                for i in range(len(text_bayi_data)):
                    text_bayi_data[i] = text_bayi_data[i].strip()

                text_clean_bayi_data = []
                for data_clean in text_bayi_data:
                    text_clean_bayi_data.append(data_clean)
                    if "Kelurahan" in data_clean:
                        break

                # Prepare data for add bayi data to dictionary data
                for item_data_bayi in text_clean_bayi_data:
                    key, value = item_data_bayi.split(":", 1)
                    key = key.strip().lower().replace(" ", "_")
                    value = value.strip()
                    clean_bayi_data[key] = value
                    clean_bayi_data["no_hp_penolong"] = (
                        clean_nakes_data["penolong"]["no_hp"]
                        if clean_nakes_data.get("penolong")
                        else None
                    )

                    clean_bayi_data["no_hp_nakes"] = (
                        clean_nakes_data["nakes"]["no_hp"]
                        if clean_nakes_data.get("nakes")
                        else None
                    )

            # Action if column contain bayi data part 2
            elif column == 3:
                # Getting element status and convert them to text
                status_element = column_element.select("table > thead > tr")[0].find(
                    "td"
                )
                text_data_status = status_element.text
                # Clean text data status
                text_data_status = text_data_status.strip().split("\n")
                text_data_status = [item for item in text_data_status if item != ""]
                for j in range(len(text_data_status)):
                    text_data_status[j] = text_data_status[j].strip()
                text_data_status = text_data_status[2:6]
                # Prepare status data bayi for add to clean bayi data
                for item_data_status in text_data_status:
                    key, value = item_data_status.split(":", 1)
                    key = key.strip().lower().replace(" ", "_")
                    value = value.strip()
                    clean_bayi_data[key] = value
            column += 1
        num_data += 1

        # Add Record to database
        # Add record data bayi
        db.insert("data_bayi", clean_bayi_data)
        print(f"{str(num_data).zfill(5)}. Menambahkan : {clean_bayi_data['nama_bayi']}")
        print(20 * "-")

        # Add record data penolong and nakes
        try:
            if clean_nakes_data["penolong"]:
                db.insert("data_penolong", clean_nakes_data["penolong"])
        except:
            pass

        try:
            if clean_nakes_data["nakes"]:
                db.insert("data_nakes", clean_nakes_data["nakes"])
        except:
            pass
    driver.get(f"https://ekohort.kemkes.go.id/xxxxx/{num_data_page}?xxxxxxx")
    num_data_page += 10

print("Program selesai, menutup program....")
time.sleep(5)

driver.quit()
