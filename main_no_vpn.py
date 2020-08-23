import logging
import sys
from argparse import ArgumentParser

from core import run


def get_script_arguments():
    args = ArgumentParser()
    args.add_argument('--keywords', default=None, type=str)
    args.add_argument('--language', default='ja')
    args.add_argument('--retrieve_content_behind_links', action='store_true')
    args.add_argument('--limit_num_links_per_keyword', default=50, type=int)
    args.add_argument('--num_threads', default=1, type=int)
    return args.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
    # https://news.google.com/?output=rss&hl=fr
    # RSS Feed does not work for Japanese/Chinese language.
    args = get_script_arguments()
    keywords = args.keywords.split(',') if args.keywords is not None else None
    run(
        keywords=keywords,
        language=args.language,
        limit=args.limit_num_links_per_keyword,
        retrieve_content_behind_links=args.retrieve_content_behind_links,
        num_threads=args.num_threads
    )


if __name__ == '__main__':
    main()
