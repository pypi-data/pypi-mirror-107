class pyezxl_fun:
	def __init__(self,aa):
		# 사용가능한 색깔을 보다 쉽게 표현하기위해 만들었다
		# 색은 3가지로 구분 : 테이블등을 만들때 사용하면 좋은 색 : ez1~15번까지
		# 12가지의 색을 기본, 약간 옅은 테이블색칠용, 파스텔톤의 3가지로 구분
		# 각 3종류는 7개의 형태로 구분하여 +, -의 형태로 표현을 하도록 하였다
		aa = "www.halmoney.com"
		self.color_nono = {
			"ez1" : 6384127,
			"ez2" : 4699135,
			"ez3" : 9895421,
			"ez4" : 7855479,}

	def fun_trim(self, input_data):
		# 함수중 trim을 사용하는 것이며 엑셀 함수의 사용을 보여주기 위하여 만든 것이다
		aaa = self.xlApp.WorksheetFunction.Trim(input_data)
		return aaa

	def fun_ltrim(self, input_data):
		# 함수중 ltrim을 사용하는 것이며 엑셀 함수의 사용을 보여주기 위하여 만든 것이다
		aaa = self.xlApp.WorksheetFunction.LTrim(input_data)
		return aaa

	def fun_rtrim(self, input_data):
		# 함수중 rtrim을 사용하는 것이며 엑셀 함수의 사용을 보여주기 위하여 만든 것이다
		aaa = self.xlApp.WorksheetFunction.RTrim(input_data)
		return aaa
