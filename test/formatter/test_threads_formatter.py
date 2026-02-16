import unittest

from formatter.threads_formatter import ThreadsFormatter

class ThreadsFormatterTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatter = ThreadsFormatter()

    def test_when_formatting_post_with_url_that_contains_anchor_should_html_encode_symbol(self):
        post = "Watch live! https://svtplay.se/melodifestivalen#2026 (you need an account: https://lyseurovision.github.io/help.html#account-Sweden)"
        formatted_post = self.formatter.format_post(post)
        self.assertEqual(formatted_post, "Watch live! https://svtplay.se/melodifestivalen%232026 (you need an account: https://lyseurovision.github.io/help.html%23account-Sweden)")