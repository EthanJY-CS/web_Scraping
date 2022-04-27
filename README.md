# Data Collection Pipeline

> Web scraping a website to collect data.

> UML Diagram of Data Collection Pipeline
> ![image](https://user-images.githubusercontent.com/78024243/164996194-5a6ca374-3a27-40c6-80db-e7b8f0b798a2.png)


## Milestone 1: Decide the website you are going to collect data from

![image](https://user-images.githubusercontent.com/78024243/164996592-4e80adbd-d6d5-4d55-b779-db2ca3f54a86.png)


I decided to collect data from Gymshark, who are the worlds biggest gym clothing brand, why? well I chose them because I am passionate with the gym and bodybuilding,
and have bought and lived in some of their clothing for a while with the only thing stopping me from buying more is my bank balance. I also had a think as to where I'd
maybe like to work at, and you know what, if they ever wanted a keen Data scientist/ML engineer to work on their data pipelines, I will be available.

Goal is to collect data from both their mens and womens catalogue, and in which case relevent data to clothing will be;
- Product ID
- Price
- Sizes Available
- Colours Available (although redundent to a degree as all individual colours of a specific clothing are under 'all products' anyway)
- Any images of the clothing showcased

## Milestone 2: Prototype finding the individual page for each entry

First, we create a web_Scraper class that will essentially run all the functions that we need to perform to load, navigate, and scrape the website that we have chosen.
The tools we will be using to perform these tasks is called selenium, where we use the webDriver package from the library to first load a browser in this case, Firefox,
and then go to the URL that we send to the class, which of course is the url of either the men's all products page or women's, as I'll have 2 instances of the web scraper
class eventually.

Next is to populate the class with methods that we need to perform in sequential order, because the first thing that happens when the page is loaded, is like most websites,
they ask to accept cookies, and we can't navigate or perform web scraping until we accept. So the first method is to accept_Cookies(). We will do this by using the webdriver
wait module, where it waits for the page to load fully before we use an Xpath expression to find the element on the page that contains the accept cookies pop up message, and
then clicks the button to accept.

Navigating the website is where it starts to become exciting, watching the webdriver move around the website and such like if it were a user, so to start, as we are on the
all products page, I notice that the mens catalogue shows 60 products per page, with a 'load more' button, and this load more really just opens up another 60, so already
I'm thinking of a function navigate_webpage() which essentially is a loop control flow of clicking the load more button until there is no more products to load, so we find the
element of the load button using xPath, and then click it. I realise in testing that doing this started to take a really long time to load, because if you think about showing
~1300 clothing products on one page, it'll start struggling with how much data to load starting at around 400-500 products so we must find a fix! I notice that we can narrow
down the amount of products per page by using the filters, mainly the one that splits the clothing into types for example T-shirts & tops, bottoms, hoodies & jackets, etc, which
lowers the maximum amount of products to ever load all at once to no more than 400 which speeds up the process. So in another function start_scrape() where I handle the sequential
order of calling these different methods inside the class, there is another function that I create to return the get_product_types() and navigate the filter bar to click on the filter
buttons in order of each type, so we can then deal with the products loading faster per load phase.

Once each loading phase happens per type, I have another function that returns the get_products_links() which using an xPath expression, we find the container that holds all the products,
and then go into each product to return the HTML link under a_tag href for that product. So we end up creating a list link_list[] that holds each HTML for each product on that page from now we can
use to individually load those pages and start to think about scraping the data from the individual pages.

## Milestone 3: Retrieve data from details page

I split the next section into another function that deals with the loading of the product web pages, and then another function called scrape_data, that is called for every product link loaded. Essentially, we open a new tab, and loop through the link_list[] gathered in milestone 2, which loads each product one by one, ready for us to think about scraping the data.

Inside the loop of each link, we call a scrape_data function, which will hold all the necessary actions to scrape the data we want per product, using more of the selenium web driver/element functions. The layout of a products page is split into 2 sections, left and right column. This turns out to be really useful as we can see in the HTML, that the images we would like to grab the links from (to download soon) are located in the left column, while all the details of the product title, cost, sizes, etc are located in the right column. We scrape all the necessary data using xpath, the images by looking for img tag in the left column and then get the src attribute, while all the text details (all but the sizes) were in header tags, and for the sizes, we looked for all the /buttons within a class that contains "Styles__SizesWrapper" because for different products, they have a different range of sizes they come in so the id of the container for those buttons could change (found when testing).

Before we create a data dictionary for our scraped data, what we need is a user friendly id and a uuid, in which I separate in another function that returns both of those, id comes from the last section of it's html link, and the uuid is generated by using uuid4 from the uuid library.

A data dictionary is then created and is locally stored as a json file in a raw_data direcotry that is created upon start, this raw_data directory will act as our root for storing our scraped data. The next step is to download the images from the scraped image links, just in case the original html link changes for that product. This is split into a function download_image that I searched online to use using the requests library, we request the image from its src link scraped, then download as a jpeg, named using numbers starting from 0.jpg to n.jpg depending on how many images per product. These images are stored in a directory called images, which is inside the raw_data directory.

After this, I realised that my data to scrape naturally fell into categories so I wanted to completely overhaul how they were stored in sub-directories,
so here's how I wanted to design my raw_data directory.

```python
    """
    >raw_data
      >Mens                       #Catalogue e.g. Mens, Womens, possibly Accesories in the future
        >Product_type             #e.g. T-shirts and tops, Shorts, Joggers, etc.
          >Product_title          #e.g. Legacy T-shirt. A line of clothing that can come in different colours
            >Product_colour       #e.g. Black, White, etc
              >data.json          #Contains the data dictoinary of the product, with all data that is scraped
              >images             #contains the images downloaded of that product
                >0.jpg
                >..jpg
                >n.jpg
    """
```

