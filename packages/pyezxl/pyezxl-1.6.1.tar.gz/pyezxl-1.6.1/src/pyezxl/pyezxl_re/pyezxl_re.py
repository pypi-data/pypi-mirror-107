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

    def ezre(self, input_data):
        input_data = input_data.replace(" ", "")
        # 아래의 내용중 순서가 중요하므로 함부러 바꾸지 않기를 바랍니다
        # 1. 제일먼저의것은
        # &로 되어있는것은 제일 마지막에 처리를 하도록 하였다
        # 만약 새로운 글자셋이 있다면 아래의 3개를 같이 넣어야 한다
        # 1."[한글]": "[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]",
        # 2."한글&": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",
        # 3."한글": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",

        ezre_dic = {
            ":최소반복]": "]?",
            ":1번이상]": "]+",
            ":0번이상]": "]*",
            ":0-1번]": "]?",
            "또는": "|",
            "[특수문자": "[",
            "[not": "[^",

            "(앞에있음:": "(?=",
            "(뒤에있음:": "(?<=",
            "(앞에없음:": "(?!",
            "(뒤에없음:": "(?<!",

            "[1번이상]": "+",
            "[0번이상]": "*",
            "[0-1번]": "?",
            "[맨앞]": "^",
            "[시작]": "^",
            "[맨뒤]": "$",
            "[맨끝]": "$",
            "[끝]": "$",
            "[최소반복]": "?",

            "[공백]": "\s",
            "[문자]": ".",
            "[숫자]": "0-9",
            "[영어]": "[a-zA-Z]",
            "[영어대문자]": "[A-Z]",
            "[영어소문자]": "[a-z]",
            "[한글]": "[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]",

            "[영어&숫자]": "\w",
            "[숫자&영어]": "\w",

            "문자&": ".",
            "숫자&": "0-9",
            "영어&": "a-zA-Z",
            "영어대문자&": "A-Z",
            "영어소문자&": "a-z",
            "한글&": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",

            "숫자": "0-9",
            "영어": "a-zA-Z",
            "영어대문자": "A-Z",
            "영어소문자": "a-z",
            "한글": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",
        }

        ezre_list = ["\[최소\d*?번\]",
                     "\[최대\d*?번\]",
                     "\[\d*-\d*?번\]",
                     "\[\d*?번\]",
                     ":최소\d*?번\]",
                     ":최대\d*?번\]",
                     ":\d*-\d*?번\]",
                     ":\d*?번\]"]

        changed_data = input_data
        print("변환전 ==> ", changed_data)

        for num_1 in range(len(ezre_list)):
            compile_1 = re.compile(ezre_list[num_1])
            result_1 = compile_1.findall(changed_data)
            if result_1:
                for num in range(len(result_1)):
                    one = result_1[num]
                    compile_1 = re.compile("\d+")
                    no = compile_1.findall(one)
                    if num_1 == 0:
                        new_str = "{" + str(no[0]) + ",}"
                    elif num_1 == 1:
                        new_str = "{," + str(no[0]) + "}"
                    elif num_1 == 2:
                        new_str = "{" + str(no[0]) + "," + str(no[1]) + "}"
                    elif num_1 == 3:
                        new_str = "{" + str(no[0]) + "}"
                    elif num_1 == 4:
                        new_str = "]{" + str(no[0]) + ",}"
                    elif num_1 == 5:
                        new_str = "]{," + str(no[0]) + "}"
                    elif num_1 == 6:
                        new_str = "]{" + str(no[0]) + "," + str(no[1]) + "}"
                    elif num_1 == 7:
                        new_str = "]{" + str(no[0]) + "}"
                    changed_data = changed_data.replace(result_1[num], new_str)

        for ezre_value in ezre_dic.keys():
            re_value = ezre_dic[ezre_value]
            changed_data = changed_data.replace(ezre_value, re_value)
        print("중간변환 ==> ", changed_data)

        min_dic = {
            "a-zA-Z0-9": "\w",
            "0-9a-zA-Z": "\w",
            "0-9": "\d",
        }
        for ezre_value in min_dic.keys():
            re_value = min_dic[ezre_value]
            changed_data = changed_data.replace(ezre_value, re_value)

        print("변환완료 ==> ", changed_data)

        return changed_data
