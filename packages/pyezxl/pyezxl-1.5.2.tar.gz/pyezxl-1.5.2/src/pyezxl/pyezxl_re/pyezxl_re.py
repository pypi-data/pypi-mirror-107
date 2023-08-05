# -*- coding: utf-8 -*-

import re

class pyezxl_re:
    my_web_site = "www.halmoney.com"

    def __init__(self):
            self.web_site = "www.halmoney.com"

    def between_a_b(self, input_data, text_a, text_b):
        # 입력된 자료에서 두개문자사이의 글자를 갖고오는것
        replace_lists=[
            ["(","\("],
            [")", "\)"],
        ]
        origin_a = text_a
        origin_b = text_b

        for one_list in replace_lists:
            text_a = text_a.replace(one_list[0], one_list[1])
            text_b = text_b.replace(one_list[0], one_list[1])
        re_basic =text_a+"[^"+str(origin_b)+"]*"+text_b
        result = re.findall(re_basic, input_data)
        return result

    def email_address(self, input_data):
        # 이메일주소 입력
        re_basic ="^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
        result = re.findall(re_basic, input_data)
        return result

    def ip_address(self, input_data):
        # 이메일주소 입력
        re_basic ="((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))"
        result = re.findall(re_basic, input_data)
        return result

    def no_times(self, input_data, m, n):
        # 이메일주소 입력
        re_basic ="^\d{"+str(m)+","+str(n) +"}$"
        result = re.findall(re_basic, input_data)
        return result

    def text_length(self, input_data, m, n):
        # 문자수제한 : m다 크고 n보다 작은 문자
        re_basic ="^.{"+str(m)+","+str(n) +"}$"
        result = re.findall(re_basic, input_data)
        return result

    def check_all_cap(self, input_data):
        # 모두 알파벳대문자
        re_basic ="^[A-Z]+$"
        result = re.findall(re_basic, input_data)
        return result

    def check_date_422 (self, input_data):
        # 모두 알파벳대문자
        re_basic ="^\d{4}-\d{1,2}-\d{1,2}$"
        result = re.findall(re_basic, input_data)
        return result

    def check_korean_only (self, input_data):
        # 모두 한글인지
        re_basic ="[ㄱ-ㅣ가-힣]"
        result = re.findall(re_basic, input_data)
        return result

    def check_korean_only (self, input_data):
        # 모두 영문인지
        re_basic ="[a-zA-Z]"
        result = re.findall(re_basic, input_data)
        return result

    def check_special_char (self, input_data):
        # 특수문자가들어가있는지
        re_basic ="^[a-zA-Z0-9]"
        result = re.findall(re_basic, input_data)
        return result

    def check_handphone (self, input_data):
        # 특수문자가들어가있는지
        re_basic ="^(010|019|011)-\d{4}-\d{4}"
        result = re.findall(re_basic, input_data)
        return result

    def check_basic (self, input_data, re_text):
        # 특수문자가들어가있는지
        re_basic = str(re_text)
        result = re.findall(re_basic, input_data)
        return result
