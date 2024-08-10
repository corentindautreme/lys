import re

from abc import ABC, abstractmethod
from common import CASSETTE_EMOJI, TROPHY_EMOJI, CLOCK_EMOJI, TV_EMOJI
from utils.watch_link_utils import get_short_url

class Generator(ABC):
    GENERIC_EVENT_STRING = "{}\n---------\n" + CASSETTE_EMOJI + " {}\n" + TROPHY_EMOJI + " {}\n" + CLOCK_EMOJI + " {} CET\n---------\n" + TV_EMOJI + " {}"

    def __init__(self, formatter=None, shorten_urls=False):
        self.formatter = formatter
        self.shorten_urls = shorten_urls


    def get_watch_link_string(self, watch_link, country):
        has_comment = False
        watch_link_string = get_short_url(watch_link['link']) if self.shorten_urls else watch_link['link']
        if "comment" in watch_link and watch_link['comment'] != "" and watch_link['comment'] != "Recommended link":
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


    def generate_thread(self, events, is_morning):
        if self.is_single_post(events):
            return [self.generate_single_post(events, is_morning)]

        events = sorted(events, key=lambda e: (e['dateTimeCet'], e['country']))

        thread = []
        if self.has_header(events):
            header = self.generate_header(events, is_morning)
            if self.formatter is not None:
                header = self.formatter.format_post(header, None)
            thread.append(header)

        for event in events:
            post = self.generate_post(event, is_morning)
            if self.formatter is not None:
                post = self.formatter.format_post(post, event)
            thread.append(post)

        return thread
