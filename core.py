from __future__ import print_function

import errno
import logging
import os
import pickle
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from mtranslate import translate
from slugify import slugify

from constants import *

NUMBER_OF_CALLS_TO_GOOGLE_NEWS_ENDPOINT = 0

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def parallel_function(f, sequence, num_threads=None):
    from multiprocessing import Pool
    pool = Pool(processes=num_threads)
    result = pool.map(f, sequence)
    cleaned = [x for x in result if x is not None]
    pool.close()
    pool.join()
    return cleaned


def forge_url(q, start, year_start, year_end):
    global NUMBER_OF_CALLS_TO_GOOGLE_NEWS_ENDPOINT
    NUMBER_OF_CALLS_TO_GOOGLE_NEWS_ENDPOINT += 1
    return GOOGLE_NEWS_URL.format(q.replace(' ', '+'), str(year_start), str(year_end), start)


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
            logging.debug('For Google -> {}'.format(url))
            logging.debug('Total number of calls to Google = {}'.format(NUMBER_OF_CALLS_TO_GOOGLE_NEWS_ENDPOINT))
        headers = {'User-Agent': ua.chrome}
        try:
            response = requests.get(url, headers=headers, timeout=20)
            links = extract_links(response.content)

            nb_links = len(links)
            if nb_links == 0 and num_articles_index == 0:
                raise Exception(
                    'No results fetched. Either the keyword is wrong '
                    'or you have been banned from Google. Retry tomorrow '
                    'or change of IP Address.')

            for i in range(nb_links):
                if debug:
                    cur_link = links[i]
                    logging.debug('TITLE = {}, URL = {}'.format(cur_link[1], cur_link[0]))
            result.extend(links)
        except requests.exceptions.Timeout:
            logging.debug('Google news TimeOut. Maybe the connection is too slow. Skipping.')
            pass
        num_articles_index += 10
        if debug and sleep_time_every_ten_articles != 0:
            logging.debug('Program is going to sleep for {} seconds.'.format(sleep_time_every_ten_articles))
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
    response = requests.get('http://www.generalecommerce.com/clients/broadcastnews_tv/category_list_js.html',
                            timeout=20)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, 'html.parser')
    keywords = [l.replace('news', '') for l in
                set([v.text for v in soup.find_all('td', {'class': 'devtableitem'}) if 'http' not in v.text])]
    assert len(keywords) > 0

    random.shuffle(keywords)
    for keyword in keywords:
        japanese_keyword = translate(keyword, 'ja')
        logging.debug('[Google Translate] {} -> {}'.format(keyword, japanese_keyword))
        if re.search('[a-zA-Z]', japanese_keyword):  # we don't want that: Fed watch -> Fed時計
            continue
        yield japanese_keyword


def run():
    for keyword in get_keywords():
        logging.debug('KEYWORD = {}'.format(keyword))
        generate_articles(keyword)


def generate_articles(keyword, year_start=2010, year_end=2016, limit=ARTICLE_COUNT_LIMIT_PER_KEYWORD):
    tmp_news_folder = 'data/{}/news'.format(keyword)
    mkdir_p(tmp_news_folder)

    tmp_link_folder = 'data/{}/links'.format(keyword)
    mkdir_p(tmp_link_folder)

    pickle_file = '{}/{}_{}_{}_links.pkl'.format(tmp_link_folder, keyword, year_start, year_end)
    if os.path.isfile(pickle_file):
        logging.debug('Google news links for keyword [{}] have been fetched already.'.format(keyword))
        links = pickle.load(open(pickle_file, 'rb'))
        logging.debug('Found {} links.'.format(len(links)))
    else:
        links = google_news_run(keyword=keyword,
                                limit=limit,
                                year_start=year_start,
                                year_end=year_end,
                                debug=True,
                                sleep_time_every_ten_articles=SLEEP_TIME_EVERY_TEN_ARTICLES_IN_SECONDS)
        pickle.dump(links, open(pickle_file, 'wb'))
    retrieve_data_from_links(links, tmp_news_folder)


def retrieve_data_for_link(param):
    logging.debug('retrieve_data_for_link - param = {}'.format(param))
    (full_link, tmp_news_folder) = param
    link = full_link[0]
    google_title = full_link[1]
    compliant_filename_for_link = slugify(link)
    max_len = 100
    if len(compliant_filename_for_link) > max_len:
        logging.debug('max length exceeded for filename ({}). Truncating.'.format(compliant_filename_for_link))
        compliant_filename_for_link = compliant_filename_for_link[:max_len]
    pickle_file = '{}/{}.pkl'.format(tmp_news_folder, compliant_filename_for_link)
    already_fetched = os.path.isfile(pickle_file)
    if not already_fetched:
        try:
            raw_text = download_html_from_link(link)
        except:
            raw_text = ''
            logging.debug('ERROR could not download article with link {}'.format(link))
        text, full_title = clean_html_and_complete_title(raw_text, google_title)
        text = re.sub('\s\s+', ' ', text)  # remove multiple spaces.
        article = {'link': link,
                   'title': full_title,
                   'text': text,
                   'raw_text': raw_text,
                   }
        pickle.dump(article, open(pickle_file, 'wb'))


def retrieve_data_from_links(full_links, tmp_news_folder):
    if MULTI_THREADING:
        inputs = [(full_links, tmp_news_folder) for full_links in full_links]
        parallel_function(retrieve_data_for_link, inputs, NUM_THREADS)
    else:
        for full_link in full_links:
            retrieve_data_for_link((full_link, tmp_news_folder))


def download_html_from_link(link, params=None, fail_on_error=True, debug=True):
    try:
        if debug:
            logging.debug('Get -> {} '.format(link), end='')
        response = requests.get(link, params, timeout=20)
        if fail_on_error and response.status_code != 200:
            raise Exception('Response code is not [200]. Got: {}'.format(response.status_code))
        else:
            logging.debug('[OK]')
        return response.content
    except:
        if fail_on_error:
            raise
        return None


def update_title(soup, google_article_title):
    if '...' not in google_article_title:
        return google_article_title
    truncated_title = google_article_title[:-4]  # remove ' ...' at the end.
    title_list = [v.text for v in soup.find_all('h1') if len(v.text) > 0]
    for title in title_list:
        if truncated_title in title:
            return title
    return google_article_title


def clean_html_and_complete_title(html_page, google_article_title):
    if html_page is None:
        return ''
    soup = BeautifulSoup(html_page, 'html.parser')
    # soup.contents (show without formatting).
    text_list = [v.text for v in soup.find_all('p') if len(v.text) > 0]

    words_to_bans = ['<', 'javascript']
    for word_to_ban in words_to_bans:
        text_list = list(filter(lambda x: word_to_ban not in x.lower(), text_list))

    text_list = [t for t in text_list if
                 len(re.findall('[a-z]', t.lower())) / (len(t) + 1) < CLEAN_HTML_RATIO_LETTERS_LENGTH]

    text = ' '.join(text_list)
    text = text.replace('\n', ' ')
    full_title = update_title(soup, google_article_title).strip()
    if full_title != google_article_title:
        logging.debug('updated title: old is [{}], new is [{}]'.format(google_article_title, full_title))
    return text, full_title
