# Google News Scraper - Japanese only (for now)

## How to get started?

```
git clone git@github.com:philipperemy/google-news-scraper.git gns
cd gns
sudo pip install -r requirements.txt
python main_no_vpn.py
```
## Configuration

- `SLEEP_TIME_EVERY_TEN_ARTICLES_IN_SECONDS`: Sleep time before two calls to Google News. On average 10 articles are fetched per call.
- `ARTICLE_COUNT_LIMIT_PER_KEYWORD`: Maximum number of articles fetched for one keyword.
- `RUN_POST_PROCESSING`: Post processing means opening the URL, download the raw HTML from the articles, clean this HTML and save them to files.
- `LINKS_POST_PROCESSING_CLEAN_HTML_RATIO_LETTERS_LENGTH`: Technical parameter for the post processing. Apply to Japanese only. We are interesting in dropping the english sentences from the Japanese articles.
- `LINKS_POST_PROCESSING_NUM_THREADS`: Number of threads to use when doing this post processing task.
- `LINKS_POST_PROCESSING_MULTI_THREADING`: Enable/disable multithreading for for the postprocessing. 1 means multithreaded. 0 means no multithreading.

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
- you can `expressvpn` in your terminal.
- ExpressVPN is configured [https://www.expressvpn.com/setup](https://www.expressvpn.com/setup) and [https://www.expressvpn.com/support/vpn-setup/app-for-linux/#download](https://www.expressvpn.com/support/vpn-setup/app-for-linux/#download)
- you get `expressvpn-python (x.y)` where `x.y` is the version, when you run `pip list | grep "expressvpn-python"`

Once you have all of that, simply run:

```
python main.py
```

Every time the script detects that Google has banned you, it will request the VPN to get a fresh new IP and will resume.

