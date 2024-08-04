import re

from abc import ABC, abstractmethod
from common import CASSETTE_EMOJI, TROPHY_EMOJI, CLOCK_EMOJI, TV_EMOJI

class Generator(ABC):
    GENERIC_EVENT_STRING = "{}\n---------\n" + CASSETTE_EMOJI + " {}\n" + TROPHY_EMOJI + " {}\n" + CLOCK_EMOJI + " {} CET\n---------\n" + TV_EMOJI + " {}"

    def __init__(self, formatter, single_post=False, shorten_urls=False):
        self.formatter = formatter
        self.single_post = single_post
        self.shorten_urls = shorten_urls


    def get_short_url(self, url):
        link_text = re.sub(
            r'https?:\/\/(www\.)?',
            '',
            url
        )
        idx_slash = link_text.find("/")
        if idx_slash > -1:
            link_text = link_text[:idx_slash]
        return link_text


    def get_watch_link_string(self, watch_link, country):
        has_comment = False
        watch_link_string = get_short_url(watch_link['link']) if shorten_urls else watch_link['link']
        if "comment" in watch_link and watch_link['comment'] != "" and watch_link['comment'] != "Recommended link":
            watch_link_string += " (" + watch_link['comment'] + ")"
            has_comment = True

        additional_comments = []
        if "geoblocked" in watch_link and watch_link['geoblocked']:
            additional_comments.append("geoblocked")
        if "accountRequired" in watch_link and watch_link['accountRequired']:
            account_comment = "account required: see "
            account_help_link = "https://lyseurovision.github.io/help.html#account-" + country
            account_comment += get_short_url(account_help_link) if shorten_urls else account_help_link
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
    def generate_single_post(self, events):
        pass


    def generate_thread(self, events, is_morning):
        if single_post:
            return [generate_single_post(events)]

        thread = []
        if has_header(events):
            thread.push(generate_header(events, is_morning))

        for event in events:
            post = generate_post(event, is_morning)
            post = formatter.format_post(post)
            thread.push(post)


    def publish_thread(self, thread):
        summary = []
        reply_post_id = parent_post_id = ""

        for post in thread:
            summary.append(post)
            try:
                (reply_post_id, parent_post_id) = self.client.publish(post, reply_post_id, parent_post_id)
            except PublishError as e:
                summary.append("Failed to publish " + post + " - " + str(e.errors))

        return summary


    def publish_daily_thread_for_events(self, events, is_morning):
        thread = generator.generate_thread(events, is_morning)
        return publish_thread(thread)
