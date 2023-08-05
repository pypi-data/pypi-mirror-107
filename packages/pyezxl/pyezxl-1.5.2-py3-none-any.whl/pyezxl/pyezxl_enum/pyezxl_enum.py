class pyezxl_enum:
	my_web_site = "www.halmoney.com"
	def __init__(self):
		# 사용가능한 색깔을 보다 쉽게 표현하기위해 만들었다
		# 색은 3가지로 구분 : 테이블등을 만들때 사용하면 좋은 색 : ez1~15번까지
		# 12가지의 색을 기본, 약간 옅은 테이블색칠용, 파스텔톤의 3가지로 구분
		# 각 3종류는 7개의 형태로 구분하여 +, -의 형태로 표현을 하도록 하였다
		self.color_nono = {
			"ez1" : 6384127,
			"ez2" : 4699135,
			"ez3" : 9895421,
			"ez4" : 7855479,}

	def line(self):
		enum_line={
		"basic" : 1,
		"-" : -4115 ,
		"-." : 4,
		"-.." : 5,
		"." : -4118,
		"=" : -4119,
		"none" : -4142,
		"/." : 13,
		"continuous" : 1,
		"dash" : -4115 ,
		"dashdot" : 4,
		"dashdotdot" : 5,
		"dot" : -4118,
		"double" : -4119,
		"slantdashdot" : 13,
		"hairline" : 1,
		"thin" : 2,
		"medium" : -4138,
		"thick" : 4,
		"t1" : 1,
		"t2" : 2,
		"t3" : -4138,
		"t4" : 4,
		"basic--" : 1,
		"basic-" : 2,
		"basic+" : -4138,
		"basic++" : 4,
		"diagonaldown" : 5,
		"diagonalup" : 6,
		"edgebottom" : 9,
		"edgeleft" : 7,
		"edgeright" : 8,
		"edgetop" : 10,
		"insidehorizontal" : 12,
		"insidevertical" : 11,
		"inside-h" : 12,
		"inside-v" : 11,
		"\\" : 5,
		"/" : 6,
		"b" : 9,
		"l" : 7,
		"r" : 8,
		"t" : 10,
		"in-h" : 12,
		"in-v" : 11,
		"bottom" : 9,
		"left" : 7,
		"right" : 10,
		"top" : 8,
		"bottom-in" : 12,
		"top-in" : 11,
		"rightleft-in" : 12,
		"leftright-in" : 5,
		}
		return enum_line

	def orientation(self):
		self.enum_orientation={
		"bottom" : -4170,
		"horizontal" : -4128,
		"up" : -4171,
		"vertical" : -4166,
		"downward" : -4170,
		"upward" : -4171,
		}
		return self.enum_orientation

	def copy(self):
		self.enum_copy={
		"pasteall" : -4104,
		"pasteallexceptborders" : 7,
		"pasteallmergingconditionalformats" : 14,
		"pasteallusingsourcetheme" : 13,
		"pastecolumnwidths" : 8,
		"pastecomments" : -4144,
		"pasteformats" : -4122,
		"pasteformulas" : -4123,
		"pasteformulasandnumberformats" : 11,
		"pastevalidation" : 6,
		"pastevalues" : -4163,
		"pastevaluesandnumberformats" : 12,
		"basic" : -4104,
		"all" : -4104,
		"memo" : -4144,
		"format" : -4122,
		"formula" : -4123,
		"formula+format" : 11,
		"value" : -4163,
		"value+format" : 12,
		}
		return self.enum_copy

	def letter(self):
		self.letter={
		"a":"abcdefghijklmnopqrstuvwxyz",
		"ㄱ" :"ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ",
		"가":"가나다라마바사아자차카타파하",
		"1":"1234567890",
		"그리스문자":"αβγδεζήθικλμνξόπρΣτ",
		"로마숫자":"ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ",
		"원ㄱ":"㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭",
		"원가":"㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻",
		"원알":"ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
		"원숫자":"⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿",
		}
		return self.enum_letter