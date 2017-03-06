import re

from constants import data


def get_content(soup):
    """Retrieves contents of the article"""
    content = ''
    # heuristics
    div_tags = soup.find_all('div', id='articleContentBody')
    div_tags_2 = soup.find_all('div', class_='ArticleText')
    div_tags_3 = soup.find_all('div', id='ArticleText')
    div3 = soup.find_all('div', id='article_content')
    div4 = soup.find_all('div', class_='articleBodyText')
    div5 = soup.find_all('div', class_='story-container')
    div_tags_l = soup.find_all('div', id=re.compile('article'))
    div6 = soup.find_all('div', class_='kizi-honbun')
    div7 = soup.find_all('div', class_='main-text')
    rest = soup.find_all(id='articleText')

    if div_tags:
        return collect_content(div_tags)
    elif div_tags_2:
        return collect_content(div_tags_2)
    elif div_tags_3:
        return collect_content(div_tags)
    elif div3:
        return collect_content(div3)
    elif div4:
        return collect_content(div4)
    elif div5:
        return collect_content(div5)
    elif div_tags_l:
        return collect_content(div_tags_l)
    elif div6:
        return collect_content(div6)
    elif div7:
        return collect_content(div7)
    elif rest:
        return collect_content(rest)
    else:
        # contingency
        c_list = [v.text for v in soup.find_all('p') if len(v.text) > 0]
        words_to_bans = ['<', 'javascript']
        for word_to_ban in words_to_bans:
            c_list = list(filter(lambda x: word_to_ban not in x.lower(), c_list))
        c_list = [t for t in c_list if
                  len(re.findall('[a-z]', t.lower())) / (
                      len(t) + 1) < data.LINKS_POST_PROCESSING_CLEAN_HTML_RATIO_LETTERS_LENGTH]
        content = ' '.join(c_list)
        content = content.replace('\n', ' ')
        content = re.sub('\s\s+', ' ', content)  # remove multiple spaces.
    return content


def collect_content(parent_tag):
    """Collects all text from children p tags of parent_tag"""
    content = ''
    for tag in parent_tag:
        p_tags = tag.find_all('p')
        for tag in p_tags:
            content += tag.text + '\n'
    return content


def get_title(soup):
    """Retrieves Title of Article. Use Google truncated title trick instead."""
    # Heuristics
    div_tags = soup.find_all('div', class_='Title')
    article_headline_tags = soup.find_all('h1', class_='article-headline')
    headline_tags = soup.find_all('h2', id='main_title')
    hl = soup.find_all(class_='Title')
    all_h1_tags = soup.find_all('h1')
    title_match = soup.find_all(class_=re.compile('title'))
    Title_match = soup.find_all(class_=re.compile('Title'))
    headline_match = soup.find_all(class_=re.compile('headline'))

    item_prop_hl = soup.find_all(itemprop='headline')
    if item_prop_hl:
        return item_prop_hl[0].text

    if div_tags:
        for tag in div_tags:
            h1Tag = tag.find_all('h1')
            for tag in h1Tag:
                if tag.text:
                    return tag.text

    elif article_headline_tags:
        for tag in article_headline_tags:
            return tag.text
    elif headline_tags:
        for tag in headline_tags:
            return tag.text
    elif headline_match:
        return headline_match[0].text
    elif all_h1_tags:
        return all_h1_tags[0].text
    elif hl:
        return hl[0].text
    else:
        if title_match:
            return title_match[0].text
        elif Title_match:
            return Title_match[0].text
        else:
            return ""
