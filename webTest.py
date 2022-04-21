from json import load
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

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

    def navigate_WebPage(self):
        while True:
            if not self.driver.find_element_by_xpath('//*[@class="Styles__Button-sc-1kpnvfh-4 cRnfyG Styles__PaginationButton-sc-1kf2zc1-1 hBnwhL"]').is_displayed():
                break
            else:
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight) - 1200);")
                load_More_Button = self.driver.find_element_by_xpath('//*[@class="Styles__Button-sc-1kpnvfh-4 cRnfyG Styles__PaginationButton-sc-1kf2zc1-1 hBnwhL"]')
                load_More_Button.click()

    def get_Product_Catagories(self):
        time.sleep(3)
        catagory_container = self.driver.find_element_by_xpath('//*[@id="collections"]') # XPath corresponding to the Container
        product_Type_Button = catagory_container.find_element_by_xpath('./button')
        product_Type_Button.click()

        checkbox_list = catagory_container.find_elements_by_xpath('//*[@class="Styles__Checkbox-sc-9kless-1 eLKrVj"]')
        print(f'There are {len(checkbox_list)} catagories on this page')
        for checkbox in checkbox_list:
            time.sleep(4)
            checkbox.click()
            time.sleep(2)
            checkbox.click()

    def get_Product_Links(self):
        time.sleep(3)
        prod_container = self.driver.find_element_by_xpath('//*[@class="Styles__Grid-sc-1hr3n2q-0 ekxOoE"]') # XPath corresponding to the Container
        prod_list = prod_container.find_elements_by_xpath('./article')
        link_list = []

        for product in prod_list:
            a_tag = product.find_element_by_tag_name('a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
    
        print(f'There are {len(link_list)} Products on this page')
        print(link_list)

if __name__ == '__main__':
    mens_URL = "https://uk.gymshark.com/collections/all-products/mens"
    womens_URL = "https://uk.gymshark.com/collections/all-products/womens"
    test = Web_Scraper(mens_URL)
    test.accept_Cookies()
    test.get_Product_Catagories()
    #test.navigate_WebPage()
    #test.get_Product_Links()


#Styles__Wrapper-sc-9kless-0 jZLLBP