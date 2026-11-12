from pathlib import Path
from urllib.parse import urljoin, urlparse
import sys
import requests
import argparse
from bs4 import BeautifulSoup, ResultSet
import os

downloaded_images = set()
all_unique_links = set()
all_already_scraped_links = set()



def parsing_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A simple web scraper to download images from a webpage.")
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
                        type=int,
                        default = 5, 
                        help="Level of recursion, default value is 5.")

    parser.add_argument("start_url", help="Webpage to scrape")



    return parser.parse_args()



def arg_check(args: argparse.Namespace) -> None:
    save_path = args.path

    if args.level < 1:
        print(f"Level of recursion cant be zero or negative")
        sys.exit(1)

    path = Path(save_path)

    if path.is_absolute() or path.is_file():
        print(f"Provide a valid path to download images")
        sys.exit(1)



class Link:

    def __init__(self, start_url: str) ->None:
        self.url: str = start_url
        self.domain: str = urlparse(self.url).netloc
        self.soup: BeautifulSoup | None = None
        self.links: ResultSet | None = None
        self.level: int = 0


    def getPage(self) -> None:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            print(f"Scraping page from class: {self.url}")
        except requests.exceptions.RequestException as error:
            print(f"{error}")
            return
        
        self.soup = BeautifulSoup(response.text, "html.parser")

    def downloadImages(self) -> None:

        if self.soup:
            img_link = self.soup.find_all("img")
        else:
            print(f"Class Link: Failed to download images from {self.url}")
            return


        for img in img_link:
            img_download_link = urljoin(self.url, img['src'])
            print(f"Self.url is :  {self.url}")

            if img_download_link not in downloaded_images:
                try:
                    img_download = requests.get(img_download_link)
                    img_download.raise_for_status()
                    # filename = args.path + img['src']
                    filename = Path(urljoin(args.path, img['src'])).name
                    dirfilename = "./" + str(Path(urljoin(args.path, filename)))

                    print(f"args.path is :  {args.path}")
                    print(f"img['src'] is :  {img['src']}")
                    print(f"filename is :  {filename}")
                    print(f"dirfilename is :  {dirfilename}")
                    os.makedirs(args.path, exist_ok=True)


                    with open(dirfilename, "wb") as file:
                        file.write(img_download.content)
                        print(f"Class Link: Downloading image from: {img_download_link} to {filename}")
                        downloaded_images.add(img_download_link)
                except requests.exceptions.RequestException as error:
                    print(f"{error}")
                    print(f"Class Link: Failed to download image from {img_download_link}")
            else:
                print(f"Class Link: Skipping downloading image {img_download_link} since it was already downloaded")
    
    def getLinks(self) -> None:

        if self.soup:
            next_links = self.soup.find_all("a")
        else:
            print(f"Class Link: Failed to scrape links from {self.url}")
            return
    

        for link_iter in next_links:
            full_link= urljoin(self.url, link_iter.get("href"))
            print(f"Found the following links on the page: {full_link}")
            

            domain = urlparse(full_link).netloc
            if self.domain == domain:
                all_unique_links.add(full_link)
            else:
                print(f"Skipping link {full_link} since it is an external domain {domain}")

args = parsing_arguments()
args.path = args.path if args.path.endswith("/") else args.path + "/"
arg_check(args)



link1 = Link(args.start_url)
link1.getPage()
link1.getLinks()
link1.downloadImages()
pending_links = all_unique_links - all_already_scraped_links
print(f"##############This is pending links before loop: {pending_links}")

while pending_links:
    if link1.level >= args.level:
        break
    first = next(iter(pending_links))
    print(f"Checking link {first}")
    
    temp_link_obj = Link(first)
    temp_link_obj.getPage()
    temp_link_obj.getLinks()
    temp_link_obj.downloadImages()
    all_already_scraped_links.add(first)
    pending_links = all_unique_links - all_already_scraped_links
    link1.level = link1.level + 1
    print(f"`----------------------level is {link1.level}")
    print(f"##############This is pending links after loop: {pending_links}")
    print(f"##############This is pending links after loop: {pending_links}")


# first = next(iter(pending_links))
# print(f"Checking link {first}")
    
# temp_link_obj = Link(first)
# temp_link_obj.getPage()
# temp_link_obj.getLinks()
# temp_link_obj.downloadImages()
# all_already_scraped_links.add(first)
# pending_links = all_unique_links - all_already_scraped_links


print(f"Scraping website {args.start_url} for images")
print(f"Downloading files to {args.path}")
print(f"Downloads should be recursive {args.recursive}")
print(f"Level of recursion {args.level}")

start_url = args.start_url
