from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#//*[@id="onetrust-accept-btn-handler"]

class Web_Scraper:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://uk.gymshark.com/collections/all-products/mens")
        
    def accept_Cookies(self):
        time.sleep(3)
        try:
            accept_cookies_button = self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
            accept_cookies_button.click()
        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    def navigate_WebPage(self):
        element = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/main/div[2]/div[1]/section/button")
        element.click()

    def get_Links(self):
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
    test = Web_Scraper()
    test.accept_Cookies()
    #test.navigate_WebPage()
    test.get_Links()
