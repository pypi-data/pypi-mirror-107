from KDHexcel import KDHexcel

exc = KDHexcel.KDHexcel()

help(exc.셀값넣기)
help(exc.이미지파일넣기)
help(exc.그래프넣기)
help(exc.셀값지우기)

# 직접 VBA 코드를 이용할 수 있음 (exc.excel 이 엑셀 application 임)
exc.excel.Activesheet.Range("A1").Value = 15

# 첫번째 시트에 1개의 값 넣어줌
exc.셀값넣기(셀="A1", 값="첫번째시트")

# 테스트 시트에 1개의 값 넣어줌
exc.셀값넣기(셀="A1", 값="abcdef", 시트명="테스트")
exc.셀값넣기("B1",5.15,"테스트")

# 튜플 시트에 tuple 데이터 넣어줌
t1 = ("튜플a","튜플b","튜플c","튜플d")
exc.셀값넣기("B3",t1,"튜플")

# 리스트11 시트에 list 데이터 넣어줌
l1 = ["리스트1","리스트2","리스트3"]
exc.셀값넣기("A3",l1,"리스트11")

# 리스트2 시트에 2차원 list 데이터 넣어줌
l2 = [ ["리스트21","리스트22","리스트23"],
       ["리스트1","리스트2","리스트3"],
     ]
exc.셀값넣기("A1",l2,"리스트2")

# pandas 데이터셋 넣어줌
import pandas as pd
a = [["a1","b1"],["c1","d1"]]
p1 = pd.DataFrame(a, index=list('ab'), columns=list('de'))
exc.셀값넣기("A1",p1,"판다스")

# numpy array 넣어줌
import numpy as np
lst1 = [1, 2, 3, 4, 5, 6]
넘파이 = np.array(lst1)
exc.셀값넣기("a1",넘파이,"넘파이")

lst2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
넘파이 = np.array(lst2)
exc.셀값넣기("b3",넘파이,"넘파이")

# 이미지파일 넣어줌
exc.이미지파일넣기("d4", 시트명="이미지", 파일명=r"C:\Users\User\파이썬주피터\plot3.png",ColumnWidth=50, RowHeight=150)

# matplotlib.pyplot 넣어줌
import matplotlib.pyplot as plt
# 샘플그래프 그리기 시작
import numpy as np
a = np.random.normal(size=50)
plt.hist(a, bins=5)
# 샘플그래프 그리기 끝

exc.그래프넣기("f8",plt,ColumnWidth=30, RowHeight= 130, 시트명="그래프")

a = [[1,2],[2,4],[3,3]]
p1 = pd.DataFrame(a, index=list('abc'), columns=list('de'))
p1.plot.line(x='d',y='e')

exc.그래프넣기("a1",plt,ColumnWidth=30, RowHeight= 130, 시트명="그래프")

exc.셀값넣기(셀="A1", 값=[1,2,3,4,5,6], 시트명="셀값지우기")
exc.셀값지우기(셀="B1:D1", 시트명="셀값지우기")

