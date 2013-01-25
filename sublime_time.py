import sublime
import sublime_plugin
import datetime
import time
import re

st_settings = sublime.load_settings('sublime_time.sublime-settings')

# given a starting point, the regex to find and the text to search (haystack),
# return a list of regions
def find(needle_start, needle_regex, haystack):
	matches = []
	for match in needle_regex.finditer(haystack):
		region = sublime.Region(needle_start + match.start(), needle_start + match.start() + len(match.group()))
		matches.insert(0, region)

	return matches


class UnixTimeToDateStrCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regex = re.compile(st_settings.get('unix_timestamp_regex'))
		user_selections = [s for s in self.view.sel() if not s.empty()]

		# Filter whole document if there's no non-empty selection
		if len(user_selections) == 0:
			user_selections = [sublime.Region(0, self.view.size())]

		for user_selection in reversed(user_selections):
			matches = find(user_selection.begin(), regex, self.view.substr(user_selection))
			if matches != None:
				for matched_region in matches:
					unix_time_str = self.view.substr(matched_region)
					time_str = datetime.datetime.fromtimestamp(int(unix_time_str)).strftime(st_settings.get('date_string_format'))
					self.view.replace(edit, matched_region, time_str)


class DateStrToUnixTimeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regex = re.compile(st_settings.get('date_string_regex'))
		user_selections = [s for s in self.view.sel() if not s.empty()]

		# Filter whole document if there's no non-empty selection
		if len(user_selections) == 0:
			user_selections = [sublime.Region(0, self.view.size())]

		for user_selection in reversed(user_selections):
			matches = find(user_selection.begin(), regex, self.view.substr(user_selection))
			if matches != None:
				for matched_region in matches:
					time_str = self.view.substr(matched_region)
					unix_time_str = str(int(time.mktime(datetime.datetime.strptime(time_str, st_settings.get('date_string_format')).timetuple())))
					self.view.replace(edit, matched_region, unix_time_str)