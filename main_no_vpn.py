import logging
import sys

from core import run

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

    # https://news.google.co.jp
    # https://news.google.com/?output=rss&hl=fr
    # RSS Feed does not work for Japanese language.
    # get_articles('プロクター・アンド・ギャンブル')
    if len(sys.argv) > 1:
        keywords = sys.argv[1].split(',')
    else:
        keywords = None
    run()
