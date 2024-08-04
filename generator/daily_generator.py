import re
import datetime

from generator.generator import Generator
from common import DATETIME_CET_FORMAT, flag_emojis, DOWN_ARROW_EMOJI

class DailyGenerator(Generator):
    def __init__(self, formatter, shorten_urls=False):
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
        watch_link_string = ""
        try:
            watch_links = event['watchLinks']
            # including only links that can be watched live
            for watch_link in list(filter(lambda wl: 'live' in wl and wl['live'], watch_links)):
                if watch_link_string != "":
                    watch_link_string += " OR "
                if "link" in watch_link:
                    watch_link_string += get_watch_link_string(watch_link, event['country'])
            watch_link_string += "."
        except KeyError:
            pass
        if watch_link_string == "":    
            watch_link_string = "(no watch link found)"
        if event['country'] not in flag_emojis:
            output.append("WARNING: no emoji found for country " + country)
            country = event['country'].upper()
        else:
            country = flag_emojis[event['country']] + " " + event['country'].upper()
        return post + GENERIC_EVENT_STRING.format(country, event['name'], event['stage'], time, watch_link_string)


    def generate_single_post(self, events):
        raise NotImplementedError