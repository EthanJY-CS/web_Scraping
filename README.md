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
- Colours Available
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

Here is an example of the filter by type, which we will use to our advantage:
> ![image](https://user-images.githubusercontent.com/78024243/169665525-f040d3f6-d8bf-4246-85ff-bd96c87a1166.png)

Once each loading phase happens per type, I have another function that returns the get_products_links() which using an xPath expression, we find the container that holds all the products,
and then go into each product to return the HTML link under a_tag href for that product. So we end up creating a list link_list[] that holds each HTML for each product on that page from now we can
use to individually load those pages and start to think about scraping the data from the individual pages.

## Milestone 3: Retrieve data from details page

I split the next section into another function that deals with the loading of the product web pages, and then another function called scrape_data, that is called for every product link loaded. Essentially, we open a new tab, and loop through the link_list[] gathered in milestone 2, which loads each product one by one, ready for us to think about scraping the data.

Inside the loop of each link, we call a scrape_data function, which will hold all the necessary actions to scrape the data we want per product, using more of the selenium web driver/element functions. The layout of a products page is split into 2 sections, left and right column. This turns out to be really useful as we can see in the HTML, that the images we would like to grab the links from (to download soon) are located in the left column, while all the details of the product title, cost, sizes, etc are located in the right column. We scrape all the necessary data using xpath, the images by looking for img tag in the left column and then get the src attribute, while all the text details (all but the sizes) were in header tags, and for the sizes, we looked for all the /buttons within a class that contains "Styles__SizesWrapper" because for different products, they have a different range of sizes they come in so the id of the container for those buttons could change (found when testing).

Before we create a data dictionary for our scraped data, what we need is a user friendly id and a uuid, in which I separate in another function that returns both of those, id comes from the last section of it's html link, and the uuid is generated by using uuid4 from the uuid library.

A data dictionary is then created and is locally stored as a json file in a raw_data directory that is created upon start, this raw_data directory will act as our root for storing our scraped data. The next step is to download the images from the scraped image links, just in case the original html link changes for that product. This is split into a function download_image that I searched online to use using the requests library, we request the image from its src link scraped, then download as a jpeg, named using numbers starting from 0.jpg to n.jpg depending on how many images per product. These images are stored in a directory called images, which is inside the raw_data directory.

After this, I realised that my data to scrape naturally fell into categories so I wanted to completely overhaul how they were stored in sub-directories,
so here's how I wanted to design my raw_data directory.

```python
    """
    >raw_data
      >Mens                       #Catalogue e.g. Mens, Womens, possibly Accesories in the future
        >Product_type             #e.g. T-shirts and tops, Shorts, Joggers, etc.
          >Product_title          #e.g. Legacy T-shirt. A line of clothing that can come in different colours
            >Product_colour       #e.g. Black, White, etc
              >data.json          #Contains the data dictionary of the product, with all data that is scraped
              >images             #contains the images downloaded of that product
                >0.jpg
                >..jpg
                >n.jpg
    """
```

Here is an example page for a product:
> ![image](https://user-images.githubusercontent.com/78024243/169665397-83fae8fc-75ce-402c-a8c9-ffbe3221f463.png)

## Milestone 4: Documentation and Testing

First to scrutinise the code and refactor, which you naturally do over the course of the project anyway, when you realise you could do something different that will optimise workflow etc. Then Docstrings were added to the file to explain and readably convey my project where I chose the NumPy/SciPy style format. In addition to this and I didn't have to but I had a go at Typing, using Pythons built in typing library, which essentially just adds more understanding to the code as to the data types of variables, arguments and function returns. 

Building onto this, we then used pythons unittest library to apply unit testing to public methods from our web_Scraper class. I didn't have many public methods that we standalone, without then moving into component testing which is slightly different (unit testing uses dummy data, component testing uses real data), so the test suite was quite small, testing;
- the ability to create a directory at a given path
- to generate the ID of a product (strip the ID from a string of it's HTML link)
- downloading an image using the image src of a link (in this case, a product)
- the ability to create a json file of a dictionary, then read it back in to test the contents

Here are the 4 tests passing when running the test suite
> ![image](https://user-images.githubusercontent.com/78024243/169661880-35bfdc18-e3d6-4255-b06f-5cc4d912ff89.png)

## Milestone 5: Scalably store the Data

This is where we learn to operate AWS services to scalably store the data that we scrape from the website, using the services;
- S3 to store the raw_data folder, which contains both the json files and any image data
    - This is where I learnt that an S3 Bucket operates using objects, and there's no such thing as directories, but it can simulate them online if you use       the same paths as you were to create them locally when uploading to S3
- RDS to store the contents of the json files as tabular data
- IAM to create an admin User that we will use the credentials for when connecting to these services
- EC2 instance to run and operate workflow on the cloud instead of locally (Milestone 7)

I actually split the cloud_data methods in a seperate class as it made sense to not add it to a web_scraper class. To make this possible, I used the boto3 library to create a client that connects to S3 services, to upload the contents of raw_data, this is done individually for every product scraped, uploading with the 'path' as it would be locally and therefore as an object to S3 that can simulate that path.
Then using sqlalchemy and pandas, for reading/uploading to AWS RDS, where we connect to the database via creating an engine from sqlAlchemy. With 3 main methods that we need;
- To upload/append a data_dict of a product to the table 'gymshark-database' to RDS
- To read the table (printing the .head() and then the shape of the table to confirm for testing to check if they are being uploaded correctly)
- To check if a record exists by ID. A does_record_exist() that checks the database to see if we have already scraped a product using it's ID (Milestone 7)

Example of the contents uploaded to S3:
> ![image](https://user-images.githubusercontent.com/78024243/169663572-b26fd63f-cd44-4775-b704-40c2c189bf26.png)

Example of running the read_database():
> ![image](https://user-images.githubusercontent.com/78024243/169663662-1fa4fbe7-a656-4cd6-aed5-a133d2d24876.png)

## Milestone 6: Getting more Data

Funny enough I skipped this milestone as it didn't concern me having already done it, essentially can the scraper run without issues and scraping more data, but I had already wanted to scrape all the products anyway so I was testing if the project could do this since at milestone 3. The other option was to stop the rescraping of images/data locally, but I knew we were about to do it when referencing to AWS RDS which will in turn do it locally.

## Milestone 7: Make the scraping Scalable

The check to see if we have scraped an image with reference to checking a products ID using an SQL statement call from the cloud_data file and RDS was created. This allowed the running of the project that won't rescrape and therefore won't create existing local and AWS data points of the products. 
With this, the next step was to create an EC2 instance that would run the program so everything operated on the cloud instead of a local machine. To do this we first had to use Docker, to create an Image of the environment and libraries needed to run the program, so that we could then containerise the project and upload and run from an EC2 instance. 

First we needed to make a DockerFile that ran through commands that would build the environment on an already prexisting image like python or an operating system, with then the necessary steps of setting up the rest of the environment by downloading the libraries and dependencies that the project needs. For example, firefox and the geckodriver had to first then be downloaded. Then we would pip install all the dependencies from a requirements.txt file that contains the libraries and their version that needs to be installed to run the scraper. Once built, we upload the image to Dockerhub, and then download the image onto the EC2 instance by pulling from dockerhub. We could then run the project on the EC2 instance without having to download and setup everything on there as it's all contained in a docker image. 

I noticed that while running the scraper, a t2.micro (free tier) instance was simply not enough to perform the scraper project, so I upgraded to a t2.medium for more cpu and memory, as both was needed (cpu was running at near 100% with more memory needed also for loading lots of products on a single browser tab would use a lot of RAM)

Here is me connected to my EC2 t2.medium instance and showing the web_scraper docker image is on there
>![image](https://user-images.githubusercontent.com/78024243/169664660-61f6c6e7-de89-462f-8283-8f8eb817629b.png)

## Milestone 8: Monitoring and Alerting

Once we are able to run the scraper on the EC2 instance, we would like a way to monitor and alert us with metrics that are viewable. This is where we take advantage of using Prometheus, originally designed for soundcloud and is now an open source widely used service that helps monitor and alert us using what is known as 'jobs' so we create a job that prometheus will then scrape metrics at intervals. We use 3 jobs for monitoring and alerting;
- Prometheus (itself)
- docker (metrics of docker containers, for example, containers that are running)
- node (using node_exporter, these are hardware metrics, so in our case, hardware metrics from the EC2 instance)

We can observe these metrics by connecting to a port from our EC2 instance Ip that we exposed to access these metrics and graphs, however we would like a nicer way of observing these graphs. This is where grafana comes in, which we set up on localhost, connecting to the IP:port of the EC2 instance, and all the prometheus graphs and metrics are then brought to a grafana dashboard, where you can create your own dashboard to show key metrics on essentially a front page, for important monitoring which will be necessary to understand on a larger scale project to operate large services.

Here is the dashboard example of my EC2 instance on Grafana
>![grafanaDashboard](https://user-images.githubusercontent.com/78024243/169665056-970f691d-d99a-40e6-8f62-2fe3bef94a71.png)

## Milestone 9: Setup a CI/CD pipeline for your Docker image

a CI/CD pipeline is setup using github secrets and github actions, where everytime we make code changes and push to the 'main' branch on github for the web_scraping project, a github action will take place, that runs through some commands that essentially builds a new image based on the code changes and uploads a web_scraper:latest to dockerHub. This allows us to auto regulate our EC2 instance online, where using cronjobs, we schedule (I chose once a week) for the EC2 to pull the latest version of the web_scraper from dockerhub, then to run this image. So once a week, the web_scraper will scrape data that it already checks to scrape products that don't exist, therefore speaking, only products that gymshark add to their catalogue will be scraped, hence why I chose once a week as the time frame, as they will probably not add new products every day.

## Final comments

Really had fun on this project, learning and using libraries and services that were new to me gaining a lot of experience with data collection, in which long term, we can then do useful things with the data scraped. 
