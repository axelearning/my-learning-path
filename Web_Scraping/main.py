from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

ROOT_URL = "https://www.schoolmouv.fr/"
YEARS = ["6eme", "5eme", "4eme", "3eme", "Seconde", "1ere", "Terminale"]

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=options)

# iterate over each years
chapter_by_years = {}
for year in YEARS:
    driver.get(f"{ROOT_URL}{year}")
    chapter_by_years[year] = {}

    # iterate ever each subject
    for subject in driver.find_elements_by_class_name("subject-content"):
        if subject.is_displayed():
            driver.execute_script("arguments[0].click();", subject)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            subject_name = soup.find("h1", class_="breadcrumb-title").get_text()
            chapter_by_years[year][subject_name] = []
            # iterate over each chapter
            for chapter in soup.findAll("div", class_="chapter"):
                # collect the title of each chapter
                title = chapter.h2.contents[-1].get_text()
                chapter_by_years[year][subject_name].append(title)

# Save as JSON
with open("chapters.json", "w") as file:
    json.dump(chapter_by_years, file)
