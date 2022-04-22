from cgi import test
from json import load
from xml.dom import NotFoundErr
from selenium import webdriver
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import uuid

class Web_Scraper:

    def __init__(self, url):
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        
    def accept_Cookies(self):
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            accept_cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            accept_cookies_button.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")

    def load_More_Products(self):
        delay = 20
        while True:
            try:
                WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="Styles__Button-sc-1kpnvfh-4 cRnfyG Styles__PaginationButton-sc-1kf2zc1-1 hBnwhL"]')))
                load_More_Button = self.driver.find_element_by_xpath('//*[@class="Styles__Button-sc-1kpnvfh-4 cRnfyG Styles__PaginationButton-sc-1kf2zc1-1 hBnwhL"]')
            except:
                break
            else:
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight) - 1200);")
                load_More_Button.click()

    def get_product_types(self):
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collections"]')))
            catagory_container = self.driver.find_element_by_xpath('//*[@id="collections"]') # XPath corresponding to the Container
            product_Type_Button = catagory_container.find_element_by_xpath('./button')
            product_Type_Button.click()
        except TimeoutException:
            print("Loading took too much time!")

        checkbox_list = catagory_container.find_elements_by_xpath('.//*[@class="Styles__Checkbox-sc-9kless-1 eLKrVj"]')
        print(f'There are {len(checkbox_list)} catagories on this page')
        return product_Type_Button, checkbox_list

    def get_Product_Links(self):
        prod_container = self.driver.find_element_by_xpath('//*[@class="Styles__Grid-sc-1hr3n2q-0 ekxOoE"]') # XPath corresponding to the Container
        prod_list = prod_container.find_elements_by_xpath('./article')
        link_list = []
        for product in prod_list:
            a_tag = product.find_element_by_tag_name('a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        print(f'There are {len(link_list)} Products on this page')
        print(link_list)
        return link_list

    def generate_ID(link_list):
        id_list = []
        uuid_list = []
        for link in link_list:
            idx = link.find('gymshark-', 0, len(link))
            id_list.append(link[idx:len(link)])
            uuid_list.append(str(uuid.uuid4()))
        return id_list, uuid_list
            
    def start_crawl(self):
        self.accept_Cookies()
        product_Type_Button, checkbox_list = self.get_product_types()
        for checkbox in checkbox_list:
            time.sleep(2)
            checkbox.click()
            product_Type_Button.click()
            self.load_More_Products()
            link_list = self.get_Product_Links()
            id_list, uuid_list = self.generate_ID(link_list)
            self.driver.execute_script("window.scrollTo(0, 0);")
            product_Type_Button.click()
            time.sleep(2)
            checkbox.click()

if __name__ == '__main__':
    mens_URL = "https://uk.gymshark.com/collections/all-products/mens"
    womens_URL = "https://uk.gymshark.com/collections/all-products/womens"
    mens_Catalogue = Web_Scraper(mens_URL)
    mens_Catalogue.start_crawl()
    #womens_Catalogue = Web_Scraper(womens_URL)
    #womens_Catalogue.start_crawl()