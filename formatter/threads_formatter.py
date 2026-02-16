import re

from formatter.formatter import Formatter

class ThreadsFormatter(Formatter):
    def __init__(self, include_link_card=False):
        self.include_link_card = include_link_card


    @staticmethod
    def replace_anchor_in_links(match):
        link = match.group(0) # The full matched URL
        modified_link = link.replace('#', '%23')
        return modified_link


    def format_post(self, post_string, events=None):
        url_regex = r'https?://[^\s]+'
        return re.sub(url_regex, ThreadsFormatter.replace_anchor_in_links, post_string)