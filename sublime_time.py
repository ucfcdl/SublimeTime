import sublime, sublime_plugin
import datetime
import time

class UnixTimeToDateStrCommand(sublime_plugin.TextCommand):
	regex = '[0-9]{9,10}'

	def run(self, edit):
		region = self.view.find(UnixTimeToDateStrCommand.regex, 0)
		while(region is not None):
			unix_time_str = self.view.substr(region)
			time_str = datetime.datetime.fromtimestamp(int(unix_time_str)).strftime('%Y-%m-%d %I:%M:%S %p')
			self.view.replace(edit, region, time_str)
			region = self.view.find(UnixTimeToDateStrCommand.regex, 0)

class DateStrToUnixTimeCommand(sublime_plugin.TextCommand):
	regex = '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} (A|P|a|p)(M|m)'

	def run(self, edit):
		#2013-01-24 02:28:42 PM
		region = self.view.find(DateStrToUnixTimeCommand.regex, 0)
		while(region is not None):
			time_str = self.view.substr(region)
			unix_time_str = str(int(time.mktime(datetime.datetime.strptime(time_str, '%Y-%m-%d %I:%M:%S %p').timetuple())))
			self.view.replace(edit, region, unix_time_str)
			region = self.view.find(DateStrToUnixTimeCommand.regex, 0)
