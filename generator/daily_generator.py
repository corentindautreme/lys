import re
import datetime

from generator.generator import Generator
from utils.time_utils import DATETIME_CET_FORMAT
from common import flag_emojis, DOWN_ARROW_EMOJI

class DailyGenerator(Generator):
    def __init__(self, formatter=None, shorten_urls=False):
        super().__init__(formatter, shorten_urls=shorten_urls)


    def has_header(self, events):
        return len(events) > 1


    def generate_header(self, events, is_morning):
        header = ""

        if is_morning:
            header = "TODAY | "
        else:
            header = "TONIGHT | "

        multi_parter_regex = re.compile(r".*\(part [0-9]+\)")
        event_count = len(list(filter(lambda e: re.match(multi_parter_regex, e['stage']) is None, events)))
        header = (header + str(event_count) + " selection show{} across Europe{}! (thread " + DOWN_ARROW_EMOJI + ")").format(
            "s" if event_count > 1 else "",
            " and Australia" if any("Australia" == e['country'] for e in events) else ""
        )
        return header


    def generate_post(self, event, is_morning):
        time = datetime.datetime.strptime(event['dateTimeCet'], DATETIME_CET_FORMAT).strftime("%H:%M")
        watch_link_string = self.get_live_watch_links_string(event)
        if watch_link_string == "":    
            watch_link_string = "(no watch link found)"
        else:
            watch_link_string += "."
        if event['country'] not in flag_emojis:
            output.append("WARNING: no emoji found for country " + country)
            country = event['country'].upper()
        else:
            country = flag_emojis[event['country']] + " " + event['country'].upper()
        
        post = ""

        if is_morning:
            post = "TODAY | "
        else:
            post = "TONIGHT | "

        return post + self.GENERIC_EVENT_STRING.format(country, event['name'], event['stage'], time, watch_link_string)


    def is_single_post(self, events):
        return len(events) == 1


    def generate_single_post(self, events, is_morning):
        return self.generate_post(events[0], is_morning)