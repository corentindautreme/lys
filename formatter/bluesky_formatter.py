import requests

from bs4 import BeautifulSoup

from formatter.formatter import Formatter
from utils.watch_link_utils import get_first_watch_link, get_short_url
from utils.time_utils import get_timestamp

class BlueskyFormatter(Formatter):
    def __init__(self, include_link_card=False):
        self.include_link_card = include_link_card


    def parse_url_links(self, post_string, link_descriptions):
        spans = []
        last_appearance_of = {}
        for ld in link_descriptions:
            previous_appearance = (last_appearance_of.get(ld['text']) + 1) if ld['text'] in last_appearance_of else 0
            start = post_string.find(ld['text'], previous_appearance)
            # keep track of the last appearance of a link text to handle posts where a short link appears multiple times
            last_appearance_of[ld['text']] = start
            # we have to "count in utf-8" to make sure emojis are counted for the right amount of characters
            start = len(post_string[:start].encode("utf-8"))
            end = start + len(ld['text'].encode("utf-8"))
            spans.append({
                "start": start,
                "end": end,
                "url": ld['url'],
            })
        return spans


    # stolen from https://atproto.com/blog/create-post
    def get_facets(self, link_spans, mention_spans=[]):
        facets = []
        for m in mention_spans:
            resp = requests.get(
                "https://bsky.social/xrpc/com.atproto.identity.resolveHandle",
                params={"handle": m["handle"]},
            )
            # If the handle can't be resolved, just skip it!
            # It will be rendered as text in the post instead of a link
            if resp.status_code == 400:
                continue
            did = resp.json()["did"]
            facets.append({
                "index": {
                    "byteStart": m["start"],
                    "byteEnd": m["end"],
                },
                "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}],
            })
        for u in link_spans:
            facets.append({
                "index": {
                    "byteStart": u["start"],
                    "byteEnd": u["end"],
                },
                "features": [
                    {
                        "$type": "app.bsky.richtext.facet#link",
                        "uri": u["url"],
                    }
                ],
            })
        return facets


    def get_facets_for_event_links_in_string(self, events, post_string, live_links_only=True):
        link_descriptions = []

        for event in events:
            # extract links to insert in the post alongside their associated string
            for link in event['watchLinks']:
                if live_links_only and ('live' not in link or not link['live']):
                    continue
                link_string = get_short_url(link['link'])
                link_descriptions.append({'text': link_string, 'url': link['link']})
                if 'accountRequired' in link and link['accountRequired']:
                    account_help_link = "https://lyseurovision.github.io/help.html#account-" + event['country']
                    link_descriptions.append({'text': get_short_url(account_help_link), 'url': account_help_link})

        spans = self.parse_url_links(post_string, link_descriptions)
        facets = self.get_facets(link_spans=spans)
        return facets


    def generate_url_card(self, url):
        # the required fields for every embed card
        card = {
            "uri": url,
            "title": "",
            "description": "",
        }

        # fetch the HTML
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # parse out the "og:title" and "og:description" HTML meta tags
        title_tag = soup.find("meta", property="og:title")
        if title_tag:
            card["title"] = title_tag["content"]
        description_tag = soup.find("meta", property="og:description")
        if description_tag:
            card["description"] = description_tag["content"]

        return {
            "$type": "app.bsky.embed.external",
            "external": card,
        }


    def format_post(self, post_string, events):
        if events is None or len(events) <= 1:
            event = None if events is None or len(events) == 0 else events[0]
            return self.format_single_event_post(post_string, event)
        else:
            return self.format_multi_event_post(post_string, events)


    def format_multi_event_post(self, post_string, events):
        post = {
            "$type": "app.bsky.feed.post",
            "text": post_string,
            "createdAt": get_timestamp(),
            "langs": ["en-US"]
        }
        post["facets"] = self.get_facets_for_event_links_in_string(events, post_string)
        
        # include a social card to the post only if we have at least one (live) recommended link to provide
        # and, of course, if we want to include a card
        if self.include_link_card:
            first_link = get_first_watch_link(events[0])
            if first_link is not None:
                post["embed"] = self.generate_url_card(first_link)

        return post


    def format_single_event_post(self, post_string, event):
        post = {
            "$type": "app.bsky.feed.post",
            "text": post_string,
            "createdAt": get_timestamp(),
            "langs": ["en-US"]
        }

        first_link = None

        if event is not None:
            first_link = get_first_watch_link(event)
            post["facets"] = self.get_facets_for_event_links_in_string([event], post_string)

        # include a social card to the post only if we have at least one (live) recommended link to provide
        # and, of course, if we want to include a card
        if self.include_link_card and first_link is not None:
            post["embed"] = self.generate_url_card(first_link)

        return post


