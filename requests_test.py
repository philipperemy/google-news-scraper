from __future__ import print_function

import requests


def forge_url(q, start):
    return 'https://www.google.co.jp/search?q={}&hl=en&tbm=nws&start={}'.format(q.replace(' ', '+'), start)


URL = 'https://www.google.co.jp/search?q=Honda&hl=en&tbm=nws&start=20'


def find_indexes(str1, pattern, return_only_first=False, length_check=10):
    N = len(pattern)
    found_indexes = []
    for i in range(0, len(str1) - N):
        if str1[i:i + N] == pattern:
            if return_only_first:
                return i
            found_indexes.append(i)
    if length_check != len(found_indexes):
        raise Exception('Length differ. We expected {} articles. Found {}'.format(length_check, len(found_indexes)))
    return found_indexes


# extract timestamp : <span class="f">
def extract_links(content):
    # print(content)
    start_pattern = '<h3 class="r"><a href="/url?q='
    start_indexes = find_indexes(content, start_pattern)
    links = []
    for start_index in list(start_indexes):
        end_index = start_index + find_indexes(content[start_index:], '&amp', return_only_first=True, length_check=1)
        link = content[start_index:end_index][len(start_pattern):]
        links.append(link)
        print(link)
    return links


def run(q, limit=10):
    num_articles_index = 0
    while num_articles_index < limit:
        url = forge_url(q, num_articles_index)
        print('For Google -> {}'.format(url))
        response = requests.get(url)
        extract_links(response.content)
        num_articles_index += 10


run(q='Honda Factory', limit=40)
