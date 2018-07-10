# coding: utf-8

"""Tests UnicodeNormalizer functions."""

from unittest import TestCase

import sublime


class TextHandlerMixin:
    """Mixin for handling view text."""

    def get_text(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def set_text(self, string):
        self.view.run_command("insert", {"characters": string})


class TestUnicodeNormalizerSwitchCommand(TextHandlerMixin, TestCase):
    """Tests `UnicodeNormalizerSwitchCommand` command."""

    def setUp(self):
        self.view = sublime.active_window().new_file()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def test_nfd_to_nfc(self):
        original = 'ガギグゲゴ'
        expected = 'ガギグゲゴ'

        self.set_text(original)
        self.view.run_command('unicode_normalizer_switch', {'form': 'NFC'})
        self.assertEqual(self.get_text(), expected)

    def test_nfc_to_nfd(self):
        original = 'ダヂヅデド'
        expected = 'ダヂヅデド'

        self.set_text(original)
        self.view.run_command('unicode_normalizer_switch', {'form': 'NFD'})
        self.assertEqual(self.get_text(), expected)
