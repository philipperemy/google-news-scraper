#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mtranslate import translate

from core import retrieve_data_from_links


def test_google_translate_api():
    to_translate = 'Procter & Gamble'
    print(translate(to_translate))
    print(translate(to_translate, 'ja'))
    print(translate(to_translate, 'ru'))


if __name__ == '__main__':
    # main()
    # links = [('http://www.excite.co.jp/News/column_g/20161115/TokyoFm_QICfvc0b1m.html',
    #          'コレってアリ!? 私が体験した「飲食店」ドン引きエピソード')]
    # links = [('http://www.sankei.com/west/news/160610/wst1606100085-n1.html',
    #          '尾道市の飲食店から出火、２４棟に延焼 ２人けが、１人体調不良に')]
    # links = [('https://www.travelvoice.jp/20160808-71985',
    #          'グーグル検索から飲食店予約が可能に、ホットペッパー・食べログ・一休に ...')]

    # links = [('http://www.news24.jp/articles/2016/06/27/07333796.html', '車の自動走行に向け課題を議論 警察庁')]
    # links = [('http://ascii.jp/elem/000/000/606/606175/', '日立ソリューションズ、在宅勤務「SecureOnline」にWeb認証')]
    # links = [('http://the-liberty.com/article.php?item_id=10396', '安倍首相、中央アジア訪問 中国の経済支援との質的違いとは?')]
    links = [('http://tower.jp/article/feature_item/2015/05/19/0105', 'チルアウト/バレアリック界のレジェンド＝ホセ・パディーヤ、14年振り新作')]
    retrieve_data_from_links(links, '')
