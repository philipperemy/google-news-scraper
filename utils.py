import errno
import os
import pickle

import requests
from bs4 import BeautifulSoup
from slugify import slugify

from core import google_news_run


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
    return keywords


def run():
    for keyword in get_keywords():
        print('KEYWORD = {}'.format(keyword))
        get_articles(keyword)


def get_articles(keyword, year_start=2010, year_end=2016, limit=100):
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

    articles = []
    for full_link in links:
        link = full_link[0]
        title = full_link[1]
        compliant_filename_for_link = slugify(link)
        pickle_file = '{}/{}.pkl'.format(tmp_news_folder, compliant_filename_for_link)
        already_fetched = os.path.isfile(pickle_file)
        if already_fetched:
            article = pickle.load(open(pickle_file, 'rb'))
        else:
            try:
                article = download_html_from_link(link)
            except:
                article = ''
                print('ERROR could not download article with link {}'.format(link))
            article = clean_html(article, filter_on_paragraph_length=60)
            pickle.dump({'link': link,
                         'title': title,
                         'article': article
                         },
                        open(pickle_file, 'wb'))
        articles.append(article)
    return articles, links


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
