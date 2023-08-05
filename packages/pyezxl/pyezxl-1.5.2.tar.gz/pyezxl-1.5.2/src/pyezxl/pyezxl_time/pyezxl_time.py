# -*- coding: utf-8 -*-

import time
import string

class pyezxl_time:
	def __init__(self):
		self.web_site = "www.halmoney.com"

	def read_time_day(self, time_char=""):
		# 일 -----> ['05', '095']
		if time_char == "":
			time_char = time.localtime(time.time())
		return [time.strftime('%d', time_char), time.strftime('%j', time_char)]

	def read_time_hour(self, time_char=""):
		# 시 -----> ['10', '22', 'PM']
		if time_char == "":
			time_char = time.localtime(time.time())
		return [time.strftime('%I', time_char), time.strftime('%H', time_char), time.strftime('%P', time_char)]

	def read_time_minute(self, time_char=""):
		# 분 -----> ['07']
		if time_char == "":
			time_char = time.localtime(time.time())
		return [time.strftime('%M', time_char)]

	def read_time_month(self, time_char=""):
		# 월 -----> ['04', 'Apr', 'April']
		if time_char == "":
			time_char = time.localtime(time.time())
		return [time.strftime('%m', time_char), time.strftime('%b', time_char), time.strftime('%B', time_char)]

	def read_time_second(self, time_char=""):
		# 초 -----> ['48']
		if time_char == "":
			time_char = time.localtime(time.time())
		return [time.strftime('%S', time_char)]

	def read_time_today(self, time_char=""):
		# 종합 -----> ['2002-04-05', '04/05/02', '22:07:48', '04/05/02 22:07:48']
		if time_char == "":
			time_char = time.localtime(time.time())
		total_dash = time.strftime('%Y', time_char) + "-" + time.strftime('%m', time_char) + "-" + time.strftime('%d', time_char)
		return [total_dash, time.strftime('%Y', time_char), time.strftime('%m', time_char), time.strftime('%d', time_char)]

	def read_time_now(self, time_char=""):
		if time_char == "":
			time_char = time.localtime(time.time())
		# 종합 -----> ['04/05/02', '22:07:48', '04/05/02 22:07:48','2002-04-05']
		now_dash = time.strftime('%H', time_char) + ":" + time.strftime('%M', time_char) + ":" + time.strftime('%S', time_char)
		return [now_dash, time.strftime('%H', time_char), time.strftime('%M', time_char), time.strftime('%S', time_char)]

	def read_time_week(self, time_char=""):
		if time_char == "":
			time_char = time.localtime(time.time())
		# 주 -----> ['5', '13', 'Fri', 'Friday']
		return [time.strftime('%w', time_char), time.strftime('%W', time_char), time.strftime('%a', time_char), time.strftime('%A', time_char)]

	def read_time_year(self, time_char=""):
		if time_char == "":
			time_char = time.localtime(time.time())
		# 년 -----> ['02', '2002']
		return [time.strftime('%y', time_char), time.strftime('%Y', time_char)]

	def change_time_sec(self, input_data=""):
		# input_data = "14:06:23"
		re_compile = re.compile("\d+")
		result = re_compile.findall(input_data)
		total_sec = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
		return total_sec

	def change_sec_time(self, input_data=""):
		# input_data = 123456
		step_1 = divmod(int(input_data), 60)
		step_2 = divmod(step_1[0], 60)
		final_result = [step_2[0], step_2[1], step_1[1]]
		return final_result
