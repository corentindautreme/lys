import re

def get_short_url(url):
    link_text = re.sub(
        r'https?:\/\/(www\.)?',
        '',
        url
    )
    idx_slash = link_text.find("/")
    if idx_slash > -1:
        link_text = link_text[:idx_slash]
    return link_text


def get_first_watch_link(event, live=True):
    links = event['watchLinks']
    if live:
        links = list(filter(lambda l: l['live'], links))
    if len(links) == 0:
        return None
    return links[0]['link']