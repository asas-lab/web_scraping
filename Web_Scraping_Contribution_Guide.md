# Web_Scraping


This guide helps you contribute to our efforts in crawling various websites using Scrapy and Selenium.

Prerequisites

    Basic knowledge of Python, Scrapy, and Selenium.
    Python version >= 3.8 installed on your machine.


1. Cloning the Repository

Start by cloning the repository to your local machine:

```
git clone https://github.com/asas-lab/web_scraping.git

```


2. Installing Dependencies

 Enter to the project directory and install the required dependencies:


```
cd web_scraping
pip install -r requirements.txt

```
3. Claiming Issues

Visit our issues page: https://github.com/asas-lab/web_scraping/issues to claim an issue. Each issue
corresponds to a website that needs to be crawled.

4. Running Scripts

For Scrapy:

Navigate to the corresponding website directory and run:

```
cd news_website_name
scrapy crawl news_website_name

```

For Selenium:

Navigate to the corresponding website directory and run:

```
cd news_website_name
python main.py

```

5. Locate the Generated Json File:

`news_website_name.py` file is found in the news website directory folder. The file contains the crawled content in json line format.

5. Upload the dataset:

Run the upload script `upload.py` which designed to upload the files into HuggingFace. You can run the code using the following  command:

```
cd news_website_name
python upload.py --token tyour_token_in_hf --dataset_path path_to_json_file --hf_repository_name dataset_name_or_path_in_hf

```
