import json
import os
import pickle
from glob import iglob

OUTPUT_DIR = 'json-output'

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    all_news = iglob('data/**/news/*.pkl', recursive=True)
    for i, news in enumerate(all_news):
        content = pickle.load(open(news, 'rb'))
        keyword = news.split('/')[1]
        print('keyword = {}'.format(keyword))
        print('text = {}'.format(content['content']))
        print('text = {}'.format(content['datetime']))
        print('link = {}'.format(content['link']))
        print('title = {}'.format(content['title']))
        content['keyword'] = keyword
        print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-')
        output_filename = os.path.join(OUTPUT_DIR, '{}.json'.format(i))
        print(output_filename)
        with open(output_filename, 'w') as fp:
            json.dump(content, fp, sort_keys=True, indent=4, ensure_ascii=False)
