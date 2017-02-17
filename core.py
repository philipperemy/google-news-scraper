from __future__ import print_function

import errno
import os
import pickle
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from mtranslate import translate
from numpy import random
from slugify import slugify


class BannedFromGoogleException(Exception):
    pass


def forge_url(q, start, year_start, year_end):
    return 'https://www.google.co.jp/search?q={}&hl=ja&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{}%2Ccd_max%3A{}&tbm=nws&start={}'.format(
        q.replace(' ', '+'), str(year_start), str(year_end), start)


def extract_links(content):
    soup = BeautifulSoup(content, 'html.parser')  # _sQb top _vQb _mnc
    tag_1 = 'l _HId'
    links_1 = [(v.attrs['href'], v.text) for v in soup.find_all('a', {'class': tag_1})]

    tag_2 = '_sQb'
    links_2 = [(v.attrs['href'], v.text) for v in soup.find_all('a', {'class': tag_2})]

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

        nb_links = len(links)
        if nb_links == 0 and num_articles_index == 0:
            print('Banned from Google. Retry tomorrow or change of IP Address.')
            raise BannedFromGoogleException()

        for i in range(nb_links):
            if debug:
                print('{}'.format(links[i]))
        num_articles_index += 10
        result.extend(links)
        if debug and sleep_time_every_ten_articles != 0:
            print('Program is going to sleep for {} seconds.'.format(sleep_time_every_ten_articles))
        time.sleep(sleep_time_every_ten_articles)
    return result


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_keywords():
    response = requests.get('http://www.generalecommerce.com/clients/broadcastnews_tv/category_list_js.html')
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, 'html.parser')
    keywords = [l.replace('news', '') for l in
                set([v.text for v in soup.find_all('td', {'class': 'devtableitem'}) if 'http' not in v.text])]
    assert len(keywords) > 0
    # japanese_keywords = []

    random.shuffle(keywords)
    for keyword in keywords:
        japanese_keyword = translate(keyword, 'ja')
        print('[Google Translate] {} -> {}'.format(keyword, japanese_keyword))
        if re.search('[a-zA-Z]', japanese_keyword):  # we don't want that: Fed watch -> Fed時計
            continue
        yield japanese_keyword
        # japanese_keywords.append(japanese_keyword)
        # return japanese_keywords


def run():
    for keyword in get_keywords():
        print('KEYWORD = {}'.format(keyword))
        generate_articles(keyword)


def generate_articles(keyword, year_start=2010, year_end=2016, limit=300):
    tmp_news_folder = 'data/{}/news'.format(keyword)
    mkdir_p(tmp_news_folder)

    tmp_link_folder = 'data/{}/links'.format(keyword)
    mkdir_p(tmp_link_folder)

    pickle_file = '{}/{}_{}_{}_links.pkl'.format(tmp_link_folder, keyword, year_start, year_end)
    if os.path.isfile(pickle_file):
        links = pickle.load(open(pickle_file, 'rb'))
    else:
        links = google_news_run(keyword=keyword,
                                limit=limit,
                                year_start=year_start,
                                year_end=year_end,
                                debug=True,
                                sleep_time_every_ten_articles=10)
        pickle.dump(links, open(pickle_file, 'wb'))

    full_articles = []
    for full_link in links:
        link = full_link[0]
        title = full_link[1]
        compliant_filename_for_link = slugify(link)
        max_len = 100
        if len(compliant_filename_for_link) > max_len:
            print('max length exceeded for filename ({}). Truncating.'.format(compliant_filename_for_link))
            compliant_filename_for_link = compliant_filename_for_link[:max_len]
        pickle_file = '{}/{}.pkl'.format(tmp_news_folder, compliant_filename_for_link)
        already_fetched = os.path.isfile(pickle_file)
        if already_fetched:
            article = pickle.load(open(pickle_file, 'rb'))
        else:
            try:
                raw_text = download_html_from_link(link)
            except:
                raw_text = ''
                print('ERROR could not download article with link {}'.format(link))
            text = clean_html(raw_text, filter_on_paragraph_length=60)
            article = {'link': link,
                       'title': title,
                       'text': text,
                       'raw_text': raw_text,
                       }
            pickle.dump(article, open(pickle_file, 'wb'))
        full_articles.append(article)
    return full_articles


def get_google_search_results(keyword):
    links = []
    for start in range(0, 10):
        url = "https://www.google.co.jp/search?q={}&start={}".format(keyword, str(start * 10))
        page = requests.get(url).content
        soup = BeautifulSoup(page, 'html.parser')
        for cite in soup.findAll('cite'):
            links.append(cite.text)
    return links


def download_html_from_link(link, params=None, fail_on_error=True, debug=True):
    try:
        if debug:
            print('Get -> {} '.format(link), end='')
        response = requests.get(link, params, timeout=20)
        if fail_on_error and response.status_code != 200:
            raise Exception('Response code is not [200]. Got: {}'.format(response.status_code))
        else:
            print('[OK]')
        return response.content
    except:
        if fail_on_error:
            raise
        return None


def clean_html(html_page, filter_on_paragraph_length=60):
    if html_page is None:
        return ''
    soup = BeautifulSoup(html_page, 'html.parser')
    text = '\n\n'.join([v.text for v in soup.find_all('p') if len(v.text) > 0])
    if filter_on_paragraph_length > 0:
        text = '. '.join([v for v in text.split('\n') if len(v) > filter_on_paragraph_length])
    return text


if __name__ == '__main__':
    print(get_keywords())
    _html_ = download_html_from_link('http://www.motortrend.com/cars/toyota/camry/2007/0603fs-2007-toyota-camry/')
    print(clean_html(_html_))
    print(get_google_search_results('hello'))
