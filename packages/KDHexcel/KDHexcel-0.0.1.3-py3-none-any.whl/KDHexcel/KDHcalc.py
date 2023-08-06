import pandas
import math

class KDHcalcClass:

    def calc(self, upche, fmul, dateC, dateB, dateA, option: str = 'y'):
        """ 산식을 계산해 줌
            산식의 &00-0000C& 를 금액으로 치환해서 계산해줌
        """
        fmul = fmul.lower()
        fmul = fmul.replace('if', 'self.KDHif')
        fmul = fmul.replace('or', 'self.KDHor')
        fmul = fmul.replace('and', 'self.KDHand')
        fmul = fmul.replace('=', '==')
        fmul = fmul.replace('<==', '<=')
        fmul = fmul.replace('>==', '>=')
        fmul = fmul.replace('log', 'math.log')
        fmul = fmul.replace('exp', 'math.exp')
        fmul = fmul.replace('log10', 'math.log10')
        fmul = fmul.replace('pow', 'math.pow')
        fmul = fmul.replace('sqrt', 'math.sqrt')

        cnt = fmul.count('&') % 2
        if cnt != 0 :
            return "& 개수가 홀수 입니다.[" + fmul + "]"

        cnt = fmul.count('(') - fmul.count(')')
        if cnt != 0:
            return "괄호의 개수가 맞지 않습니다.[" + fmul + "]"

        for i in range(1, 1000):
            st = fmul.find('&')
            ed = fmul.find('&', st + 1) + 1

            if st < 0:
                # print('fmul=', fmul)
                break

            acc = fmul[st:ed]
            bogosu = acc[1:3]
            hang = acc[4:8]
            klgubn = acc[8:9]
            klgubn = klgubn.upper()
            if klgubn == 'C':
                selDate = dateC
            elif klgubn == 'B':
                selDate = dateB
            elif klgubn == 'A':
                selDate = dateA
            else:
                selDate = dateC

            amt = self.getValue(upche, selDate, bogosu, hang)
            fmul = fmul.replace(acc, str(amt))

        """ eval 을 이용해서 계산함
            제수가 0 일경우 0 리턴 
        """

        if option != 'y' :  # 옵션값 체크 해서 숫자로 변경된 산식을 리턴함
            return fmul

        try :
            revalue = eval(fmul)
            return revalue
        except ZeroDivisionError:
            return 0


    def KDHif(self,TrueFalse,x,y):
        """ if 문 처리
            TrueFalse : True, False
            x : TrueFalse == True 일경우 리턴될 값
            y : TrueFalse == False 일경우 리턴될 값
        """
        if TrueFalse :
            return x
        else :
            return y

    def KDHor(self, *args):
        """ or 처리 : KDHor(1!=1,2!=2, True)
        """
        re = args[0]
        for arg in args:
            if arg:
                re = True
        return re

    def KDHand(self, *args):
        """ and 처리 : KDHand(1!=1,2!=2, True) """
        re = args[0]
        for arg in args:
            if (re) and (arg):
                re = True
            else:
                re = False
        return re

    def getValue(self, upche, date, bogosu, hang):
        """ 조건에 맞는 1개의 값을 리턴 해줌
            데이터프레임의 값이 숫자일수도 문자일 수도 있어서 or 처리 함.
            해당 계정이 없을 때 0을 리턴해줌
        """
        a = upche[((upche['date'] == int(date)) | (upche['date'] == str(date)) ) & ((upche['bogosu'] == int(bogosu)) | (upche['bogosu'] == str(bogosu))) & ((upche['hang'] == int(hang)) | (upche['hang'] == str(hang))) ]
        if len(a) == 0 :
            return 0
        else :
            return a.amt.values[0]

