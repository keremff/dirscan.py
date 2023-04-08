import requests
from concurrent.futures import ThreadPoolExecutor
import time
import sys

__author__ = ''


try:
    sys.argv[1]
    sys.argv[2]
except:
    print('Usage: py dirscan.py "https://url.com" "wordlist.txt"')
    exit()


def check_url(url):
    if requests.get(url).status_code != 200:
        print(f'Target has scraping protection. (status code : {requests.get(url).status_code})')


def load_wordlist(url, wordlist, List):  # combine the url with wordlist into a list to loop through it
    with open(wordlist, 'r') as f:
        for word in f:
            List.append(f'{url}/{word.strip()}')


def check_status(response):
    return response.status_code


def try_urls(List):
    found_list = []  # This is used to make sure same url doesn't get printed twice
    found = 0
    with ThreadPoolExecutor(max_workers=120) as executor:
        for response in executor.map(requests.get, List):
            if check_status(response) == 200:
                if response.url in found_list:
                    pass
                else:
                    found_list.append(response.url)
                    found += 1
                    print(f'Found ====> {response.url}')
    print(f'\nFinished. Found {found} directory.')


def main():
    url = sys.argv[1]
    check_url(url)
    wordlist = sys.argv[2]
    start = time.perf_counter()
    urls = []
    load_wordlist(url, wordlist, urls)
    try_urls(urls)
    end = time.perf_counter()
    print(f'Time elapsed: {end - start:.1f} seconds')


if __name__ == "__main__":
    main()
