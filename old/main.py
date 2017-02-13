


def get_articles(keyword, year_start=2015, year_end=2016, limit=100):
    tmp_news_folder = 'data/{}/news'.format(keyword)
    mkdir_p(tmp_news_folder)

    tmp_link_folder = 'data/{}/links'.format(keyword)
    mkdir_p(tmp_link_folder)

    pickle_file = '{}/{}_{}_{}_links.pkl'.format(tmp_link_folder, keyword, year_start, year_end)
    if os.path.isfile(pickle_file):
        links = pickle.load(open(pickle_file, 'rb'))
    else:
        if KEYWORD not in keyword:
            keyword_q = KEYWORD + ' ' + keyword
        else:
            keyword_q = keyword
        links = get_news_from_google(keyword=keyword_q,
                                     limit=limit,
                                     year_start=year_start,
                                     year_end=year_end,
                                     debug=True,
                                     sleep_time_every_ten_articles=10)
        pickle.dump(links, open(pickle_file, 'wb'))

    articles = []
    for link in links:
        # start_time = time.time()
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
            article = clean_html(article, filter_on_paragraph_length=10)
            pickle.dump(article, open(pickle_file, 'wb'))

        articles.append(article)
        # print('Processing link {0:}. Took {1:.2f} seconds. already fetched = {2:}'.format(link,
        #                                                                                  time.time() - start_time,
        #                                                                                  already_fetched))
    return articles, links


if __name__ == '__main__':
    get_articles(keyword, year_start=2015, year_end=2016, limit=100)