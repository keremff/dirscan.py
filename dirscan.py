import requests
from concurrent.futures import ThreadPoolExecutor
import time
import sys
from fake_useragent import UserAgent

__author__ = 'keremff'
__version__ = '0.2.0'

try:
    sys.argv[1]
    sys.argv[2]
except:
    print('Usage: py dirscan.py "https://url.com" "wordlist.txt"')
    exit()


def request(url):
    headers = {'User-Agent': UserAgent().firefox}
    return requests.get(url, headers=headers)


try:
    if request(sys.argv[1]).status_code > 399:
        exit('Target has scraping protection, exiting.')
except:
    exit("Url down or not valid, exiting.")


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
        for response in executor.map(request, List):
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
    wordlist = sys.argv[2]
    start = time.perf_counter()
    urls = []
    load_wordlist(url, wordlist, urls)
    try_urls(urls)
    end = time.perf_counter()
    print(f'Time elapsed: {end - start:.1f} seconds')


if __name__ == "__main__":
    main()
