import requests
import os
import datetime

from bs4 import BeautifulSoup
from common import get_short_url


def get_session():
    BLUESKY_ACCOUNT_HANDLE=os.environ['BLUESKY_ACCOUNT_HANDLE']
    BLUESKY_ACCOUNT_APP_PASSWORD=os.environ['BLUESKY_ACCOUNT_APP_PASSWORD']

    # json with accessJwt and refreshJwt
    response = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_ACCOUNT_HANDLE, "password": BLUESKY_ACCOUNT_APP_PASSWORD},
    )
    response.raise_for_status()
    return response.json()


def get_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def parse_url_links(post_body, link_descriptions):
    spans = []
    last_appearance_of = {}
    for ld in link_descriptions:
        previous_appearance = (last_appearance_of.get(ld['text']) + 1) if ld['text'] in last_appearance_of else 0
        start = post_body.find(ld['text'], previous_appearance)
        # keep track of the last appearance of a link text to handle posts where a short link appears multiple times
        last_appearance_of[ld['text']] = start
        # we have to "count in utf-8" to make sure emojis are counted for the right amount of characters
        start = len(post_body[:start].encode("utf-8"))
        end = start + len(ld['text'].encode("utf-8"))
        spans.append({
            "start": start,
            "end": end,
            "url": ld['url'],
        })
    return spans


# stolen from https://atproto.com/blog/create-post
def get_facets(link_spans, menion_spans=[]):
    facets = []
    for m in menion_spans:
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


def get_facets_for_event_links_in_string(events, string, live_links_only=True):
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

    spans = parse_url_links(string, link_descriptions)
    facets = get_facets(spans)
    return facets


def generate_url_card(url):
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


def generate_post(post_string, facets=[], include_card=False, url_for_card=None):
    post = {
        "$type": "app.bsky.feed.post",
        "text": post_string,
        "facets": facets,
        "createdAt": get_timestamp(),
        "langs": ["en-US"]
    }

    if include_card:
        # generate social card for the recommended link
        post["embed"] = generate_url_card(url_for_card)

    return post


def publish_post(session, post):
    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": "Bearer " + session["accessJwt"]},
        json={
            "repo": session["did"],
            "collection": "app.bsky.feed.post",
            "record": post
        }
    )
    resp.raise_for_status()
    return resp.json()
