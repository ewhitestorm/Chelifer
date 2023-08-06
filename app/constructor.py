from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pydantic import BaseModel
from user_agent import UserAgent
from translation import Data, City



class ItemOut(BaseModel):
    city: str
    rubric: str
    num: int


class Constructor:
    def info_about_city(city_id, city):
        options = Options()
        options.add_argument(f"headers={UserAgent()}")
        options.headless = True
        browser = webdriver.Chrome(options=options)
        browser.get(Data.opener("web_links.json")["realty"] + city_id + f'/{Data.opener("categories.json")["type"][2]}')
        city = City.translate_city(city_id)
        try:
            elems = browser.find_elements(by=By.CSS_SELECTOR, value='div[data-marker="page-title"]')
            for item in elems:
                rubric = item.find_element(by=By.CSS_SELECTOR, value='h1[data-marker="page-title/text"]').text
                number = item.find_element(by=By.CSS_SELECTOR, value='span[data-marker="page-title/count"]').text
                num = int(''.join(number.split()))
                break
            return (ItemOut.model_validate({
                "city": city,
                "rubric": rubric,
                "num": num
                }))
        finally:
            browser.quit()