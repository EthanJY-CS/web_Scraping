import unittest
from web_Scraper import Web_Scraper
import shutil
from selenium.common.exceptions import TimeoutException
import pathlib
import json

class TestWebScraper(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.mens_Catalogue = Web_Scraper("https://uk.gymshark.com/collections/all-products/mens", "Mens")

    @classmethod
    def tearDownClass(cls):
        #Removes the folder of raw_data created after testing
        shutil.rmtree("/home/ethanjy/Scratch/web_Scraping/raw_data", ignore_errors=True)

    def test_generate_ID(self):
        id, uuid = self.mens_Catalogue.generate_ID("https://uk.gymshark.com/products/gymshark-power-t-shirt-black-aw21")
        self.assertIsInstance(id, str)
        self.assertEqual(id, "gymshark-power-t-shirt-black-aw21")
        self.assertIsInstance(uuid, str)

    def test_create_Directory(self):
        self.mens_Catalogue.current_Directory = "/raw_data"
        self.mens_Catalogue.create_Directory()
        file = pathlib.Path("/home/ethanjy/Scratch/web_Scraping/raw_data")
        if not file.exists ():
            self.fail("The directory raw_data does not Exist!")

    def test_download_Image(self):
        self.mens_Catalogue.current_Directory = "/raw_data"
        self.mens_Catalogue.download_Image("https://cdn.shopify.com/s/files/1/0098/8822/products/PowerSsT-Shirt_Og_BlackA2A1W.ATIFF_IS_290x.jpg?v=1645128107", "0")
        file = pathlib.Path("/home/ethanjy/Scratch/web_Scraping/raw_data/images")
        if not file.exists ():
            self.fail("The directory images does not Exist!")
        else:
            file = pathlib.Path("/home/ethanjy/Scratch/web_Scraping/raw_data/images/0.jpg")
            if not file.exists():
                self.fail("The image 0.png does not exist therefore was not downloaded!")

    def test_create_JSON_file(self):
        self.mens_Catalogue.current_Directory = "/raw_data"
        self.mens_Catalogue.create_Directory()
        test_Dict = {
                "Name": "Ethan",
                "Age": 22
        }
        self.mens_Catalogue.create_JSON_File(test_Dict)
        file = pathlib.Path("/home/ethanjy/Scratch/web_Scraping/raw_data/data.json")
        if not file.exists ():
            self.fail("The file data.json does not Exist!")
        else:
            #Check contents of json
            f = open(file)
            data = json.load(f)
            self.assertIsInstance(data, dict)
            self.assertEqual(data['Age'], 22)
            self.assertIsInstance(data['Age'], int)
            self.assertEqual(data['Name'], "Ethan")
            self.assertIsInstance(data['Name'], str)
            f.close()
            #Remove json file in testing conditions
            shutil.rmtree("/home/ethanjy/Scratch/web_Scraping/raw_data/data.json", ignore_errors=True)

if __name__ == '__main__':
    unittest.main()