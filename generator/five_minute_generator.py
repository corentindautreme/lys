import re
import datetime

from generator.generator import Generator
from common import DATETIME_CET_FORMAT, flag_emojis, ALERT_EMOJI, DOWN_ARROW_EMOJI

class FiveMinuteGenerator(Generator):
    def __init__(self, formatter=None, shorten_urls=False, post_char_limit=275):
        super().__init__(formatter, shorten_urls=shorten_urls)
        self.post_char_limit = post_char_limit


    def has_header(self, events):
        return False


    def generate_header(self, events, is_morning):
        raise NotImplementedError


    def generate_single_post(self, events, is_morning):
        raise NotImplementedError


    def generate_post(self, event, is_morning):
        # five-minute reminder threads work differently (a post can include multiple events)
        # we must override the thread generation process
        raise NotImplementedError


    def is_single_post(self, events):
        return False


    def generate_event_string(self, event):
        flag = (flag_emojis[event['country']] + " ") if event['country'] in flag_emojis else ""
        watch_link_string = self.get_live_watch_links_string(event, include_comments=False)
        if watch_link_string == "":    
            watch_link_string = "(no watch link found)"
        else:
            watch_link_string = "(" + watch_link_string + ")"
        event_string = "\n{}{} - {} {}".format(flag, event['name'], event['stage'], watch_link_string)
        return event_string


    def generate_thread(self, events, is_morning=False):
        post_header = ALERT_EMOJI + " 5 MINUTES REMINDER!"
        thread = []
        is_thread=False
        tmp_post = ""
        post_events = []
        for idx, event in enumerate(events):
            event_string = self.generate_event_string(event)
            # leaving room for the header
            if len(tmp_post + event_string) < self.post_char_limit:
                # add the event string to the current post
                tmp_post += "\n---------" + event_string
                # flag the event as part of the current post
                post_events.append(event)
            else:
                # we're ready to save the first post
                # add the header
                post = post_header
                # if we're here, we're about to create/continue a thread, because the next event doesn't fit in the current post
                if not is_thread:
                    # if we haven't started a thread yet, this means this is the first post of the thread
                    post += " (thread " + DOWN_ARROW_EMOJI + ")"
                else:
                    # otherwise, we're just adding another post to the thread
                    post += " (cont.)"
                is_thread = True
                # the post is complete, we save it and save the events that are part of it
                post += tmp_post
                if self.formatter is not None:
                    post = self.formatter.format_post(post, post_events)
                thread.append(post)
                # we reset the tmp post, and initialize it with the next event (the one we couldn't add to the previous post)
                tmp_post = "\n---------" + event_string
                post_events = [event]
        # if we processed all events but still have event strings that we haven't saved to a post, we do it now
        if len(tmp_post) > 0:
            post = post_header
            if is_thread:
                post += " (cont.)"
            post += tmp_post
            if self.formatter is not None:
                post = self.formatter.format_post(post, post_events)
            thread.append(post)

        return thread