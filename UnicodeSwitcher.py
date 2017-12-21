# coding: utf-8

'''Provides a function to switch unicode normalization formats.
'''

from unicodedata import normalize

import sublime
import sublime_plugin


FORMS = (
    ['NFC', 'Composed format.'],
    ['NFD', 'Decomposed format.'],
)


class UnicodeSwitcherSelectCommand(sublime_plugin.TextCommand):
    '''Shows a list of unicode encoding forms and applies one of them.
    '''

    def run(self, edit):
        self.view.window().show_quick_panel(FORMS, self.replace_all)

    def replace_all(self, form_index):
        if form_index < 0:
            return

        self.view.run_command('unicode_switcher_switch', {
            'form': FORMS[form_index][0],
        })


class UnicodeSwitcherSwitchCommand(sublime_plugin.TextCommand):
    '''Applies the specified unicode encoding form to the current view.
    '''

    def run(self, edit, form=FORMS[0][0]):
        regions_sorted = self._get_sorted_regions(reverse=True)

        try:
            replacements = self._prepare_replacements(form, regions_sorted)
        except UnicodeDecodeError as e:
            sublime.error_message('Unicode decode failed. '
                                  'Please check the encoding of the file.')
            return

        self._replace_regions(edit, replacements)
        message = ('The Unicode form has been changed to "{}" successfully.'
                   .format(form))
        sublime.status_message(message)

    def _get_sorted_regions(self, reverse=False):
        selection = self.view.sel()

        if len(selection) == 0:
            is_empty = True
        elif len(selection) == 1 and selection[0].empty():
            is_empty = True
        else:
            is_empty = False

        if is_empty:
            return [sublime.Region(0, self.view.size())]
        else:
            return sorted(selection, key=lambda s: s.begin(), reverse=reverse)

    def _prepare_replacements(self, form, regions):
        return ((r, normalize(form, self.view.substr(r))) for r in regions)

    def _replace_regions(self, edit, replacements):
        for region, string in replacements:
            self.view.replace(edit, region, string)
