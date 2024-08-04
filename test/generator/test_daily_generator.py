import unittest

from generator.daily_generator import DailyGenerator

class DailyGeneratorTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator = DailyGenerator(formatter=None)


    def test_when_zero_or_one_event_in_list_should_not_generate_header(self):
        events = []
        self.assertEqual(self.generator.has_header(events), False)
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        self.assertEqual(self.generator.has_header(events), False)


    def test_when_more_than_one_event_in_list_should_generate_header(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        self.assertEqual(self.generator.has_header(events), True)


    def test_when_more_than_one_event_in_list_should_generate_header(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        self.assertEqual(self.generator.has_header(events), True)
        header = self.generator.generate_header(events, is_morning=False)
        self.assertEqual(header, "TONIGHT | 2 selection shows across Europe! (thread \U00002B07\U0000FE0F)")


    def test_when_multiple_events_and_1_Australian_event_then_should_mention_Australia_in_header(self):
        events = [
            {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
        self.assertEqual(self.generator.has_header(events), True)
        header = self.generator.generate_header(events, is_morning=True)
        self.assertEqual(header, "TODAY | 3 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")


    def test_when_events_include_multi_parter_then_should_count_the_multi_parter_as_only_one_event_in_header(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        self.assertEqual(self.generator.has_header(events), True)
        header = self.generator.generate_header(events, is_morning=True)
        self.assertEqual(header, "TODAY | 2 selection shows across Europe! (thread \U00002B07\U0000FE0F)")


    def test_when_events_only_contains_a_multi_parter_show_then_should_count_the_multi_parter_show_as_only_one_event_in_the_header(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        self.assertEqual(self.generator.has_header(events), True)
        header = self.generator.generate_header(events, is_morning=False)
        self.assertEqual(header, "TONIGHT | 1 selection show across Europe! (thread \U00002B07\U0000FE0F)")


    def test_generate_single_post_should_raise_error(self):
        e = None
        try:
            self.generator.generate_single_post([])
        except NotImplementedError as err:
            e = err
        self.assertIsNotNone(e)
        self.assertIsInstance(e, NotImplementedError)
