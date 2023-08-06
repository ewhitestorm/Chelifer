import re
import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By



class Data:
    def opener(file_name):
        with open(f"atributs/{file_name}") as f:
            return json.load(f)


class City:
    def make_translit(item):
        if item.isalpha() == False:
            if item.count('-') != 0:
                for v in Data.opener("exceptions.json").values():
                    if v in item:
                        item = item.replace('-', '_')
                        break
                    else:
                        continue
        return item
    
    
    def name_check(item, browser, interpreter_to_translit, interpreter_from_translit):
        if re.search(r'[^a-zA-Z]', item[0]):
            if browser != None:
                return browser.get(Data.opener("web_links.json")[interpreter_to_translit])
            else:
                return City.make_translit(item).title()
        else:
            if browser != None:
                return browser.get(Data.opener("web_links.json")[interpreter_from_translit])
            else:
                return City.make_translit(item)
    
    
    def translate_city(name):
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Chrome(options=options)
        City.name_check(
            item=name, 
            browser=browser, 
            interpreter_to_translit="interpreter_to_translit", 
            interpreter_from_translit="interpreter_from_translit"
            )
        try:
            locator = browser.find_element(By.NAME, "in")
            locator.send_keys(name)
            browser.find_element(By.XPATH, "//input[@name='translate'][@type='submit']").click()
            elem = browser.find_element(by=By.CSS_SELECTOR, value='textarea[id="out"]').text
            return City.name_check(
                item=elem, 
                browser=None, 
                interpreter_to_translit=None, 
                interpreter_from_translit=None
                )
        finally:
            browser.quit()