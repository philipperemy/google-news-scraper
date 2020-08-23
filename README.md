# Google News Scraper - Japanese only

For english articles, Google has a RSS feed that you can directly use: https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en.

Each scraped article has the following fields:
- **title**: Title of the article
- **datetime**: Publication date
- **content**: Full content (text format)
- **link**: URL where the article was published
- **keyword**: Google News keyword used to find this article

## How many articles can I fetch with this scraper?

No upper bound of course but it should be in the range **`100,000 articles per day`** when scraping 24/7 with VPN enabled.

## How to get started?
```bash
git clone git@github.com:philipperemy/google-news-scraper.git && cd google-news-scraper
virtualenv -p python3 venv && source venv/bin/activate # optional but recommended!
pip install -r requirements.txt
python main_no_vpn.py # for VPN support, scroll down!
```

## Output example

`Article 1`
```
{
    "content": "(本文中の野村証券 [...] 生命経済研の熊野英生氏は指摘。  記事の全文 \n保護主義を根拠とする円高説を信じ込むのは禁物であり、実際は米貿易赤字縮小と円安が進むかもしれないとＢＢＨの村田雅志氏は指摘。  記事の全文 \n",
    "datetime": "2015/11/03",
    "keyword": "米国の銀行業務",
    "link": "http://jp.reuters.com/article/idJPL3N12Y5QX20151104",
    "title": "再送-インタビュー：運用高度化、ＰＥやハイイールド債増やす＝長門・ゆうちょ銀社長"
}
```

`Article 2`

```
{
    "content": "記事保存 有料会員の方のみご利用になれます。[...] 詳しくは、こちら 電子版トップ速報トップ アルゼンチン、ドル、通貨ペソ、外貨取引 来春の新入社員を募集　記者など４職種 【週末新紙面】宅配＋電子版お試し実施中！ 天気 プレスリリース検索 アカウント一覧 訂正・おわび",
    "datetime": "2015/12/17",
    "keyword": "アルゼンチン",
    "link": "http://www.nikkei.com/article/DGXLASGM18H1B_Y5A211C1EAF000/",
    "title": "アルゼンチンの通貨ペソ、大幅下落 対ドルで36％安"
}
```
**NOTE**: The field `content` was truncated for improving the readibility.

## Configuration
- `SLEEP_TIME_EVERY_TEN_ARTICLES_IN_SECONDS`: Sleep time before two calls to Google News. On average 10 articles are fetched per call. Default value is 1 second.
- `ARTICLE_COUNT_LIMIT_PER_KEYWORD`: Maximum number of articles fetched for one keyword. Default value is 300. I tried it up to 600 and it worked.
- `RUN_POST_PROCESSING`: Post processing means opening the URL of the article and extracting the content. **For maximum efficiency, we first scrape all the available tuples (title, datetime, url) on Google.com. Then, from the collected URLs, we fetch the content. This two-step procedure is empirically more efficient.** Run first `RUN_POST_PROCESSING` with a value of 0. Then, run it a second time with `RUN_POST_PROCESSING` set to 1. All the Google data scraped is persisted so no problem!
- `LINKS_POST_PROCESSING_CLEAN_HTML_RATIO_LETTERS_LENGTH`: Technical parameter for the post processing. Apply to Japanese only. We are interesting in dropping the english sentences from the Japanese articles. Default is 0.33.
- `LINKS_POST_PROCESSING_NUM_THREADS`: Number of threads to use when doing this post processing task. Default is 8.

## VPN
Scraping Google News usually results in a ban for a few hours. Using a VPN with dynamic IP fetching is a way to overcome this problem.

In my case, I subscribed to this VPN: [https://www.expressvpn.com/](https://www.expressvpn.com/).

I provide a python binding for this VPN here: [https://github.com/philipperemy/expressvpn-python](https://github.com/philipperemy/expressvpn-python).

Run those commands in Ubuntu 64 bits to configure the VPN with the Google News Scraper project:
```
git clone git@github.com:philipperemy/expressvpn-python.git evpn
cd evpn
sudo dpkg -i expressvpn_1.2.0_amd64.deb # will install the binaries provided by ExpressVPN
sudo pip install . # will install it as a package
```

Also make sure that:
- you can run `expressvpn` in your terminal.
- ExpressVPN is properly configured:
    - [https://www.expressvpn.com/setup](https://www.expressvpn.com/setup) 
    - [https://www.expressvpn.com/support/vpn-setup/app-for-linux/#download](https://www.expressvpn.com/support/vpn-setup/app-for-linux/#download)
- you get `expressvpn-python (x.y)` where `x.y` is the version, when you run `pip list | grep "expressvpn-python"`

Once you have all of that, simply run:

```
# I advise you to set RUN_POST_PROCESSING=0 in conf.json, run main.py. 
# It will gather all the Google data in data/. Then stop the script.
# Change the parameter RUN_POST_PROCESSING=1 and run it again.
# The script will read from data/ and start fetching the content of the links.
python main.py
```

Every time the script detects that Google has banned you, it will request the VPN to get a fresh new IP and will resume.

## Questions/Answers
- Why didn't you use the RSS feed provided by Google News? It does not exist for Japanese!
- What is the best way to use this scraper? If you want to scrape a lot of data, I highly recommend you to subscribe to a VPN, preferably ExpressVPN (I implemented the VPN wrapper and the interaction with this scraper).
