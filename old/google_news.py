from __future__ import print_function

import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def forge_url(q, start, year_start, year_end):
    return 'https://www.google.co.jp/search?q={}&hl=en&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{}%2Ccd_max%3A{}&tbm=nws&start={}'.format(
        q.replace(' ', '+'), str(year_start), str(year_end), start)


def index(str1, pattern):
    """ because '&'.index(str) did not work for HTML strings!"""
    N = len(pattern)
    for i in range(0, len(str1) - N):
        if str1[i:i + N] == pattern:
            return i
    return -1


def find_all_indices(text, pattern):
    indices = []
    idx = 0
    while idx < len(text):
        idx = text.find(pattern, idx)
        if idx == -1:
            break
        indices.append(idx)
        idx += len(pattern)
    return indices


def extract_links(content):
    soup = BeautifulSoup(content, 'html.parser')  # _sQb top _vQb _mnc
    # soup.find_all('span', {'class':'f nsa _uQb'})
    # soup.find_all('a', {'class':'top _vQb _mnc'})
    # soup.find_all('a', {'class':'_sQb'})
    tag_1 = 'top _vQb _mnc'
    links_1 = [v.attrs['href'] for v in soup.find_all('a', {'class': tag_1})]
    #    indices_tag_1 = find_all_indices(content, tag_1)

    tag_2 = '_sQb'
    links_2 = [v.attrs['href'] for v in soup.find_all('a', {'class': tag_2})]
    #    indices_tag_2 = find_all_indices(content, tag_2)

    # TODO: link the dates here.
    # tag_dates = 'f nsa _uQb'
    # dates = [str(v.contents[0]) for v in soup.find_all('span', {'class': tag_dates})]

    return list(set(links_1 + links_2))


def google_news_run(keyword, limit=10, year_start=2010, year_end=2011, debug=True, sleep_time_every_ten_articles=0):
    if limit > 500:
        raise Exception('You are likely to be banned from Google if you set the limit too high.')
    num_articles_index = 0
    ua = UserAgent()
    result = []
    while num_articles_index < limit:
        url = forge_url(keyword, num_articles_index, year_start, year_end)
        if debug:
            print('For Google -> {}'.format(url))
        headers = {'User-Agent': ua.chrome}
        response = requests.get(url, headers=headers)
        links = extract_links(response.content)
        for i in range(len(links)):
            if debug:
                print('{}'.format(links[i]))
        num_articles_index += 10
        result.extend(links)
        if debug and sleep_time_every_ten_articles != 0:
            print('Program is going to sleep for {} seconds.'.format(sleep_time_every_ten_articles))
        time.sleep(sleep_time_every_ten_articles)
    return result
