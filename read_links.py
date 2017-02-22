import pickle
from glob import glob

if __name__ == '__main__':
    nb_links = 0
    all_news = glob('data/**/links/*.pkl', recursive=True)
    for news in all_news:
        content = pickle.load(open(news, 'rb'))
        nb_links += len(content)
    print('nb_link = {}'.format(nb_links))
