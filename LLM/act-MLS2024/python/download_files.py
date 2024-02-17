#!/usr/bin/env python
import os
import requests
import fire
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def download_files(url, folder_location, file_types=['pdf', 'zip']):
    os.makedirs(folder_location, exist_ok=True)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") 

    for file_type in file_types:
        for link in soup.select(f"a[href$='.{file_type}']"):
            filename = os.path.join(folder_location,link['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url,link['href'])).content)

if __name__ == '__main__':
    fire.Fire(download_files)