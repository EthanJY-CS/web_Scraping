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

if __name__ == '__main__':
    test = Web_Scraper()
    test.accept_Cookies()
    #test.navigate_WebPage()
