#  -*- coding: utf-8 -*-

import pyezxl

# 선택한 영역에서 각셀마다 왼쪽에서 N번째까지의글자삭제하기
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

input_no = excel.read_messagebox_value("Please Input Number : ")

for x in range(x1, x2 + 1):
	for y in range(y1, y2 + 1):
		cell_value = str(excel.read_cell_value(sheet_name, [x, y]))

		try:
			excel.write_cell_value(sheet_name, [x, y], cell_value[int(input_no):])
		except:
			pass