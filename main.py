from core import run
from expressvpn import wrapper

if __name__ == '__main__':
    # https://news.google.co.jp
    # https://news.google.com/?output=rss&hl=fr
    # RSS Feed does not work for Japanese language.
    # get_articles('プロクター・アンド・ギャンブル')

    while True:
        try:
            run()
        except Exception as e:
            print('EXCEPTION CAUGHT in __MAIN__')
            print(e)
            print('Lets change our PUBLIC IP GUYS!')
            wrapper.random_connect()
