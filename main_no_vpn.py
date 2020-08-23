import logging
import sys
from argparse import ArgumentParser

from core import run


def get_script_arguments():
    args = ArgumentParser()
    args.add_argument('--keywords', default=None, type=str)
    args.add_argument('--language', default='ja')
    args.add_argument('--retrieve_content_behind_links', action='store_true')
    args.add_argument('--limit_num_links_per_keywords', default=50, type=int)
    args.add_argument('--num_threads', default=1, type=int)
    return args.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
    # https://news.google.co.jp
    # https://news.google.com/?output=rss&hl=fr
    # RSS Feed does not work for Japanese language.
    args = get_script_arguments()
    run(args.keywords.split(','), args.language, args.limit_num_links_per_keywords,
        args.retrieve_content_behind_links, args.num_threads)


if __name__ == '__main__':
    main()
