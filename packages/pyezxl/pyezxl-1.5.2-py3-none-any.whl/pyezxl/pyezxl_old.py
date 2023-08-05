# -*- coding: utf-8 -*-

import win32com.client
import re
import string
import win32gui

class pyezxl:
    my_web_site = "www.halmoney.com"

    def __init__(self, filename=None):
        # 만약 화일의 경로가 있으면 그 화일을 열도록 한다
        self.xlApp = win32com.client.dynamic.Dispatch('Excel.Application')
        self.xlApp.Visible = 1
        self.filename = filename.lower()

        if self.filename == 'activeworkbook' or self.filename == '':
            # activeworkbook으로 된경우는 현재 활성화된 workbook을 그대로 사용한다
            self.xlBook = self.xlApp.ActiveWorkbook
            if self.xlBook == None:
                # 만약 activework북을 부르면서도 화일이 존재하지 않으면 새로운 workbook을 만드는것이다
                try:
                    self.xlApp.WindowState = -4137
                    self.xlBook = self.xlApp.WorkBooks.Add()
                except:
                    win32gui.MessageBox(0, "There is no Activeworkbook", self.my_web_site, 0)

        elif not (self.filename == 'activeworkbook') and self.filename:
            # 만약 화일이름이 따로 주어지면 그화일을 연다
            try:
                self.xlApp.WindowState = -4137
                self.xlBook = self.xlApp.Workbooks.Open(self.filename)
            except:
                win32gui.MessageBox(0, "Please check file path", self.my_web_site, 0)
        else:
            # 빈것으로 된경우는 새로운 workbook을 하나 열도록 한다
            self.xlApp.WindowState = -4137
            self.xlBook = self.xlApp.WorkBooks.Add()

    def change_char_num(self, input_data):
        # input_data : aa => result : 27
        # 문자를 숫자로 바꿔주는 것
        if input_data.isalpha():
            input_data = input_data.lower()
            reversed_input_data = ''.join(reversed(input_data))
            temp_result = [ord(letter) - 96 for letter in reversed_input_data]
            result = 0
            for one in range(len(temp_result)):
                result = result + pow(26, one) * temp_result[one]
        else:
            result = input_data
        return int(result)

    def change_num_char(self, input_data):
        # input_data : 27 => result : aa
        # 숫자를 문자로 바꿔주는 것
        base_number = int(input_data)
        result_01 = ''
        result = []
        while base_number > 0:
            div = base_number // 26
            mod = base_number % 26
            if mod == 0:
                mod = 26
                div = div - 1
            base_number = div
            result.append(mod)
        for one_data in result:
            result_01 = string.ascii_lowercase[one_data - 1] + result_01
        return result_01


    def change_rgb_int(self, input_data):
        # rgb인 값을 color에서 인식이 가능한 값ㄷ으로 변경하는 것이다
        result = (int(input_data[2]))*(256**2)+(int(input_data[1]))*(256)+int(input_data[0])
        return result

    def change_sheet_name(self, sheet_name_old, sheet_name_new):
        # 시트이름을 바꿉니다
        self.xlBook.Worksheets(sheet_name_old).Name = sheet_name_new

    def change_x_y(self, input_data):
        # 행렬의 자료를 서로 바꾸는 것이다
        # 적당한 이름을 위해 한번더 사용한 것이다
        result = self.swap_list_data(input_data)
        return result

    def check_address_value(self, address):
        # 어떠한 형태의 주소값이 오더라도 결과값을 [x1, y1, x2, y2]의 형태로 만들어 주는것
        # input_data : [1,2],[1,1,2,3],[$A$1], [$A$1:$B$2], [$1:$7], [$A:$B], [A1]
        # output_data : [1,2],[1,1,2,3],[1,1], [1,1,2,2], [1,0,7.0], [0,1,0,2], [1,1]
        check_string = re.compile(r"([:$a-zA-Z]+)")
        check_range = re.compile(r"([:]+)")
        check_num = re.compile(r"([0-9]+)")

        result_final = []
        result_final_01 = []
        result_final_02 = []

        #빈것이면 현재 선택한 영역을 돌려준다
        if address == "":
            address = self.read_range_select()
        elif type(address) != type([]):
            address = [address]

        for one_data in address:
            one_data = str(one_data)
            one_data = one_data.replace('$', '')
            result_temp = []
            result_final_01 = []
            result_final_02 = []
            data_type = {"range": "no", "num_only": "no", "string_only": "no"}
            # 어떤 형태의 주소인지 확인한다

            if check_range.findall(one_data):
                data_type["range"] = "yes"
            if check_num.findall(one_data.split(":")[0]):
                data_type["num_only"] = "yes"
            if check_string.findall(one_data.split(":")[0]):
                data_type["string_only"] = "yes"

            if data_type["range"] == "no" and data_type["num_only"] == "yes" and data_type["string_only"] == "no":
                # [1, 2], [1, 1, 2, 3] => 이런형태이므로 그대로 값을 넣어준다
                result_temp.append(one_data)

            if data_type["range"] == "no" and data_type["num_only"] == "no" and data_type["string_only"] == "yes":
                # [$A$1], [A1] => 이런형태
                temp_value = self.split_eng_num(one_data)
                temp_value1 = self.change_char_num(temp_value[0])
                result_temp.append(int(temp_value[1]))
                result_temp.append(int(temp_value1))

            if data_type["range"] == "no" and data_type["num_only"] == "yes" and data_type["string_only"] == "yes":
                # [$A$1], [A1] => 이런형태
                temp_value = self.split_eng_num(one_data)
                temp_value1 = self.change_char_num(temp_value[0])
                result_temp.append(int(temp_value[1]))
                result_temp.append(int(temp_value1))

            if data_type["range"] == "yes" and data_type["num_only"] == "yes" and data_type["string_only"] == "yes":
                # [$A$1:$B$2] => 이런형태
                for data_001 in one_data.split(":"):
                    temp_value = self.split_eng_num(data_001)
                    temp_value1 = self.change_char_num(temp_value[0])
                    result_temp.append(int(temp_value[1]))
                    result_temp.append(int(temp_value1))

            if data_type["range"] == "yes" and data_type["num_only"] == "no" and data_type["string_only"] == "yes":
                # [$A:$B] => 이런형태
                for data_001 in one_data.split(":"):
                    result_temp.append(int(0))
                    temp_value = self.change_char_num(data_001)
                    result_temp.append(int(temp_value))

            if data_type["range"] == "yes" and data_type["num_only"] == "yes" and data_type["string_only"] == "no":
                # [$1:$7] => 이런형태
                aaa = one_data.split(":")
                for data_001 in aaa:
                    result_temp.append(int(data_001))
                    result_temp.append(int(0))

            result_final.extend(result_temp)
        if len(result_final) == 2: result_final_01 = [int(result_final[0]), int(result_final[1]), int(result_final[0]), int(result_final[1])]
        if len(result_final) == 4: result_final_01 = [int(result_final[0]), int(result_final[1]), int(result_final[2]), int(result_final[3])]

        #혹시 입력한 자료가 [1,2,3,4]의 형태가 아닌 [3,4,1,2]로 되어잇을때 정렬을 다시하는것이다
        temp1 = [result_final_01[0], result_final_01[2]]
        temp1.sort()

        temp2 = [result_final_01[1], result_final_01[3]]
        temp2.sort()

        result_final_02 = [temp1[0], temp2[0], temp1[1], temp2[1]]
        return result_final_02

    def check_range_address(self, xyxy):
        #비슷하게 추측이 가능한 함수를 하나더 만든 것이다
        return self.check_address_value(xyxy)

    def check_sheet_name(self, sheet_name=""):
        # sheet이름을 확인해서 돌려준다.
        # 아무것도 없으면 현재 활성화된 activesheet를 돌려준다
        # read와 check의 의미 차이는 check는 어떤 조건에서 2개이상의 다른 값을 보여줄때이며
        # read는 조건문등의 구문이 없이 단순히 값을 읽어올때 사용한다
        if str(sheet_name).lower() == "activesheet" or sheet_name == "":
            sheet = self.xlApp.ActiveSheet
        else:
            sheet = self.xlBook.Worksheets(sheet_name)
        return sheet

    def check_x_empty(self, sheet_name, x):
        # 열전체가 빈 것인지 확인해서 돌려준다
        # 전체가 비었을때는 0을 돌려준다
        x_check = self.check_x_y(x)
        x_new = self.change_char_num(str(x_check[0]))
        sheet = self.check_sheet_name(sheet_name)
        result = self.xlApp.WorksheetFunction.CountA(sheet.Rows(int(x_new)).EntireRow)
        return result

    def check_y_empty(self, sheet_name, y):
        # 세로열 전체가 빈 것인지 확인해서 돌려준다
        # 전체가 비었을때는 0을 돌려준다
        y_check = self.check_x_y(y)
        y_new = self.change_char_num(str(y_check[0]))
        sheet = self.check_sheet_name(sheet_name)
        result = self.xlApp.WorksheetFunction.CountA(sheet.Columns(y_new).EntireColumn)
        return result

    def check_x_y(self, input_data):
        # 입력의 형태 : 3, [3], [2,3], D, [A,D], [D]
        # 출력 : [3,3], [2,3], [4,4,], [1,4]
        # x나 y의 하나를 확인할때 입력을 잘못하는 경우를 방지하기위해 사용
        result = []
        if type([]) == type(input_data):
            if len(input_data) == 1:
                input_data[0] = self.change_char_num(str(input_data[0]))
                result = [input_data[0], input_data[0]]
            if len(input_data) == 2:
                input_data[0] = self.change_char_num(str(input_data[0]))
                input_data[1] = self.change_char_num(str(input_data[1]))
                result = input_data
        else:
            input_data = str(input_data)
            if re.match('[a-zA-Z0-9]', input_data):
                if re.match('[a-zA-Z]', input_data):
                    input_data = self.change_char_num(input_data)
                    result = [input_data, input_data]
                else:
                    result = [input_data, input_data]
        return result

    def copy_range_y(self, sheet_name1, sheet_name2, yy0, yy1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name1)
        sheet2 = self.check_sheet_name(sheet_name2)

        yy0_1, yy0_2 = self.check_x_y(yy0)
        yy1_1, yy1_2 = self.check_x_y(yy1)

        yy0_1 = self.change_num_char(yy0_1)
        yy0_2 = self.change_num_char(yy0_2)
        yy1_1 = self.change_num_char(yy1_1)
        yy1_2 = self.change_num_char(yy1_2)
        print(yy0_1, yy0_2, yy1_1, yy1_2)

        sheet1.Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Copy()
        sheet2.Select()
        sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Select()
        sheet2.Paste()

    def cut_range_y(self, sheet_name1, sheet_name2, yy0, yy1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name1)
        sheet2 = self.check_sheet_name(sheet_name2)

        yy0_1, yy0_2 = self.check_x_y(yy0)
        yy1_1, yy1_2 = self.check_x_y(yy1)

        yy0_1 = self.change_num_char(yy0_1)
        yy0_2 = self.change_num_char(yy0_2)
        yy1_1 = self.change_num_char(yy1_1)
        yy1_2 = self.change_num_char(yy1_2)
        print(yy0_1, yy0_2, yy1_1, yy1_2)

        sheet1.Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Copy()
        sheet2.Select()
        sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Select()
        sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Insert()

        yy0_1_no = self.change_char_num(yy0_1)
        yy0_2_no = self.change_char_num(yy0_2)
        yy1_1_no = self.change_char_num(yy1_1)
        yy1_2_no = self.change_char_num(yy1_2)

        if sheet1 == sheet2:
            if yy0_1_no <= yy1_1_no:
                sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Delete()
            else:
                new_yy0_1 = self.change_num_char(yy0_1_no + yy1_2_no - yy1_1_no)
                new_yy0_2 = self.change_num_char(yy0_2_no + yy1_2_no - yy1_1_no)
                sheet1.Columns(str(new_yy0_1) + ':' + str(new_yy0_2)).Delete()
        else:
            sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Delete()


    def copy_range_x(self, sheet_name1, sheet_name2, xx0, xx1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name1)
        sheet2 = self.check_sheet_name(sheet_name2)

        xx0_1, xx0_2 = self.check_x_y(xx0)
        xx1_1, xx1_2 = self.check_x_y(xx1)

        xx0_1 = self.change_char_num(xx0_1)
        xx0_2 = self.change_char_num(xx0_2)
        xx1_1 = self.change_char_num(xx1_1)
        xx1_2 = self.change_char_num(xx1_2)

        sheet1.Select()
        sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Select()
        sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Copy()
        sheet2.Select()
        sheet2.Rows(str(xx1_1) + ':' + str(xx1_2)).Select()
        sheet2.Paste()

    def cut_range_x(self, sheet_name1, sheet_name2, xx0, xx1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name1)
        sheet2 = self.check_sheet_name(sheet_name2)

        xx0_1, xx0_2 = self.check_x_y(xx0)
        xx1_1, xx1_2 = self.check_x_y(xx1)

        xx0_1 = self.change_char_num(xx0_1)
        xx0_2 = self.change_char_num(xx0_2)
        xx1_1 = self.change_char_num(xx1_1)
        xx1_2 = self.change_char_num(xx1_2)

        sheet1.Select()
        sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Select()
        sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Copy()
        sheet2.Select()
        sheet2.Rows(str(xx1_1) + ':' + str(xx1_2)).Select()
        sheet2.Rows(str(xx1_1) + ':' + str(xx1_2)).Insert()

        if sheet1 == sheet2:
            if xx0_1 <= xx1_1:
                sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Delete()
            else:
                new_xx0_1 = self.change_num_char(xx0_1 + xx1_2 - xx1_1)
                new_xx0_2 = self.change_num_char(xx0_2 + xx1_2 - xx1_1)
                sheet1.Rows(str(new_xx0_1) + ':' + str(new_xx0_2)).Delete()
        else:
            sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Delete()

    def delete_line_x(self, sheet_name, xx):
        # 한줄삭제하기
        self.delete_range_x(sheet_name, xx)

    def delete_line_y(self, sheet_name, yy):
        # 한줄삭제하기
        self.delete_range_y(sheet_name, yy)

    def delete_range_color(self, sheet_name, xyxy):
        # 영역의 모든 색을 지운다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Interior.Pattern = -4142
        my_range.Interior.TintAndShade = 0
        my_range.Interior.PatternTintAndShade = 0

    def delete_range_line(self, sheet_name, xyxy):
        # 영역에 선의색을 다 없애는것
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = xyxy
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Borders.LineStyle = 0

    def delete_range_link(self, sheet_name, xyxy):
        # 영역의 모든 색을 지운다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Hyperlinks.Delete()

    def delete_range_name(self, sheet_name, range_name):
        # 입력한 이름을 삭제한다
        # name은 workbook으로 되지만 동일하게 하기위하여 sheet_name을 넣은 것이다
        sheet = self.check_sheet_name(sheet_name)
        result = self.xlBook.Names(range_name).Delete()
        return result

    def delete_range_samevalue(self, sheet_name, xyxy):
        # 선택 영역중 2번이상 반복되는 값은 지우는 것이다
        temp_result = []
        select_range = self.read_range_select()
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet = self.check_sheet_name(sheet_name)

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                temp_data = self.read_cell_value(sheet, [x, y])
                if temp_data in temp_result:
                    self.write_cell_value(sheet, [x, y], "")
                else:
                    temp_result.append(temp_data)

    def delete_range_value(self, sheet_name, xyxy):
        # 선택한영역의 모든 값을 지우는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.ClearContents()

    def delete_range_x(self, sheet_name, xx):
        # 가로 한줄삭제하기
        # 입력형태는 2, [2,3]의 두가지가 가능하다
        sheet = self.check_sheet_name(sheet_name)
        new_xx = self.check_x_y(xx)
        sheet.Rows(str(new_xx[0]) + ':' + str(new_xx[1])).Delete(-4121)

    def delete_range_xx(self, sheet_name, xx):
        self.delete_range_x(sheet_name, xx)

    def delete_range_y(self, sheet_name, yy):
        # 세로 한줄삭제하기
        sheet = self.check_sheet_name(sheet_name)
        new_yy = self.check_x_y(yy)
        sheet.Columns(str(new_yy[0]) + ':' + str(new_yy[1])).Delete()

    def delete_range_yy(self, sheet_name, yy):
        self.delete_range_y(sheet_name, yy)

    def delete_sheet(self, sheet_name=""):
        # 시트하나 삭제하기
        sheet = self.check_sheet_name(sheet_name)
        self.xlApp.DisplayAlerts = False
        sheet.Delete()
        self.xlApp.DisplayAlerts = True


    def delete_sheet_drawing(self, sheet_name=""):
        # 특정 시트안의 그림을 다 지우는 것이다
        sheet = self.check_sheet_name(sheet_name)
        for aa in range(sheet.Shapes.Count, 0, -1):
            # Range를 앞에서부터하니 삭제하자마자 번호가 다시 매겨져서, 뒤에서부터 삭제하니 잘된다
            sheet.Shapes(aa).Delete()
        return

    def delete_sheet_one(self, sheet_name=""):
        # 3개의 단어를 위하여 제일 가까운 단어를 사용
        self.delete_sheet(sheet_name)

    def delete_sheet_value(self, sheet_name):
        # 시트의 모든 값을 삭제한다
        sheet = self.check_sheet_name(sheet_name)
        sheet.Cells.ClearContents()

    def delete_x_value(self, sheet_name, xx):
        # 한줄값만 삭제하기
        sheet = self.check_sheet_name(sheet_name)
        new_xx = self.check_x_y(xx)
        sheet.Rows(str(new_xx[0]) + ':' + str(new_xx[1])).ClearContents()

    def delete_y_value(self, sheet_name, yy):
        # 한줄값만 삭제하기
        sheet = self.check_sheet_name(sheet_name)
        new_yy = self.check_x_y(yy)
        sheet.Columns(str(new_yy[0]) + ':' + str(new_yy[1])).ClearContents()

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

    def insert_line_x(self, sheet_name, x):
        # 가로열을 한줄삽입하기
        sheet = self.check_sheet_name(sheet_name)
        x_new = self.check_x_y(x)
        x_no = self.change_char_num(str(x_new[0]))
        sheet.Range(str(x_no) + ':' + str(x_no)).Insert()

    def insert_line_y(self, sheet_name, num):
        # 세로행을 한줄삽입하기
        sheet = self.check_sheet_name(sheet_name)
        num_r1 = self.change_num_char(num)
        sheet.Columns(str(num_r1) + ':' + str(num_r1)).Insert()

    def insert_range_button(self, sheet_name, xyxy, macro, title):
        # 버튼을 만들어서 그 버튼에 매크로를 연결하는 것이다
        # 매크로와 같은것을 특정한 버튼에 연결하여 만드는것을 보여주기위한 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        new_btn = sheet.Buttons()
        new_btn.Add(x1, x2, y1, y2)
        new_btn.OnAction = macro
        new_btn.Text = title

    def insert_range_picture(self, sheet_name="", file_name=""):
        # 사진을 입력하는 것
        sheet = self.check_sheet_name(sheet_name)
        sheet.Shapes.AddPicture(file_name, 0, 1, 541.5, 92.25, 192.75, 180)

    def insert_sheet_new(self):
        # 시트하나 추가하기
        self.xlBook.Worksheets.Add()

    def intersect_range1_range2(self, rng1, rng2):
        # 두개의 영역에서 교차하는 구간을 돌려준다
        # 만약 교차하는게 없으면 ""을 돌려준다
        range_1 = self.check_range_address(rng1)
        range_2 = self.check_range_address(rng2)

        x11, y11, x12, y12 = range_1
        x21, y21, x22, y22 = range_2

        if x11 == 0:
           x11 = 1
           x12 = 1048576
        if x21 == 0:
           x21 = 1
           x22 = 1048576
        if y11 == 0:
           y11 = 1
           y12 = 16384
        if y21 == 0:
           y21 = 1
           y22 = 16384

        new_range_x = [x11, x21, x12, x22]
        new_range_y = [y11, y21, y12, y22]

        new_range_x.sort()
        new_range_y.sort()

        if x11 <= new_range_x[1] and x12 >= new_range_x[2] and y11 <= new_range_y[1] and y12 >= new_range_y[1]:
            result = [new_range_x[1], new_range_y[1], new_range_x[2], new_range_y[2]]
        else:
            result = "교차점없음"
        return result

    def move_down_end(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4121).Select()
        return "ok"

    def move_left_end(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4159).Select()
        return "ok"

    def move_range_x(self, sheet_name1, sheet_name2, xx0, xx1):
        self.cut_range_x(sheet_name1, sheet_name2, xx0, xx1)

    def move_range_y(self, sheet_name1, sheet_name2, yy0, yy1):
        self.cut_range_y(sheet_name1, sheet_name2, yy0, yy1)

    def move_right_end(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4161).Select()
        return "ok"

    def move_up_end(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4162).Select()
        return "ok"

    def read_address_name(self, sheet_name, xyxy_name):
        sheet = self.check_sheet_name(sheet_name)
        temp = sheet.Range(xyxy_name).Address
        result = self.check_address_value(temp)
        return result

    def read_activesheet_name(self):
        # 현재의 엑셀중에서 활성화된 시트의 이름을 돌려준다
        return self.xlApp.ActiveSheet.Name

    def read_activecell_address(self):
        # 돌려주는 값 ['행번호','열번호','현재셀의 값']
        xy = self.check_address_value(self.xlApp.ActiveCell.Address)
        return xy

    def read_activecell_value(self):
        # 현재 셀 하나의 값을 돌려준다
        # 예전 함수에서 약간 변형한것이다
        value = self.xlApp.ActiveCell.Value
        return value

    def read_activecell_range(self):
        # 돌려주는 값 [x, y]
        xyxy = self.read_activecell_address()
        return xyxy

    def read_cell_value(self, sheet_name, xy):
        # 값을 일정한 영역에서 갖고온다
        # 만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        result = sheet.Cells(x1, y1).value
        return result

    def read_continousrange_value(self, sheet_name, xyxy):
        # 현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다
        # **************다시한번 봐야할 코드이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)

        bottom = x1  # 아래의 행을 찾는다
        while sheet.Cells(bottom, y1).Value not in [None, '']:
            bottom = bottom + 1
        right = y2  # 오른쪽 열
        while sheet.Cells(x2, right).Value not in [None, '']:
            right = right + 1
        return sheet.Range(sheet.Cells(x1, y1), sheet.Cells(bottom, right)).Value

    def read_messagebox_value(self, text_01="www.halmoney.com"):
        # 메세지 박스로 원하는 겂을 알려주는 것이다
        result = self.xlApp.InputBox(text_01)
        return result

    def read_range_currentregion(self, xy=""):
        # 이것은 현재의 셀에서 공백과 공백열로 둘러싸인 활성셀영역을 돌려준다
        if xy == "":
            result = self.check_address_value(self.xlApp.ActiveCell.CurrentRegion.Address)
        else:
            sheet = self.check_sheet_name("")
            result = self.check_address_value(sheet.Cells(xy[0], xy[1]).CurrentRegion.Address)
        return result

    def read_range_name(self):
        # 현재 시트의 이름을 전부 돌려준다
        # [번호, 영역이름, 영역주소]
        names_count = self.xlBook.Names.Count
        result = []
        if names_count > 0:
            for aaa in range(1, names_count + 1):
                name_name = self.xlBook.Names(aaa).Name
                name_range = self.xlBook.Names(aaa)
                result.append([aaa, str(name_name), str(name_range)])
        return result

    def read_name_all(self):
        #모든 이름을 읽어오는 것이다
        names_count = self.xlBook.Names.Count
        result = []
        if names_count > 0:
            for aaa in range(1, names_count + 1):
                name_name = self.xlBook.Names(aaa).Name
                result.append(str(name_name))
        return result

    def read_range_select(self):
        # 현재선택된 영역의 주소값을 돌려준다
        result = ""
        temp_address = self.xlApp.Selection.Address
        temp_list = temp_address.split(",")
        if len(temp_list) == 1:
            result = self.check_address_value(self.xlApp.Selection.Address)
        if len(temp_list) > 1:
            result = []
            for one_address in temp_list:
                result.append(self.check_address_value(one_address))
        return result

    def read_range_usedrange(self, sheet_name=""):
        # 이것은 usedrange를 돌려주는 것이다. 값은 리스트이며 처음은
        # usedrange의 시작셀 ,두번째는 마지막셀값이며 세번째는 전체영역을 돌려주는 것이다
        sheet = self.check_sheet_name(sheet_name)
        result = self.check_address_value(sheet.usedrange.address)
        return result

    def read_range_value(self, sheet_name, xyxy):
        # 값을 일정한 영역에서 갖고온다
        # 만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        temp_result = my_range.Value
        result = []
        for one_data in temp_result:
            result.append(list(one_data))
        return result

    def read_sheet_count(self):
        # 시트의 갯수를 돌려준다
        return self.xlBook.Worksheets.Count

    def read_sheet_name(self):
        # 현재 워크북의 모든 시트알아내기
        temp_list = []
        for var_02 in range(1, self.read_sheet_count() + 1):
            temp_list.append(self.xlBook.Worksheets(var_02).Name)
        return temp_list

    def read_sheet_names(self):
        # 현재 워크북의 모든 시트알아내기
        temp_list = []
        for var_02 in range(1, self.read_sheet_count() + 1):
            temp_list.append(self.xlBook.Worksheets(var_02).Name)
        return temp_list

    def read_workbook_fullname(self):
        # application의 이름과 전체경로를 돌려준다
        return self.xlBook.FullName

    def read_workbook_name(self):
        # application의 이름을 돌려준다
        return self.xlBook.Name

    def read_workbook_path(self):
        # application의 경로를 돌려준다
        return self.xlBook.Path

    def read_workbook_username(self):
        #사용자 이름을 읽어온다
        return self.xlApp.Username

    def read_x_value(self, sheet_name, x):
        # 한 가로행의 전체값을 갖고온다
        sheet = self.check_sheet_name(sheet_name)
        x_check = self.change_char_num(x)
        result = sheet.Cells(x_check, 1).EntireRow.Value
        return result

    def set_range_rgbcolor(self, sheet_name, xyxy, input_data):
        # 영역에 색깔을 입힌다
        # 엑셀에서의 색깔의 번호는 아래의 공식처럼 만들어 진다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        rgb_to_int = (int(input_data[2]))*(256**2)+(int(input_data[1]))*(256)+int(input_data[0])
        my_range.Interior.Color = rgb_to_int

    def select_sheet_range(self, sheet_name, xyxy):
        #영역을 선택한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Select()

    def set_cell_bold(self, sheet_name, xyxy):
        # 셀안의 값을 진하게 만든다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Font.Bold = True

    def set_cell_color(self, sheet_name, xy, input_data):
        # 셀 하나에 색을 입힌다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Interior.ColorIndex = input_data

    def set_range_select(self, sheet_name, xyxy):
        #영역을 선택한다
        self.select_sheet_range(sheet_name, xyxy)

    def set_range_autofilter(self, sheet_name, row1, row2=None):
        # 엑셀의 자동필터 기능을 추가한 것입니다
        sheet = self.check_sheet_name(sheet_name)
        if row2 == None:
            row2 = row1
        a = str(row1) + ':' + str(row2)
        sheet.Rows(a).Select()
        sheet.Range(a).AutoFilter(1)

    def set_range_color(self, sheet_name, xyxy, input_data):
        # 영역에 색깔을 입힌다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Interior.ColorIndex = input_data

    def set_range_font(self, sheet_name, xyxy, font):
        # 영역에 글씨체를 설정한다
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet = self.check_sheet_name(sheet_name)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.font.Name = font

    def set_range_fontcolor(self, sheet_name, xyxy, font_name):
        # 영역에 글씨체를 설정한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Font.ColorIndex = font_name

    def set_range_fontsize(self, sheet_name, xyxy, input_data):
        # 영역에 글씨크기를 설정한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.font.Size = input_data

    def set_range_formula(self, sheet_name, xyxy, input_data):
        #영역에 식을 할당하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Formula = input_data

    def set_range_line(self, sheet_name, xyxy, value):
        # 안쪽의 선들지정
        # [선의위치, 라인스타일, 굵기, 색깔]
        # 선의위치 (5-대각선 오른쪽, 6-왼쪽대각선, 7:왼쪽, 8;위쪽, 9:아래쪽, 10:오른쪽, 11:안쪽세로, 12:안쪽가로)
        # 라인스타일 (1-실선, 2-점선, 3-가는점선, 6-굵은실선,
        # 굵기 (0-이중, 1-얇게, 2-굵게)
        # 색깔 (0-검정, 1-검정3-빨강),
        # [[7,1,2,1],[8,1,2,1],[9,1,2,1],[10,1,2,1], [12,3,1,1], [11,1,2,1] ]

        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Borders(value[0])
        print(value[0],value[1],value[2],value[3])
        my_range.Color = int(value[3])
        my_range.Weight = int(value[2])
        #여기에서 linestyle을 제일 나중에 해야지 잘적용이 되며, 만약 다른것을 나중에 하면 점선으로만 나온다
        my_range.LineStyle = int(value[1])

    def set_range_merge(self, sheet_name, xyxy):
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Merge(0)

    def set_range_name(self, sheet_name, xyxy, name):
        #영역에 이름을 지정한다
        self.write_range_name(sheet_name, xyxy, name)

    def set_range_nocolor(self, sheet_name, xyxy):
        # 영역에 선의색을 다 없애는것
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = xyxy
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range .Interior.Pattern = 0
        my_range .Interior.PatternTintAndShade = 0

    def set_range_numberformat(self, sheet_name, xyxy, numberformat):
        # 영역에 숫자형식을 지정하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.NumberFormat = numberformat

    def set_range_wellusedline(self):
        # 자주 사용하는 테두리선을 지정해 놓고 사용을 하는것
        # 이 코드는 선택된 영역의 테두리선을 긋는 것과 맨앞부분에 글자가 있는 부분을 색깔을 칠하는것
        # 만약 화일의 경로가 있으면 그 화일을 열도록 한다
        # [위치, 선종류, 스타일, 색깔, 굵기]

        # Borders위치 (7:왼쪽, 8;위쪽, 9:아래쪽, 10:오른쪽, 11:안쪽세로, 12:안쪽가로)
        # Weight 선종류 ( 1: 많이 얇은,  2: 얇은선, -4138: 보통, 4:두꺼운
        # LineStyle 선스타일 (1 : 실선, -4115 : 점선, -4119: 이중라인)
        # ColorIndex선색 (1: 검정, 3:빨강)

        well_used_line = [[12, 1, 1, 1], [11, 2, 1, 1], [8, -4138, 1, 1], [10, -4138, 1, 1], [9, -4138, 1, 1],
                          [7, -4138, 1, 1]]

        sheet = self.check_sheet_name()
        x1, y1, x2, y2 = self.read_range_select()
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range_top = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x1, y2))
        my_range_bottom = sheet.Range(sheet.Cells(x2, y1), sheet.Cells(x2, y2))

        for data in well_used_line:
            for range_data in [my_range, my_range_top, my_range_bottom]:
                range_data.Borders(data[0]).Weight = data[1]
                range_data.Borders(data[0]).LineStyle = data[2]
                range_data.Borders(data[0]).ColorIndex = data[3]

    def set_sheet_fullscreen(self, fullscreen=1):
        # 전체화면으로 보기
        self.xlApp.DisplayFullScreen = fullscreen

    def set_sheet_gridline(self):
        # 그리드 라인을 계속 바꾼다
        if self.xlApp.ActiveWindow.DisplayGridlines == 0:
            self.xlApp.ActiveWindow.DisplayGridlines = 1
        else:
            self.xlApp.ActiveWindow.DisplayGridlines = 0

    def set_sheet_preview(self, sheet_name=""):
        # 미리보기기능입니다
        sheet = self.check_sheet_name(sheet_name)
        sheet.PrintPreview()

    def set_sheet_visible(self, input_data=0):
        # 실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
        self.xlApp.Visible = input_data

    def set_workbook_close(self):
        # 현재는 close를 시키면 엑셀워크북만이 아니라 엑셀자체도 종료 시킵니다
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp

    def set_workbook_fullscreen(self, fullscreen=1):
        # 전체화면으로 보기
        self.xlApp.DisplayFullScreen = fullscreen

    def set_workbook_hide(self):
        # 실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
        # visible로 통합
        self.xlApp.Visible = 0

    def set_workbook_save(self, newfilename=None):
        # 별도의 지정이 없으면 기존의 화일이름으로 저장합니다
        if newfilename:
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()

    def set_wrap_on(self, sheet_name, xyxy, input_data):
        # 셀의 줄바꿈을 설정할때 사용한다
        # 만약 status를 false로 하면 줄바꿈이 실행되지 않는다.
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet = self.check_sheet_name(sheet_name)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.WrapText = input_data

    def set_x_length(self, sheet_name, xx, height=13.5):
        # 가로열의 높이를 설정하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        new_xx = self.check_x_y(xx)
        my_range = sheet.Range(sheet.Cells(new_xx[0], 1), sheet.Cells(new_xx[1], 5))
        my_range.Select()
        my_range.EntireRow.RowHeight = height

    def set_y_length(self, sheet_name, yy, length=8.38):
        # 열이나 행의 넓이를 조절한다
        # 엑셀은 기본적으로 넓이는 8.38 로, 높이는 13.5로 되어있읍니다
        sheet = self.check_sheet_name(sheet_name)
        new_yy = self.check_x_y(yy)
        my_range = sheet.Range(sheet.Cells(1, new_yy[0]), sheet.Cells(1, new_yy[1]))
        my_range.EntireColumn.ColumnWidth = length

    def set_y_numberproperty(self, sheet_name, y_old, style):
        # 각 열을 기준으로 셀의 속성을 설정하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        y_new = self.check_x_y(y_old)
        y = self.change_char_num(y_new)
        if style == 1:  # 날짜의 설정
            sheet.Columns(y).NumberFormatLocal = "mm/dd/yy"
        elif style == 2:  # 숫자의 설정
            sheet.Columns(y).NumberFormatLocal = "_-* #,##0.00_-;-* #,##0.00_-;_-* '-'_-;_-@_-"
        elif style == 3:  # 문자의 설정
            sheet.Columns(y).NumberFormatLocal = "@"

    def show_messagebox_value(self, input_data, web="www.halmoney.com"):
        # 메세지박스를 이용하여 원하는 내용을 보여준다
        win32gui.MessageBox(0, input_data, web, 0)

    def sort_range_unique(self, sheet_name, xyxy):
        # 선택한 자료중에서 고유한 자료만을 골라내는 것이다
        # 자료중에서 고유한것을 찾아내서, 선택영역에 다시 쓴다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        temp_datas = self.read_range_value(sheet, xyxy)
        temp_result = []
        for one_list_data in temp_datas:
            for one_data in one_list_data:
                if one_data in temp_result or type(one_data) == type(None):
                    pass
                else:
                    temp_result.append(one_data)
        self.delete_range_value(sheet, xyxy)

        for num in range(len(temp_result)):
            mox, namuji = divmod(num, x2 - x1 + 1)
            self.write_cell_value(sheet, [x1 + namuji, y1 + mox], temp_result[num])

    def split_eng_num(self, data):
        # 단어중에 나와있는 숫자, 영어를 분리하는기능
        re_compile = re.compile(r"([a-zA-Z]+)([0-9]+)")
        result = re_compile.findall(data)
        new_result = []
        for dim1_data in result:
            for dim2_data in dim1_data:
                new_result.append(dim2_data)
        return new_result

    def split_range_unmerge(self, sheet_name, xyxy):
        #병합된 것을 푸는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Range(xyxy).UnMerge()

    def swap(self, a, b):
        #a,b를 바꾸는 함수이다
        t = a
        a = b
        b = t
        return [a, b]

    def swap_cap_small(self, sheet_name, xyxy):
        #대소문자를 바꾸는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                temp_data = self.read_cell_value(sheet, [x, y])
                self.write_cell_value(sheet, [x, y], temp_data.swapcase())

    def swap_list_data(self, input_data):
        # input_data : [a, b, c, d]
        # result : [b, a, d, c]
        # 두개의 자료들에 대해서만 자리를 바꾸는 것이다
        result = []
        for one_data in range(int(len(input_data) / 2)):
            result.append(input_data[one_data * 2 + 1])
            result.append(input_data[one_data * 2])
        return result

    def write_cell_picture(self, sheet_name, xy, full_path):
        # 사진을 불러오는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        sheet.Cells(x1, y1).Select()
        aaa = sheet.Pictures
        aaa.Insert(full_path).Select()

    def write_cell_value(self, sheet_name, xy, value):
        # 값을 셀에 넣는다. (사용법) write_cell(시트이름, 행번호, 열번호, 넣을값)
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        sheet.Cells(x1, y1).Value = value

    def write_line_merge(self, sheet_name, xyxy):
        # 셀들을 합하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        if x1 == x2:
            sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Merge(0)
        else:
            for a in xyxy(y2 - y1 + 1):
                sheet.Range(sheet.Cells(y1 + a, x1), sheet.Cells(y1 + a, x2)).Merge(0)

    def write_range_clear(self, sheet_name, xyxy):
        # clear기능을 한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.ClearContents()

    def write_range_dump(self, sheet_name, xyxy, input_datas):
        # 영역에 값을 한번에 써 넣는 것이다
        # 차음시작하는 셀을 기준으로 알아서 맞추는 기능이다
        # 입력값과 영역이 맞지 않으면 입력값의 갯수를 더 우선함
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        y_len = len(input_datas[0])
        x_len = len(input_datas)
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x1+x_len-1, y1+y_len-1)).value = input_datas

    def write_range_list(self, sheet_name, xyxy, list_datas):
        # 2차원 리스트로 된 값을 영역에 쓰는 것이다
        self.write_range_value(sheet_name, xyxy, list_datas)

    def write_range_merge(self, sheet_name, xyxy):
        # 셀들을 합하는 것이다
        self.set_range_merge(sheet_name, xyxy)

    def write_range_name(self, sheet_name, xyxy, name):
        # 영역에 이름으로 설정하는 기능
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range  = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        self.xlBook.Names.Add(name, my_range)

    def write_range_value(self, sheet_name, xyxy, input_datas):
        # 영역에 값을 써 넣는 것이다
        # 이것은 각셀을 하나씩 쓰는 것이다
        # 입력값과 영역이 맞지 않으면 입력값의 갯수를 더 우선함
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)

        for x in range(len(input_datas)):
            for y in range(len(input_datas[x])):
                sheet.Range(sheet.Cells(x1+x, y1+y), sheet.Cells(x1+x, y1+y)).value = input_datas[x][y]

    def write_range_wrap(self, sheet_name, xyxy, input_data):
        # 셀의 줄바꿈을 설정할때 사용한다
        # 만약 status를 false로 하면 줄바꿈이 실행되지 않는다.
        sheet = self.check_sheet_name(sheet_name)
        sheet.Range(xyxy).WrapText = input_data

    #**************************** 테스트중
    #***************이것은 다시한번 확인해야 함
    def move_range_degree(self, datas, degree):
        # 리스트의 자료를 원하는 형태로 변경하는 것이다
        # 차후에 만들 예정
        degree = 1

