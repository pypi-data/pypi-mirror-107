import win32com.client
import io
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication
import pandas
import numpy

class KDHexcel:
    __version__ = "0.0.1.2"
    __작성자__ = "김대호"
    __버전__ = __version__

    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")  # 엑셀 어플리케이션 선언 """
        self.excel.Visible = True  # 엑셀 프로그램 보여지게 함 """

        if self.excel.Workbooks.Count == 0:  # 워크북 새로 만듦 """ # 없으면 새로 만듦
            self.wb = self.excel.Workbooks.Add()
        else:  # 있으면 마지막 엑셀 문서
            self.wb = self.excel.Workbooks(self.excel.Workbooks.Count)

    def _setSheet(self, 시트명=None):
        """ 시트명이 입력 되면 해당 시트 선택 없으면 시트생성, 시트명이 입력 되지 않으면 첫번째 시트명 리턴 """
        if 시트명 is None:
            self.ws = self.wb.Worksheets(1)
        else:
            try:
                self.ws = self.wb.Worksheets(시트명)
            except:
                self.ws = self.wb.Sheets.Add(self.wb.Sheets(self.wb.Sheets.Count))
                self.ws.Name = 시트명
        self.ws.Select()

    def 셀값넣기(self, 셀="A1", 값 = "1", 시트명 = None):
        """
        :param 셀 : 저장될 셀위치 (예 : B3)
        :param 값 : 셀에 들어갈 값 (1개의 값 또는 tuple, list, pandas.Dataframe, numpy.ndarray)
        :param 시트명 : 입력하면 해당 시트에 입력 안하면 첫번째 시트에 값이 들어감
        :return: 없음
        """

        self._setSheet(시트명)  # 해당 시트 선택 없으면 시트생성, 시트명을 안 넣으면 첫번재 시트 선택

        # 데이터프레임일 경우 리스트로 바꿔줌
        if type(값) == pandas.core.frame.DataFrame:
            t1 = 값.reset_index()
            c = [list(t1.columns)]
            for i in range(0, t1.shape[0]):
                c.append(list(t1.iloc[i]))
            값 = c
        elif type(값) == tuple:
            값 = list(값)

        # 리스트 일경우 반복해서 넣어 줌
        if type(값) == list or type(값) == numpy.ndarray:
            c = 1
            r = 1
            for v in 값:
                if type(v) == list or type(v) == numpy.ndarray:
                    c = 1
                    for v1 in v:
                        self.ws.Range(셀).Offset(r, c).Value = v1
                        c = c + 1
                    r = r +1
                else:
                    self.ws.Range(셀).Offset(r, c).Value = v
                    c = c + 1
        else:
            self.ws.Range(셀).Value = 값

    def 셀값지우기(self, 셀="A1", 시트명 = None):
        """
        :param 셀 : 지울 셀위치 (예 : B3, A1:B3)
        :param 시트명 : 입력하면 해당 시트에 입력 안하면 첫번째 시트에 값이 들어감
        :return: 없음
        """
        self._setSheet(시트명)  # 해당 시트 선택 없으면 시트생성, 시트명을 안 넣으면 첫번재 시트 선택
        self.ws.Range(셀).ClearContents()

    def 이미지파일넣기(self,셀, 파일명, ColumnWidth=50, RowHeight = 150, 시트명 = None):
        r"""
        :param 셀 : 저장될 셀위치 (예 : B3)
        :param 파일명: 이미지 파일명 (예 : 'C:\Users\User\파이썬주피터\plot3.png' )
        :param 시트명 : 입력하면 해당 시트에 입력 안하면 첫번째 시트에 값이 들어감
        :param ColumnWidth : 셀의 너비
        :param RowHeight : 셀의 높이
        :return: 없음
        """
        self._setSheet(시트명)  # 해당 시트 선택 없으면 시트생성, 시트명을 안 넣으면 첫번재 시트 선택

        self.ws.Columns(self.ws.Range(셀).Column).ColumnWidth = ColumnWidth
        self.ws.Rows(self.ws.Range(셀).Row).RowHeight = RowHeight

        L = self.ws.Range(셀).Left
        T = self.ws.Range(셀).Top
        W = self.ws.Range(셀).Width
        H = self.ws.Range(셀).Height

        self.ws.Shapes.AddPicture(파일명, False, True, L, T, W,H).Placement = 1

    def 그래프넣기(self,셀, plt, ColumnWidth=50, RowHeight = 150, 시트명=None):
        """ QApplication.clipboard 를 사용 주피터 노트북에서는 실행이 안됨
        :param 셀: 저장될 셀위치 (예 : B3)
        :param plt: 그래프 object (예 :  matplotlib.pyplot )
        :param 시트명 : 입력하면 해당 시트에 입력 안하면 첫번째 시트에 값이 들어감
        :param ColumnWidth : 셀의 너비
        :param RowHeight : 셀의 높이
        :return: 없음
        """
        self._setSheet(시트명)  # 해당 시트 선택 없으면 시트생성, 시트명을 안 넣으면 첫번재 시트 선택

        self.ws.Columns(self.ws.Range(셀).Column).ColumnWidth = ColumnWidth
        self.ws.Rows(self.ws.Range(셀).Row).RowHeight = RowHeight

        buf = io.BytesIO()
        plt.savefig(buf, format="svg")

        img = QImage.fromData(buf.getvalue())
        QApplication.clipboard().setImage(img)

        self.ws.Range(셀).Select()
        self.ws.Paste()

        cnt = self.ws.Shapes.Count
        self.ws.Shapes(cnt).LockAspectRatio = 0
        self.ws.Shapes(cnt).Height = self.ws.Range(셀).Height
        self.ws.Shapes(cnt).Width = self.ws.Range(셀).Width
        self.ws.Shapes(cnt).Placement = 1

