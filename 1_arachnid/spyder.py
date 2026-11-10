import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

save_path = "data/"

url = "https://crawler-test.com/links/image_links"
#url = "https://en.wikipedia.org/wiki/Spinning_top"

response = requests.get(url)
response.raise_for_status()
html = response.text
soup = BeautifulSoup(html, "html.parser")

img_link = soup.find_all("img")
for img in img_link:
    img_download_link = urljoin(url, img['src'])
    img_download = requests.get(img_download_link)
    print(f"Downloading image from: {img_download_link}")
    #img_download.raise_for_status()
    filename = Path(img_download_link).name
    with open(save_path+filename, "wb") as file:
        file.write(img_download.content)
