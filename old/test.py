from __future__ import print_function

import gnp

# b = gnp.get_google_news(gnp.EDITION_ENGLISH_US, geo='London,UK')
c = gnp.get_google_news_query("Honda+Factory")
import json

print(json.dumps(c, indent=4, sort_keys=True))