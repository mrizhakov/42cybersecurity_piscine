from pathlib import Path
from urllib.parse import urljoin, urlparse
import sys
import requests
import argparse
from bs4 import BeautifulSoup, ResultSet
import os

downloaded_images = set()
all_already_scraped_links = set()
current_level = 0

def correct_dup_filename(filename: str) -> str:
    original = Path(args.path) / Path(filename).name
    candidate = original
    unique_id = 0
    while candidate.is_file():
        candidate = original.with_name(
            f"{original.stem}_{unique_id}{original.suffix}"
        )
        unique_id += 1
    return str(candidate)


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
            print(f"Failed to download images from {self.url}")
            return

        for img in img_link:
            img_download_link = urljoin(self.url, img['src'])
            print(f"Self.url is :  {self.url}")
            print(f"Downloaded_images set is {downloaded_images}")


            if img_download_link not in downloaded_images:
                try:
                    # img_download = requests.get(img_download_link)
                    img_download = requests.get(img_download_link, timeout=(5, 10))
                    img_download.raise_for_status()
                except requests.exceptions.RequestException as error:
                    print({error})


                try:
                    filename = Path(urljoin(args.path, img['src'])).name
                    dirfilename = "./" + str(Path(urljoin(args.path, filename)))

                    os.makedirs(args.path, exist_ok=True)
                    print(f"Downloaded_images set is {downloaded_images}")
                    print(f"dirfilename  is {dirfilename}")

                    sys.exit(1)


                    dirfilename = correct_dup_filename(dirfilename, downloaded_images)

                    with open(dirfilename, "wb") as file:
                        file.write(img_download.content)
                        print(f"Downloading image from: {img_download_link}, saving to {filename}")
                        downloaded_images.add(img_download_link)
                except OSError as error:
                    print(f"Failed to save image at {dirfilename}, {error}")
            else:
                print(f"Skipping downloading image {img_download_link} since it was already downloaded")
    
    def getLinks(self) -> None:

        if self.soup:
            next_links = self.soup.find_all("a")
        else:
            print(f"Failed to scrape links from {self.url}")
            return
    

        for link_iter in next_links:
            full_link= urljoin(self.url, link_iter.get("href"))
            print(f"Found the following links on the page: {full_link}")
            
            domain = urlparse(full_link).netloc
            if self.domain == domain and current_level <= args.level:
                print(f"Links {full_link} is unique, will proceed to scrape")

                all_unique_links[current_level + 1].add(full_link)
            else:
                if self.domain == domain:
                    print(f"Skipping link {full_link} since it is an external domain {domain}")
                if current_level > args.level:
                    print(f"Skipping link {full_link} since it is recursion level {current_level} exceeds specified {args.level}")

     


args = parsing_arguments()
args.path = args.path if args.path.endswith("/") else args.path + "/"
arg_check(args)
all_unique_links = [set() for _ in range(args.level+2)]

print(f"Scraping website {args.start_url} for images")
print(f"Downloading files to {args.path}")
print(f"Downloads should be recursive {args.recursive}")
print(f"Level of recursion {args.level}")

print(f"----------------current level is {current_level}------------ ")
print(f"----------------args.level is {args.level}------------ ")
link1 = Link(args.start_url)
link1.getPage()
link1.getLinks()
link1.downloadImages()
pending_links = [set() for _ in range(args.level+2)]
pending_links[current_level] = all_unique_links[current_level] - all_already_scraped_links

while current_level <= args.level:

    print(f"----------------current level is {current_level}------------ ")
    print(f"----------------args.level is {args.level}------------ ")
    pending_links[current_level] = all_unique_links[current_level] - all_already_scraped_links


    while pending_links[current_level]:
        
        first = next(iter(pending_links[current_level]))
        print(f"Checking link {first}")
        
        temp_link_obj = Link(first)
        temp_link_obj.getPage()
        temp_link_obj.getLinks()
        temp_link_obj.downloadImages()
        all_already_scraped_links.add(first)
        print(f"----------------current level is {current_level}------------ ")
        print(f"----------------args.level is {args.level}------------ ")
        
        pending_links[current_level] = all_unique_links[current_level] - all_already_scraped_links

    current_level = current_level + 1

print(f"`----------------------level is {current_level}")
print(f"----------------args.level is {args.level}------------ ")