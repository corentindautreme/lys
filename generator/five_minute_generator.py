import re
import datetime

from generator.generator import Generator
from utils.post_utils import flag_emojis, ALERT_EMOJI, DOWN_ARROW_EMOJI

class FiveMinuteGenerator(Generator):
    POST_HEADER = ALERT_EMOJI + " 5 MINUTES REMINDER!"
    SEPARATOR = "\n---------"

    def __init__(self, formatter=None, shorten_urls=False, post_char_limit=260, thread_indicator=False):
        super().__init__(formatter, shorten_urls=shorten_urls)
        self.post_char_limit = post_char_limit
        # include indicator that the post is part of a thread at the beginning of each post
        self.thread_indicator = thread_indicator


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


    def is_post_too_long(self, event_string):
        return len((self.POST_HEADER + self.SEPARATOR + event_string).encode("utf-8")) > self.post_char_limit


    def generate_event_string(self, event, include_comments=True, include_link_count=None):
        flag = (flag_emojis[event['country']] + " ") if event['country'] in flag_emojis else ""
        watch_link_string = self.get_live_watch_links_string(event, include_comments=include_comments, include_link_count=include_link_count)
        if watch_link_string == "" and include_link_count is None:    
            watch_link_string = "(no watch link found)"
        elif watch_link_string != "":
            watch_link_string = "(" + watch_link_string + ")"
        event_string = "\n{}{} - {} {}".format(flag, event['name'], event['stage'], watch_link_string)
        return event_string


    def generate_shorter_event_string(self, event):
        # we start by removing the comments
        event_string = self.generate_event_string(event, include_comments=False)
        link_count = len(event['watchLinks'])
        # if that's not enough, we remove watch links one by one, starting by the last ones
        while self.is_post_too_long(event_string) and link_count >= 0:
            link_count -= 1
            event_string = self.generate_event_string(event, include_comments=False, include_link_count=link_count)
        return event_string


    def generate_thread(self, events, is_morning=False):
        thread = []
        is_thread = False
        tmp_post = ""
        post_events = []

        for idx, event in enumerate(events):
            event_string = self.generate_event_string(event)
            # if the string for a single event is already too long to be posted on its own, we
            # need to shorten it
            if self.is_post_too_long(event_string):
                event_string = self.generate_shorter_event_string(event)
            # leaving room for the header
            if len(self.POST_HEADER + self.SEPARATOR + tmp_post + event_string) < self.post_char_limit:
                # add the event string to the current post
                tmp_post += self.SEPARATOR + event_string
                # flag the event as part of the current post
                post_events.append(event)            
            else:
                # we're ready to save the first post
                # add the header
                post = self.POST_HEADER
                # if we're here, we're about to create/continue a thread, because the next event doesn't fit in the current post
                if self.thread_indicator:
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
                tmp_post = self.SEPARATOR + event_string
                post_events = [event]
        
        # if we processed all events but still have event strings that we haven't saved to a post, we do it now
        if len(tmp_post) > 0:
            post = self.POST_HEADER
            if is_thread and self.thread_indicator:
                post += " (cont.)"
            post += tmp_post
            if self.formatter is not None:
                post = self.formatter.format_post(post, post_events)
            thread.append(post)

        return thread