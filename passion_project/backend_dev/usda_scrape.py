import argparse
import yaml
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import json

"""
def GetSpeciesData(html, attributes, common_name, species_dict):
    species_dict[common_name] = {}
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_="usa-table")
    for attribute in attributes:    
        for table in tables:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if cells and cells[0].text.strip() == attribute:
                    species_dict[common_name][attribute]= cells[1].text.strip()
                    break   
    return species_dict
"""

def GoToCharacteristics(attributes, species_list):
    service = Service('/usr/bin/chromedriver')

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # <-- this runs Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")   # recommended for Linux (optional)
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems (optional)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    #driver = webdriver.Chrome(service=service)

    species_dict = {}
    for common_name in species_list:
        driver.get('https://plants.usda.gov/')
        try:
            wait10 = WebDriverWait(driver, 10)
            wait5 = WebDriverWait(driver, 10)

            search_bar = wait10.until(EC.presence_of_element_located((By.ID, 'find-plant')))
            search_bar.clear()
            search_bar.send_keys(common_name)

            time.sleep(1)
            search_bar.send_keys(Keys.ARROW_DOWN)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(1)

            button = wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                "button.usa-button.usa-button--outline.usa-button--inverse")))
            button.click()

            button = wait10.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Characteristics']")))
            button.click()

            # Wait for specific content in the tab to appear
            wait10.until(EC.presence_of_element_located((By.XPATH, "//table")))  # update this to match your content

            html = driver.page_source
            species_dict = GetSpeciesData(html, attributes, common_name, species_dict)

        except TimeoutException:
            print(common_name+',')
            continue
    
    driver.quit()
    print(species_dict)
    return species_dict

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='species_attributes.yml',
                         help='Path to yml with species and attributes you want to scrape from https://plants.usda.gov/')
    args, remaining_argv = parser.parse_known_args()

    defaults = {}
    if os.path.exists(args.config):
        defaults = load_config(args.config)
    
    parser = argparse.ArgumentParser(description='Scrape https://plants.usda.gov/ for attributes of plants with species symbol')
    parser.add_argument('--species', type=str, nargs='*', default=defaults.get('species'),
                        help='Plant species symbol (AMCA3, etc...)')
    parser.add_argument('--attributes', type=str, nargs='*', default=defaults.get('attributes'),
                        help = 'Plant attributes from species characteristics tab on https://plants.usda.gov/')
    
    args = parser.parse_args(remaining_argv)
    
    species_dict = GoToCharacteristics(args.attributes, args.species)

    with open('species_data.json', 'w') as f:
        json.dump(species_dict, f, indent=2)

if __name__ == '__main__':
    main()