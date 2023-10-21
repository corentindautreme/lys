import unittest

from lys_weekly import generate_weekly_post

class WeeklyPostGenerationTest(unittest.TestCase):
    def test_when_one_event_then_post_should_only_contain_this_one_event(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Andra Chansen', 'dateTimeCet': '2021-03-06T20:00:00', 'watchLink': 'https://svtplay.se'}]
        (post, output) = generate_weekly_post(events)
        self.assertEqual(post, "\U0001F5D3 COMING UP NEXT WEEK:\n\n - Saturday 06: \U0001F1F8\U0001F1EA")

    def test_when_multiple_events_then_post_should_contain_them_all(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLink': 'https://err.tv'},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 4', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        (post, output) = generate_weekly_post(events)
        self.assertEqual(post, "\U0001F5D3 COMING UP NEXT WEEK:\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: \U0001F1F3\U0001F1F4\U0001F1F8\U0001F1EA")


    def test_when_events_include_a_final_then_post_should_contain_final_indicators(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLink': 'https://err.tv'},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        (post, output) = generate_weekly_post(events)
        self.assertEqual(post, "\U0001F5D3 COMING UP NEXT WEEK (* = final):\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: \U0001F1F3\U0001F1F4*\U0001F1F8\U0001F1EA")


    def test_when_events_include_country_without_known_flag_should_replace_by_country_name(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLink': 'https://err.tv'},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'FYR Macedonia', 'name': 'What is the Macedonian for "Song" again?', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://google.it.mate'}
        ]
        (post, output) = generate_weekly_post(events)
        self.assertEqual(post, "\U0001F5D3 COMING UP NEXT WEEK (* = final):\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: (FYR Macedonia*)\U0001F1F8\U0001F1EA")

    def test_when_events_include_multiple_events_for_one_country_the_country_should_only_appear_once_in_the_post(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://nrk.no/mgp'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final (part 2)', 'dateTimeCet': '2021-02-06T21:20:00', 'watchLink': 'https://nrk.no/mgp'},
        ]
        (post, output) = generate_weekly_post(events)
        self.assertEqual(post, "\U0001F5D3 COMING UP NEXT WEEK (* = final):\n\n - Saturday 06: \U0001F1F3\U0001F1F4*\U0001F1F8\U0001F1EA")
