from core import run
from expressvpn import wrapper


def get_new_ip():
    while True:
        try:
            print('GETTING NEW IP')
            wrapper.random_connect()
            print('SUCCESS')
            return
        except:
            pass


if __name__ == '__main__':
    # https://news.google.co.jp
    # https://news.google.com/?output=rss&hl=fr
    # RSS Feed does not work for Japanese language.
    # get_articles('プロクター・アンド・ギャンブル')

    while True:
        try:
            run()
        except:
            print('EXCEPTION CAUGHT in __MAIN__')
            print('Lets change our PUBLIC IP GUYS!')
            get_new_ip()
