from math import prod
from tabnanny import check
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import uuid
from pathlib import Path
import json
import requests

class Web_Scraper:

    def __init__(self, url, catalogue):
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        self.root_Path = "/home/ethanjy/Scratch/web_Scraping/raw_data"
        self.current_directory = ""
        self.catalogue = catalogue
        
    def create_folder(self):
        Path(self.root_Path + self.current_directory).mkdir(parents=True, exist_ok=True)
    
    def download_Image(self, image_url, image_name):
        img_data = requests.get(image_url).content
        self.current_directory += "/images"
        self.create_folder() #Creates folder for images inside the
        with open(self.root_Path + self.current_directory + "/" + image_name + '.jpg', 'wb') as handler:
            handler.write(img_data)
        self.current_directory = self.current_directory.replace("/images", "")

    def accept_Cookies(self):
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            accept_cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            accept_cookies_button.click()
        except TimeoutException:
            print("Loading took too much time!")

    def load_More_Products(self):
        while True:
            try:
                load_More_Button = self.driver.find_element_by_xpath('//*[@class="Styles__Button-sc-1kpnvfh-4 cRnfyG Styles__PaginationButton-sc-1kf2zc1-1 hBnwhL"]')
                self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight) - 1200);")
                load_More_Button.click()
            except:
                break 
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_product_types(self):
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collections"]')))
            catagory_container = self.driver.find_element_by_xpath('//*[@id="collections"]')
            product_Type_Button = catagory_container.find_element_by_xpath('./button')
            product_Type_Button.click()
            checkbox_list = catagory_container.find_elements_by_xpath('.//*[@class="Styles__Checkbox-sc-9kless-1 eLKrVj"]')
        except TimeoutException:
            print("Loading took too much time!")

        return product_Type_Button, checkbox_list

    def get_Product_Links(self):
        prod_container = self.driver.find_element_by_xpath('//*[@class="Styles__Grid-sc-1hr3n2q-0 ekxOoE"]')
        prod_list = prod_container.find_elements_by_xpath('./article')
        link_list = []
        for product in prod_list:
            a_tag = product.find_element_by_tag_name('a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
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
            images_container = self.driver.find_element_by_xpath('//*[@class="Styles__LeftColumn-lpqwbz-2 danMny"]')
            details_container = self.driver.find_element_by_xpath('//*[@class="Styles__RightColumn-lpqwbz-3 beeZhk"]')
            
            #Scrape Details
            product_title = details_container.find_element_by_xpath('.//h1').text
            product_gender = details_container.find_element_by_xpath('.//h5').text
            try:
                product_colour = details_container.find_element_by_xpath('.//h4').text.replace("COLOR: ", "")
            except: #Noticed on very rare occasions, a product didn't have any colours except itself, which we can't grab since no h4 tag exists, so under 'Other' instead
                product_colour = 'Other'
            product_price = details_container.find_element_by_xpath('.//span[@class="Styles__Price-qfm034-4 laqfaf"]').text
            product_sizes_container = details_container.find_element_by_xpath('.//div[@class="Styles__SizesWrapper-sc-8ocgtc-2 kAvucC"]')
            product_sizes = product_sizes_container.find_elements_by_xpath('./button')
            sizes_list = []
            for size in product_sizes:
                sizes_list.append(size.get_attribute('aria-label'))
            id, uu_ID = self.generate_ID(link_HTML)

            self.current_directory += "/" + product_title
            self.create_folder() #Creates a directory of that product title! As they come in different colours, this is where they are stored under a single folder
            self.current_directory += "/" + product_colour
            self.create_folder() #Creates a directory of the specific product by id which will containt it's data json file and images directory

            #Scrape Images
            image_list = images_container.find_elements_by_xpath('.//*[@class="Styles__Image-sc-176u4ag-1 etChzz"]')
            image_links = []
            for idx, image in enumerate(image_list):
                try:
                    img_tag = image.find_element_by_tag_name('img')
                    link = img_tag.get_attribute('src')
                    image_links.append(link)
                    self.download_Image(link, str(idx))
                except:
                    pass

            #Create dictionary from the data collected
            product_Dict = {
                "UUID": uu_ID,
                "ID": id,
                "Title": product_title,
                "Catalogue": product_gender,
                "Colour": product_colour,
                "Price": product_price,
                "Sizes": sizes_list,
                "Images": image_links
            }

            with open(self.root_Path + self.current_directory + '/data.json', 'w') as fp:
                json.dump(product_Dict, fp)
            self.current_directory = self.current_directory.replace("/" + product_colour, "")
            self.current_directory = self.current_directory.replace("/" + product_title, "")
        except TimeoutException:
            print("Loading took too much time!")

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
        self.create_folder() #Creates raw_Data Directory
        self.current_directory = "/" + self.catalogue
        self.create_folder() #Creates catalogue Directory
        self.accept_Cookies()
        product_Type_Button, checkbox_list = self.get_product_types()
        for checkbox in checkbox_list:
            product_Type = checkbox.get_attribute('id').replace(" & ", " and ")
            if product_Type != 'Accessories': #In case of womens catalogue, they added accessories as a clothing type for some reason, so we ignore this
                self.current_directory += "/" + product_Type
                self.create_folder() #Creates product_Type directory
                checkbox.click()
                product_Type_Button.click()
                #self.load_More_Products() #Take this out when we just want max 60 products
                link_list = self.get_Product_Links()
                self.load_Product_Links(link_list)
                product_Type_Button.click()
                checkbox.click()
                self.current_directory = self.current_directory.replace("/" + product_Type, "")
                #break #Take this out When we want to scrape all the links not just 1 per product type ##Testing purposes!
        self.driver.quit()

if __name__ == '__main__':
    mens_URL = "https://uk.gymshark.com/collections/all-products/mens"
    womens_URL = "https://uk.gymshark.com/collections/all-products/womens"
    mens_Catalogue = Web_Scraper(mens_URL, "Mens")
    mens_Catalogue.start_crawl()
    #womens_Catalogue = Web_Scraper(womens_URL, "Womens")
    #womens_Catalogue.start_crawl()