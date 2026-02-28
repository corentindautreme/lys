import re
import urllib.parse

from abc import ABC, abstractmethod
from utils.post_utils import CASSETTE_EMOJI, TROPHY_EMOJI, CLOCK_EMOJI, TV_EMOJI
from utils.watch_link_utils import get_short_url

class Generator(ABC):
    GENERIC_EVENT_STRING = "{}\n---------\n" + CASSETTE_EMOJI + " {}\n" + TROPHY_EMOJI + " {}\n" + CLOCK_EMOJI + " {} CET\n---------\n" + TV_EMOJI + " {}"

    def __init__(self, formatter=None, shorten_urls=False):
        self.formatter = formatter
        self.shorten_urls = shorten_urls


    def get_single_watch_link_string(self, watch_link, country, include_comments=True):
        has_comment = False
        watch_link_string = get_short_url(watch_link['link']) if self.shorten_urls else urllib.parse.quote(watch_link['link']).replace("%3A//", "://")
        if include_comments and "comment" in watch_link and watch_link['comment'] != "" and watch_link['comment'] != "Recommended link":
            watch_link_string += " (" + watch_link['comment'] + ")"
            has_comment = True

        additional_comments = []
        if "geoblocked" in watch_link and watch_link['geoblocked']:
            additional_comments.append("geoblocked")
        if "accountRequired" in watch_link and watch_link['accountRequired']:
            account_comment = "account required: see "
            account_help_link = "https://lyseurovision.github.io/help.html#account-" + country
            account_comment += get_short_url(account_help_link) if self.shorten_urls else account_help_link
            additional_comments.append(account_comment)
        if len(additional_comments) > 0:
            if not has_comment:
                watch_link_string += " "
            watch_link_string += "(" + ", ".join(additional_comments) + ")"

        return watch_link_string


    def get_live_watch_links_string(self, event, include_comments=True, include_link_count=None):
        watch_link_string = ""
        try:
            watch_links = event['watchLinks'][:include_link_count]
            # including only links that can be watched live
            for watch_link in list(filter(lambda wl: 'live' in wl and wl['live'], watch_links)):
                if watch_link_string != "":
                    watch_link_string += " OR "
                if "link" in watch_link:
                    watch_link_string += self.get_single_watch_link_string(watch_link, event['country'], include_comments)
        except KeyError:
            return ""
        return watch_link_string


    @abstractmethod
    def has_header(self, events):
        pass


    @abstractmethod
    def generate_header(self, events, is_morning):
        pass


    @abstractmethod
    def generate_post(self, event, is_morning):
        pass


    @abstractmethod
    def is_single_post(self, events):
        pass


    @abstractmethod
    def generate_single_post(self, events, is_morning):
        pass


    def generate_thread(self, events, is_morning=False):
        events = sorted(events, key=lambda e: (e['dateTimeCet'], e['country']))

        if self.is_single_post(events):
            post = self.generate_single_post(events, is_morning)
            if self.formatter is not None:
                post = self.formatter.format_post(post, events)
            return [post]

        thread = []
        if self.has_header(events):
            header = self.generate_header(events, is_morning)
            if self.formatter is not None:
                header = self.formatter.format_post(header, None)
            thread.append(header)

        for event in events:
            post = self.generate_post(event, is_morning)
            if self.formatter is not None:
                post = self.formatter.format_post(post, [event])
            thread.append(post)

        return thread
