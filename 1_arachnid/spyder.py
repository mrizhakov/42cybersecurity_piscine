from pathlib import Path
from urllib.parse import urljoin

import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="A simple web scraper to download images from a webpage.")
#parser.add_argument("--url", type=str, default="https://crawler-test.com/links/image)
parser.add_argument('-p', 
                    '--path', 
                    type=str, 
                    default="./data/", 
                    help="The starting URL to scrape for images.") 
parser.add_argument('-r', 
                    '--recursive', 
                    action='store_true', 
                    help="Recursively scrape links found on the page, default value is 5.")
parser.add_argument('-l', 
                    '--level', 
                    default = 5, 
                    help="Level of recursion, default value is 5.")
parser.add_argument("start_url", help="Webpage to scrape")

args = parser.parse_args()
print(f"Scraping website {args.start_url} for images")
print(f"Downloading files to {args.path}")
print(f"Downloads should be recursive {args.recursive}")
print(f"Level of recursion {args.level}")



save_path = "data/"
visited_links = set()
downloaded_images = set()

start_url = "https://crawler-test.com/links/image_links"
#url = "https://en.wikipedia.org/wiki/Spinning_top"

response = requests.get(start_url)
response.raise_for_status()
print(f"Scraping page: {start_url}")
visited_links.add(start_url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

img_link = soup.find_all("img")
for img in img_link:
    img_download_link = urljoin(start_url, img['src'])
    img_download = requests.get(img_download_link)
    img_download.raise_for_status()
    print(f"Downloading image from: {img_download_link}")
    downloaded_images.add(img_download_link)
    filename = Path(img_download_link).name
    with open(save_path + filename, "wb") as file:
        file.write(img_download.content)

next_links = soup.find_all("a href")

