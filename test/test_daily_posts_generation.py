import unittest

from lys_daily import generate_thread, post_to_target

class DailyPostsGenerationTest(unittest.TestCase):
    def test_when_generating_posts_for_none_target_should_raise_value_error(self):
        e = None
        try:
            generate_thread(events=[], is_morning=False, target=None)
        except ValueError as err:
            e = err
        self.assertIsNotNone(e)
        self.assertEqual(str(e), "Unknown target 'None'")


    def test_when_generating_posts_for_unknown_target_should_raise_value_error(self):
        e = None
        try:
            generate_thread(events=[], is_morning=False, target="facebook")
        except ValueError as err:
            e = err
        self.assertIsNotNone(e)
        self.assertEqual(str(e), "Unknown target 'facebook'")

    def test_when_posting_to_none_target_should_raise_value_error(self):
        e = None
        try:
            post_to_target(posts=[], target=None)
        except ValueError as err:
            e = err
        self.assertIsNotNone(e)
        self.assertEqual(str(e), "Unknown target 'None'")

    def test_when_posting_to_unknown_target_should_raise_value_error(self):
        e = None
        try:
            post_to_target(posts=[], target='instagram')
        except ValueError as err:
            e = err
        self.assertIsNotNone(e)
        self.assertEqual(str(e), "Unknown target 'instagram'")

