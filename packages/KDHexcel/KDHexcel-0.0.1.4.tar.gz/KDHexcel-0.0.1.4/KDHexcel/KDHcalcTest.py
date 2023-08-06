import pandas as pd
from KDHexcel import KDHcalc
import os.path as path
# 재무데이터 로드
jemu_file = './jemu.csv'
jemu_file =  path.join(path.dirname(__file__),'data/jemu.csv')

df = pd.read_csv(jemu_file, index_col=0)

# 한개 업체만 선택
try:
    upche = df.loc[int('380725')]
except KeyError:
    try:
        upche = df.loc['380725']
    except KeyError:
        print("해당하는 업체가 없습니다.")
        sys.exit()

# 산식처리 클래스 선언
calc = KDHcalc.KDHcalcClass()

# 단건
fmul = '&11-1000C&+(&11-2000B&)+100'
a = calc.calc(upche,fmul,20201231,20191231,20181231)
print('단건 => ',a,'\n','-'*50)

# 산식을 값으로 변경한 결과
fmul = 'if(or(&11-9000C&>0,&11-9000B&<0),max(log(3,2),1),&11-9000C&)'
a = calc.calc(upche,fmul,20201231,20191231,20181231,'n')
print('산식을 값으로 변경한 결과 => ',a,'\n','-'*50)

# 산식 설정 : 스트링을 csv 파일처럼 인식하여 로드 함
from io import StringIO
csv_data = \
    '''bogosu|hang|fmul
    19|1000|if(&11-2000C&<0,1,&11-9000B&)
    19|2000|&11-9000C&
    19|3000|&11-9000B&
    19|1000|if(or(&11-9000C&<0,&11-9000B&<0,&11-9000B&<0),max(log(3,2),1),&11-9000C&)
    19|1000|if(and(&11-9000C&<0,&11-9000B&<0),1,100)'''
df = pd.read_csv(StringIO(csv_data), sep="|")


# 계산 하여 amt 컬럼에 넣어 줌 : 한꺼번에 처리
df['amt'] = df['fmul'].apply(lambda fmul : calc.calc(upche, fmul, '20201231', 20191231, 20181231))
# 산식 컬럼을 삭제
del df['fmul']

## 계산 하여 amt 컬럼에 넣어 줌 : for 루프로 단건씩 처리
# for i in range(0,df['fmul'].count()) :
#     df['amt'][i] = calc.calc(upche,df['fmul'][i],'20201231',20191231,20181231)
# del df['fmul'] # 컬럼을 삭제

print(df.head())

# # 엑셀 파일로 저장
# pdE = pd.ExcelWriter('result1.xlsx')
# df.to_excel(pdE)
# pdE.save()
