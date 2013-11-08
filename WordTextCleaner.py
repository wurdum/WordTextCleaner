import sublime, sublime_plugin
import re


class RemoveBaseCommand(sublime_plugin.TextCommand):
    
    replacements = []
    
    def run(self, edit):
        sels = self.view.sel()
        if self._there_no_selection(sels):
            self._handle_region(edit, sublime.Region(0, self.view.size()))
        else:
            for sel in sels:
                self._handle_region(edit, sel)

    def _there_no_selection(self, regions):
        return len(regions) == 1 and not self.view.substr(regions[0])

    def _handle_region(self, edit, region):
        text = self.view.substr(region)
        for r in self.replacements:
            text = re.sub(r['rx'], r['repl'], text)

        self.view.replace(edit, region, text)


class RemoveSpacesCommand(RemoveBaseCommand):

    replacements = [
        {'rx':re.compile('  +', re.MULTILINE),'repl':' '},
        {'rx':re.compile('^ +', re.MULTILINE),'repl':''},
        {'rx':re.compile(' +$', re.MULTILINE),'repl':''},
    ]


class RemoveListMarkersCommand(RemoveBaseCommand):
    
    replacements = [
        {'rx':re.compile('^(\d{1,3}|\w{1,3})(\.|\))?\s+', re.MULTILINE),'repl':''}
    ]
