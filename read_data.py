from glob import glob
import pickle

if __name__ == '__main__':
    all_news = glob('data/**/news/*.pkl', recursive=True)
    for news in all_news:
        print('keyword = {}'.format(news.split('/')[1]))
        content = pickle.load(open(news, 'rb'))
        print('link = {}'.format(content['link']))
        print('text = {}'.format(content['text']))
        print('title = {}'.format(content['title']))
        print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-')