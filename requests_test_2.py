from __future__ import print_function

import requests
from bs4 import BeautifulSoup


def forge_url(q, start):
    return 'https://www.google.co.jp/search?q={}&hl=en&tbm=nws&start={}'.format(q.replace(' ', '+'), start)


def index(str1, pattern):
    """ because '&'.index(str) did not work for HTML strings!"""
    N = len(pattern)
    for i in range(0, len(str1) - N):
        if str1[i:i + N] == pattern:
            return i
    return -1


# extract timestamp : <span class="f">
def extract_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    links = [v.contents[0].attrs['href'][7:] for v in soup.find_all('h3', {"class": "r"})]
    links = [link[0:index(link, '&')] for link in links]
    dates = [v.string.split('-')[1] for v in soup.find_all('span', {"class": "f"}) if '-' in v.string]
    return links, dates


def run(q, limit=10):
    num_articles_index = 0
    while num_articles_index < limit:
        url = forge_url(q, num_articles_index)
        print('For Google -> {}'.format(url))
        response = requests.get(url)
        links, dates = extract_links(response.content)
        for i in range(len(links)):
            print('{} - {}'.format(links[i], dates[i]))
        num_articles_index += 10


run(q='Honda Factory', limit=40)
