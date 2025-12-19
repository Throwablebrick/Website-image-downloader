import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import os
from PIL import Image

def images_to_pdf(pictures, new_pdf):
    all_pics = [Image.open(pic) for pic in pictures]
    ready_pics = [pic.convert('RGB') for pic in all_pics]
    ready_pics[0].save(new_pdf, save_all=True, append_images=ready_pics[1:])

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Image downloaded successfully as {filename}')
    else:
        print(f'Failed to download image: {response.status_code}')

urls = list()
names = list()
odd = True

file = open("input.txt", "r")
for line in file:
    if odd:
        urls.append(line.strip())
    else:
        names.append(line.strip())
    odd = not odd
file.close()

for i in range(len(urls)):
    url = urls[i]
    name = names[i]
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        print("souping it or something")
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to fetch page: {response.status_code}")
        exit()

    print("finding all the images")
    images = soup.find_all('img')

    print("mucking with urls")
    image_urls = []
    for image in images:
        image_url = image.get('src')
        if image_url:
            full_url = urljoin(url, image_url)
            image_urls.append(full_url)

    image_paths = []
    num = 0
    image = name

    if "readallcomics" in url:
        image_urls.pop(0)

    for i in image_urls:
        path = f'{image}{num:04}.png'
        download_image(i, path)
        image_paths.append(path)
        num += 1
        #time.sleep(0.2)  # Prevent overwhelming the server

    print("making pdf")
    images_to_pdf(image_paths, f'{image}.pdf')

    print("deleting images")
    for i in image_paths:
        os.remove(i)
