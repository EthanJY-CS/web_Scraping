from math import prod
from tabnanny import check
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import uuid
from pathlib import Path
import json
import requests

class Web_Scraper:

    def __init__(self, url):
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        self.root_Path = "/home/ethanjy/Scratch/web_Scraping/raw_data"
        
    def create_folder(self, path):
        Path(self.root_Path + path).mkdir(parents=True, exist_ok=True)
    
    def download_Image(self, image_url, image_name):
        img_data = requests.get(image_url).content
        self.create_folder("/images")
        with open(self.root_Path + '/images/' + image_name + '.jpg', 'wb') as handler:
            handler.write(img_data)

    def accept_Cookies(self):
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            accept_cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            accept_cookies_button.click()
        except TimeoutException:
            print("Loading took too much time!")

    def load_More_Products(self):
        for i in range(1):
            try:
                load_More_Button = self.driver.find_element_by_xpath('//*[@class="Styles__Button-sc-1kpnvfh-4 cRnfyG Styles__PaginationButton-sc-1kf2zc1-1 hBnwhL"]')
            except:
                break
            else:
                self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight) - 1200);")
                load_More_Button.click()
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_product_types(self):
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collections"]')))
            catagory_container = self.driver.find_element_by_xpath('//*[@id="collections"]')
            product_Type_Button = catagory_container.find_element_by_xpath('./button')
            product_Type_Button.click()
        except TimeoutException:
            print("Loading took too much time!")

        checkbox_list = catagory_container.find_elements_by_xpath('.//*[@class="Styles__Checkbox-sc-9kless-1 eLKrVj"]')
        print(f'There are {len(checkbox_list)} catagories on this page')
        return product_Type_Button, checkbox_list

    def get_Product_Links(self):
        prod_container = self.driver.find_element_by_xpath('//*[@class="Styles__Grid-sc-1hr3n2q-0 ekxOoE"]')
        prod_list = prod_container.find_elements_by_xpath('./article')
        link_list = []
        for product in prod_list:
            a_tag = product.find_element_by_tag_name('a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        print(f'There are {len(link_list)} Products on this page')
        return link_list

    def generate_ID(self, link):
        idx = link.find('gymshark-', 0, len(link))
        id = link[idx:len(link)]
        uu_ID = str(uuid.uuid4())
        return id, uu_ID
    
    def scrape_Data(self, link_HTML):
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="Styles__LeftColumn-lpqwbz-2 danMny"]')))
        except TimeoutException:
            print("Loading took too much time!")
        
        images_container = self.driver.find_element_by_xpath('//*[@class="Styles__LeftColumn-lpqwbz-2 danMny"]')
        details_container = self.driver.find_element_by_xpath('//*[@class="Styles__RightColumn-lpqwbz-3 beeZhk"]')

        #Scrape Images
        image_list = images_container.find_elements_by_xpath('.//*[@class="Styles__Image-sc-176u4ag-1 etChzz"]')
        image_links = []
        for idx, image in enumerate(image_list):
            try:
                img_tag = image.find_element_by_tag_name('img')
            except:
                pass
            link = img_tag.get_attribute('src')
            image_links.append(link)
            self.download_Image(link, str(idx))
    
        #Scrape Details
        product_title = details_container.find_element_by_xpath('.//h1').text
        product_gender = details_container.find_element_by_xpath('.//h5').text
        product_price = details_container.find_element_by_xpath('.//span[@class="Styles__Price-qfm034-4 laqfaf"]').text
        product_sizes_container = details_container.find_element_by_xpath('.//div[@class="Styles__SizesWrapper-sc-8ocgtc-2 kAvucC"]')
        product_sizes = product_sizes_container.find_elements_by_xpath('./button')
        sizes_list = []
        for size in product_sizes:
            sizes_list.append(size.get_attribute('aria-label'))
        id, uu_ID = self.generate_ID(link_HTML)

        #Create dictionary from the data collected
        product_Dict = {
            "UUID": uu_ID,
            "ID": id,
            "Title": product_title,
            "Catalogue": product_gender,
            "Price": product_price,
            "Sizes": sizes_list,
            "Images": image_links
        }

        with open(self.root_Path+'/data.json', 'w') as fp:
            json.dump(product_Dict, fp)
            
        print(product_Dict)

    def load_Product_Links(self, link_list):
        window_before = self.driver.window_handles[0]
        self.driver.execute_script("window.open()")
        for link in link_list:
            window_after = self.driver.window_handles[1]
            self.driver.switch_to.window(window_after)
            self.driver.get(link)
            self.scrape_Data(link)
            break #Take this out When we want to scrape all the links not just 1 per product type ##Testing purposes!
        self.driver.close()
        self.driver.switch_to.window(window_before)

    def start_crawl(self):
        self.create_folder("")
        self.accept_Cookies()
        product_Type_Button, checkbox_list = self.get_product_types()
        for checkbox in checkbox_list:
            product_Type = checkbox.get_attribute('id')
            if product_Type != 'Accessories': #In case of womens catalogue, they added accessories as a clothing type for some reason, so we ignore this
                checkbox.click()
                product_Type_Button.click()
                self.load_More_Products()
                link_list = self.get_Product_Links()
                self.load_Product_Links(link_list)
                product_Type_Button.click()
                checkbox.click()
                break #Take this out When we want to scrape all the links not just 1 per product type ##Testing purposes!

if __name__ == '__main__':
    mens_URL = "https://uk.gymshark.com/collections/all-products/mens"
    womens_URL = "https://uk.gymshark.com/collections/all-products/womens"
    mens_Catalogue = Web_Scraper(mens_URL)
    mens_Catalogue.start_crawl()
    #womens_Catalogue = Web_Scraper(womens_URL)
    #womens_Catalogue.start_crawl()