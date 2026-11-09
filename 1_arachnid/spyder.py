import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlopen

url = "https://crawler-test.com/links/image_links"
#url = "https://en.wikipedia.org/wiki/Spinning_top"

response    = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")
print(soup.title.text)

img_link = soup.find_all("img")
for img in img_link:
    print(img['src'])
    img_download_link = urljoin(url, img['src'])
    img_download = requests.get(img_download_link)
    print(img_download);
