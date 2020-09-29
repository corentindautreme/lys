import unittest

from lys_weekly import generate_weekly_tweet_body

class WeeklyTweetGenerationTest(unittest.TestCase):
    def test_when_one_event_then_tweet_should_only_contain_this_one_event(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Andra Chansen', 'dateTimeCet': '2021-03-06T20:00:00', 'watchLink': 'https://svtplay.se'}]
        (tweet, output) = generate_weekly_tweet_body(events)
        self.assertTrue(tweet == "\U0001F5D3 COMING UP NEXT WEEK:\n\n - Saturday 06: \U0001F1F8\U0001F1EA")

    def test_when_multiple_events_then_tweet_should_contain_them_all_event(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLink': 'https://err.tv'},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 4', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        (tweet, output) = generate_weekly_tweet_body(events)
        self.assertTrue(tweet == "\U0001F5D3 COMING UP NEXT WEEK:\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: \U0001F1F8\U0001F1EA\U0001F1F3\U0001F1F4")


    def test_when_events_include_a_final_then_tweet_should_contain_final_indicators(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLink': 'https://err.tv'},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        (tweet, output) = generate_weekly_tweet_body(events)
        self.assertTrue(tweet == "\U0001F5D3 COMING UP NEXT WEEK (* = final):\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: \U0001F1F8\U0001F1EA\U0001F1F3\U0001F1F4*")


    def test_when_events_include_country_without_known_flag_should_replace_by_country_name(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLink': 'https://err.tv'},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'FYR Macedonia', 'name': 'What is the Macedonian for "Song" again?', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://google.it.mate'}
        ]
        (tweet, output) = generate_weekly_tweet_body(events)
        self.assertTrue(tweet == "\U0001F5D3 COMING UP NEXT WEEK (* = final):\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: \U0001F1F8\U0001F1EA(FYR Macedonia*)")