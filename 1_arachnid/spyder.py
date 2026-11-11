from pathlib import Path
from urllib.parse import urljoin
import sys
import requests
import argparse
from bs4 import BeautifulSoup, ResultSet

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

# downloaded_images = set()
# all_unique_links = set()
# all_already_scraped_links = set()



class Link:
    # soup
    # BeautifulSoup().__init__(soup)

    def __init__(self, start_url: str) ->None:
        self.url: str = start_url
        self.soup: BeautifulSoup | None = None
        self.links: ResultSet | None = None

        # self.soup 

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

        img_link = self.soup.find_all("img")
        for img in img_link:
            img_download_link = urljoin(self.url, img['src'])

            if img_download_link not in downloaded_images:
                try:
                    img_download = requests.get(img_download_link)
                    img_download.raise_for_status()
                    filename = args.path + img['src']
                    with open(filename, "wb") as file:
                        file.write(img_download.content)
                        print(f"Class Link: Downloading image from: {img_download_link} to {filename}")
                        downloaded_images.add(img_download_link)
                except requests.exceptions.RequestException as error:
                    print(f"{error}")
                    print(f"Class Link: Failed to download image from {img_download_link}")
            else:
                print(f"Class Link: Skipping downloading image {img_download_link} since it was already downloaded")
    
    def getLinks(self) -> None:

        next_links = self.soup.find_all("a")
        for link_iter in next_links:
            full_link= urljoin(self.url, link_iter.get("href"))
            print(f"Found the following links on the page: {full_link}")
            all_unique_links.add(full_link)


            # self.links.add(full_link)




        
        


    

    # img_link = soup.find_all("img")



# downloaded_images = set()
# all_unique_links = set()
# all_already_scraped_links = set()

args = parsing_arguments()
arg_check(args)


link1 = Link(args.start_url)
link1.getPage()
link1.getLinks()
link1.downloadImages()
pending_links = all_unique_links - all_already_scraped_links

while pending_links:
    first = next(iter(pending_links))
    print(f"Checking link {first}")
    
    temp_link_obj = Link(first)
    temp_link_obj.getPage()
    temp_link_obj.getLinks()
    temp_link_obj.downloadImages()
    all_already_scraped_links.add(first)
    pending_links = all_unique_links - all_already_scraped_links


    # if first not in 

        
    #     print(f"Link_iter is {link_iter}")
    #     if link_iter not in all_already_scraped_links:
    #         print(f"Scraping Link_iter at {link_iter}")

    #         temp_link_obj = Link(link_iter)
    #         temp_link_obj.getPage()
    #         temp_link_obj.getLinks()
    #         temp_link_obj.downloadImages()
    #         temp_link_obj = None
    #         all_already_scraped_links.add(link_iter)





# for link_iter in all_unique_links:
#     print(f"Link_iter is {link_iter}")
#     if link_iter not in all_already_scraped_links:
#         print(f"Scraping Link_iter at {link_iter}")

#         temp_link_obj = Link(link_iter)
#         temp_link_obj.getPage()
#         temp_link_obj.getLinks()
#         temp_link_obj.downloadImages()
#         temp_link_obj = None
#         all_already_scraped_links.add(link_iter)


    # 1. make temporary Link object
    # 2. get page for this object, get links and downloaded_images
    # 3 add the link obj to exclusion set

    

# print(f"link1.soup.find_all(img) is {link1.soup.find_all("img")}")
      
# link1.getImages();
# link1.getLinks();
# link1.getPage().getImages()
# print(f"Link 1's url is {link1.url}")


print(f"Scraping website {args.start_url} for images")
print(f"Downloading files to {args.path}")
print(f"Downloads should be recursive {args.recursive}")
print(f"Level of recursion {args.level}")



# visited_links = set()
# all_scraped_links = set()
start_url = args.start_url

#start_url = "https://crawler-test.com/links/image_links"
#url = "https://en.wikipedia.org/wiki/Spinning_top"


# try:
#     response = requests.get(start_url)
#     response.raise_for_status()
#     print(f"Scraping page: {start_url}")
# except requests.exceptions.RequestException as error:
#     print(f"{error}")
#     sys.exit(1)




# visited_links.add(start_url)
# all_scraped_links.add(start_url)

# html = response.text
# soup = BeautifulSoup(html, "html.parser")

# img_link = soup.find_all("img")
# for img in img_link:
#     img_download_link = urljoin(start_url, img['src'])

#     if img_download_link not in downloaded_images:
#         try:
#             img_download = requests.get(img_download_link)
#             img_download.raise_for_status()
#             filename = args.path + img['src']
#             with open(filename, "wb") as file:
#                 file.write(img_download.content)
#                 print(f"Downloading image from: {img_download_link} to {filename}")
#                 downloaded_images.add(img_download_link)
#         except requests.exceptions.RequestException as error:
#             print(f"{error}")
#             print(f"Failed to download image from {img_download_link}")


#     else:
#         print(f"Skipping downloading image {img_download_link} since it was already downloaded")



# next_links = soup.find_all("a")
# for link in next_links:
    
#     full_link= urljoin(start_url, link.get("href"))
#     #print(f"Found the following links on the page: {full_link}")
#     all_scraped_links.add(full_link)


