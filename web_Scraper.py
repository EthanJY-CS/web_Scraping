from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import uuid
from pathlib import Path
import json
import requests
from typing import Any, Tuple, List
import cloud_data

class Web_Scraper:
    '''
    A Web Scraper that is as generic as possible when regarding to control flow and processes 
    but tailored for the gymshark website, collecting the Mens catalogue and the Womens.
    
    Parameters:
    ----------
    url: str
        str of the HTML link of the website to provide
    catalogue: str
        str of the catalogue, either 'Mens' or 'Womens'
    
    Attributes:
    ----------
    options: WebDriverOptions
        WebDriverOptions to be used when wanting to run in headless mode
    driver: WebDriver
        Webdriver to be used to drive the website UI, from Selenium
    root_Path: str
        str of the root_path to the environments directory
    current_Directory: str
        str of the path of current directory that will be concatenated with root_Path
    catalogue: str
        str of the catalogue, used for directory creation, passed from parameter
     
    Methods:
    -------
    create_Directory()
        Creates a Directory
    download_Image(image_url, image_name)
        Downloads the image of the content at the url link provided
    accept_Cookies()
        Accepts the cookies button upon load of webpage
    load_More_Products()
        Navigates to bottom of page and clicks load more button until all products show
    get_Product_Types()
        Gets the product types from the filter bar and their checkboxes to navigate
    get_Product_Links()
        Gets a List of all the HTML links from the products
    generate_ID(link)
        Creates the ID and UUID of a product
    scrape_Data(link_HTML)
        Collects all data from a products webpage
    load_Product_Links(link_list)
        Loads each products webpage in new tab ready to scrape
    start_Crawl()
        Main control of flow function to call all other functions from in order
    '''

    def __init__(self, url, catalogue):
        self.options = Options()
        self.options.headless = True #Change to True when scraping Data
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(url)
        self.root_Path = "/home/ethanjy/Scratch/web_Scraping"
        self.current_Directory = ""
        self.catalogue = catalogue
        
    def create_Directory(self) -> None:
        '''
        Creates a Directory.
        The Directory is created at the concatenation of the root_Path and current_Directory
        '''
        Path(self.root_Path + self.current_Directory).mkdir(parents=True, exist_ok=True)
    
    def download_Image(self, image_url: str, image_name: str) -> None:
        '''
        Downloads the image of the content at the url link provided.
        The Images are downloaded in an images directory, named 'n.jpg'
        where n is an integer starting at 0 to n images

        Parameters:
        ----------
        image_url: str
            The url link of the img source scraped
        image_name: str
            The integer idx of the image passed as string
        '''
        img_data = requests.get(image_url).content
        self.current_Directory += "/images"
        self.create_Directory() #Creates Directory for images inside the
        with open(self.root_Path + self.current_Directory + "/" + image_name + '.jpg', 'wb') as handler:
            handler.write(img_data)
        self.current_Directory = self.current_Directory.replace("/images", "")

    def accept_Cookies(self) -> None:
        '''
        Accepts the cookies button upon load of webpage.
        The driver waits for the container of the accept cookies handler,
        once it loads, presses the accept cookies button.
        '''
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            accept_cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            accept_cookies_button.click()
        except TimeoutException:
            print("Loading took too much time!")

    def load_More_Products(self) -> None:
        '''
        Navigates to bottom of page and clicks load more button until all products show
        While there are more products to load, navigate to bottom of page and click
        load more button, all products from a product type will load on the same page.
        '''
        while True:
            try:
                load_More_Button = self.driver.find_element_by_xpath('//*[@class="Styles__Button-sc-1kpnvfh-4 cRnfyG Styles__PaginationButton-sc-1kf2zc1-1 hBnwhL"]')
                self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight) - 1200);")
                load_More_Button.click()
            except:
                break 
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_Product_Types(self) -> Tuple[Any, List[Any]]:
        '''
        Gets the product types from the filter bar and their checkboxes to navigate.
        Waits for the page to load filter bar, clicks on product_Type filter, and grabs
        all the product_Type checkboxes.

        Returns:
        -------
        product_Type_Button: WebElement
             the product_Type button to click to reveal from the filter bar
        checkbox_list: list[WebElement]
            list of WebElement checkboxes that correspond to each of the product_Types filters
        '''
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

    def get_Product_Links(self) -> List[str]:
        '''
        Gets a List of all the HTML links from the products.
        Finds container that holds all the products, then finds all /article
        from it's children, as these are all the individual products.
        For each product, find the HTML href link tag and append it to the list.

        Returns:
        -------
        link_list: List[str]
             list of all the HTML links to all products loaded on a page
        '''
        prod_container = self.driver.find_element_by_xpath('//*[@class="Styles__Grid-sc-1hr3n2q-0 ekxOoE"]')
        prod_list = prod_container.find_elements_by_xpath('./article')
        link_list = []
        for product in prod_list:
            a_tag = product.find_element_by_tag_name('a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        return link_list

    def generate_ID(self, link: str) -> Tuple[str, str]:
        '''
        Creates the ID and UUID of a product.
        The id is stripped from the HTML link, as it contains a unique user friendly ID.
        The UUID is generated using UUID4 from the UUID library and stored as a string.

        Parameters:
        ----------
        link: str
            The HTML url link of the product

        Returns:
        -------
        id: str
            The id of the product
        uu_ID: str
            The generated UUID of the product
        '''
        idx = link.find('gymshark-', 0, len(link))
        id = link[idx:len(link)]
        uu_ID = str(uuid.uuid4())
        return id, uu_ID
    
    def scrape_Data(self, link_HTML: str) -> None:
        '''
        Collects all data from a products webpage.
        Waits for the left container to load on the webpage (chosen as its images so makes sense for loading time)
        The data is split through left colunn containing the images and the right column containing the product
        details. Scrapes all products details, grabs ID's from generate_ID() func, creates appropriate directories,
        scrapes images and downloads them by the download_Image() func into an images directory, creates data dictionary 
        of all scraped data, then creates a json file of the data dictionary.
        
        Parameters:
        ----------
        link_HTML: str
            The HTML url link of the product
        '''
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="Styles__LeftColumn-lpqwbz-2 danMny"]')))
            images_container = self.driver.find_element_by_xpath('//*[@class="Styles__LeftColumn-lpqwbz-2 danMny"]')
            details_container = self.driver.find_element_by_xpath('//*[@class="Styles__RightColumn-lpqwbz-3 beeZhk"]')
            
            #Scrape Details
            product_title = details_container.find_element_by_xpath('.//h1').text.replace("/", "-") #Pair of shorts tampered with pathway string as it was named 1/2 tight shorts.
            product_gender = details_container.find_element_by_xpath('.//h5').text
            try: #Noticed on very rare occasions, a product didn't have any colours except itself, which we can't grab since no h4 tag exists, so under 'Other' instead
                product_colour = details_container.find_element_by_xpath('.//h4').text.replace("COLOR: ", "")
            except:
                product_colour = 'Other'
            product_price = details_container.find_element_by_xpath('.//span[@class="Styles__Price-qfm034-4 laqfaf"]').text
            product_sizes_container = details_container.find_element_by_xpath('.//div[contains(@class, "Styles__SizesWrapper")]')
            product_sizes = product_sizes_container.find_elements_by_xpath('./button')
            sizes_list = []
            for size in product_sizes:
                sizes_list.append(size.get_attribute('aria-label'))
            id, uu_ID = self.generate_ID(link_HTML)

            #Create directories and go into them
            self.current_Directory += "/" + product_title
            self.create_Directory() #Creates a directory of that product title! As they come in different colours, this is where they are stored under a single directory
            self.current_Directory += "/" + product_colour
            self.create_Directory() #Creates a directory of the specific product by id which will containt it's data json file and images directory

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

            #Create dictionary from the product data collected
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
            
            #Create json file of the data dictionary
            with open(self.root_Path + self.current_Directory + '/data.json', 'w') as fp:
                json.dump(product_Dict, fp)
            
            #back out of directories
            self.current_Directory = self.current_Directory.replace("/" + product_colour, "")
            self.current_Directory = self.current_Directory.replace("/" + product_title, "")
        except TimeoutException:
            print("Loading took too much time!")

    def load_Product_Links(self, link_list: List[str]) -> None:
        '''
        Loads each products webpage in new tab ready to scrape.
        Opens a new tab, switches the window to new tab, then loads all products url from link_list,
        one by one, which we then call scrape_Data() func to carry out the scraping. After all
        products have been scraped, the tab closes, and window switches back to main window.

        Parameters:
        ----------
        link_list: list[str]
            The list of HTML links of all the products
        '''
        window_before = self.driver.window_handles[0]
        self.driver.execute_script("window.open()")
        for link in link_list:
            window_after = self.driver.window_handles[1]
            self.driver.switch_to.window(window_after)
            self.driver.get(link)
            self.scrape_Data(link)
            #break #Take this out When we want to scrape all the links not just 1 per product type ##TESTING purposes!
        self.driver.close()
        self.driver.switch_to.window(window_before)

    def start_Crawl(self) -> None:
        '''
        Main control of flow function to call all other functions from in order.
        Main function that controls the rest of the scraper class. Creates raw_Data Directory in root_Path,
        then creates the catalogue it's scraping from. Accepts cookies then navigates the webpage by clicking
        each product type checkbox in each loop from the filter bar, and then calling all necessary functions 
        to perform the scraping in order. The driver then quits after performing.

        '''
        self.current_Directory = "/raw_data"
        self.create_Directory() #Creates raw_Data Directory
        self.current_Directory += "/" + self.catalogue
        self.create_Directory() #Creates catalogue Directory
        self.accept_Cookies()
        product_Type_Button, checkbox_list = self.get_Product_Types()
        for checkbox in checkbox_list:
            product_Type = checkbox.get_attribute('id').replace(" & ", " and ")
            if product_Type != 'Accessories': #In case of womens catalogue, they added accessories as a clothing type for some reason, so we ignore this
                self.current_Directory += "/" + product_Type
                self.create_Directory() #Creates product_Type directory
                checkbox.click()
                product_Type_Button.click()
                self.load_More_Products() #Comment this out when we just want max 60 products per type ##TESTING purposes!
                link_list = self.get_Product_Links()
                self.load_Product_Links(link_list)
                product_Type_Button.click()
                checkbox.click()
                self.current_Directory = self.current_Directory.replace("/" + product_Type, "")
        self.driver.quit()
        print("The {} catalogue has been Collected!".format(self.catalogue))

if __name__ == '__main__':
    mens_URL = "https://uk.gymshark.com/collections/all-products/mens"
    womens_URL = "https://uk.gymshark.com/collections/all-products/womens"
    mens_Catalogue = Web_Scraper(mens_URL, "Mens")
    mens_Catalogue.start_Crawl()
    womens_Catalogue = Web_Scraper(womens_URL, "Womens")
    womens_Catalogue.start_Crawl()
    #Upload data collection to aws s3
    cloud_data.upload_to_s3("raw_data", "gymshark-data", "raw_data")