import datetime

from generator.generator import Generator
from utils.time_utils import extract_weekday_and_day_from_timestamp_string
from utils.post_utils import flag_emojis

class WeeklyGenerator(Generator):
    def __init__(self, formatter=None):
        super().__init__(formatter)


    def has_header(self, events):
        return False


    def generate_header(self, events, is_morning):
        raise NotImplementedError


    def generate_post(self, event, is_morning):
        raise NotImplementedError


    def is_single_post(self, events):
        return True


    def generate_single_post(self, events, is_morning):
        # list of (weekday, country) tuples
        simplified_events = list(map(lambda e: (extract_weekday_and_day_from_timestamp_string(e['dateTimeCet']), e['country'] + ('*' if "Final" in e['stage'] else '')), events))
        # indicates if any event is a final
        includes_final = False

        # weekday -> [country] map
        calendar = {}
        for event in simplified_events:
            day = event[0]
            country = event[1]
            if '*' in country:
                includes_final = True
            if day not in calendar:
                calendar[day] = set()
            calendar[day].add(country)

        # building and posting the tweet
        post = "\U0001F5D3 COMING UP NEXT WEEK" + (" (* = final)" if includes_final else "") + ":\n"
        for weekday in calendar.keys():
            # building flag emojis list
            flags = ""
            for c in sorted(list(calendar[weekday])):
                final = '*' in c
                country = c.replace('*', '')
                if country not in flag_emojis:
                    flags += "(" + c + ")"
                else:
                    flags += flag_emojis[country] + ('*' if final else '')
            post += "\n - {}: {}".format(weekday, flags)
            
        return post