import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Image downloaded successfully as {filename}')
    else:
        print(f'Failed to download image: {response.status_code}')


url = input("enter url: ")
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
else:
    print(f"Failed to fetch page: {response.status_code}")
    exit()

images = soup.find_all('img')

image_urls = []
for image in images:
    image_url = image.get('src')
    if image_url:
        full_url = urljoin(url, image_url)
        image_urls.append(full_url)

num = 0
image = input("enter the name for the files: ")
for i in image_urls:
    download_image(i, f'{image}{num}.png')
    num += 1
    #time.sleep(0.2)  # Prevent overwhelming the server
