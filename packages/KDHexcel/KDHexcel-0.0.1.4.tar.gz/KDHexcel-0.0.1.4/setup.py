from setuptools import setup, find_packages
setup(name='KDHexcel',
      version='0.0.1.4',
      description='엑셀생성',
      author='김대호',
      author_email='jmee2626@gmail.com',
      url='https://github.com/KimDaeHo26/python',
      license='MIT',
      # py_modules=['KDHexcel'],
      python_requires='>=3',
      packages=['KDHexcel'],
      # install_requires = [ ], # 해당 라이브러리를 사용하기 위해서 인스톨 되야하는 dependency들
      # packages=find_packages(exclude=('tests', 'docs')),  # 빌드에 포함들 package들 (exclude : 제외할 package)
      # executables=[Executable("./mypkg/gui_app.py", base=base)],
      # data_files=[('icons', ["./icons/add.png", "./icons/import.png"]),
      #           ('config', ["./config/mycfg.json"])],

      # options={'build_exe': {'include_files': ['./KDHexcel/jemu.csv']}},
      # include_files= ['./KDHexcel/jemu.csv']
      # data_files=[('docs', ["./KDHexcel/jemu.csv"])],
      # data_files=[('docs', ["./KDHexcel/jemu.csv"])],
      package_data={'KDHexcel': ['data/*.csv']}
)
# setup(name='KDHexcel',
#       # 프로젝트 명을 입력합니다.
#       version='0.0.1',
#       # 프로젝트 버전을 입력합니다.
#       url='https://github.com/KimDaeHo26/python',
#       # 홈페이지 주소를 입력합니다.
#       author='김대호',
#       # 프로젝트 담당자 혹은 작성자를 입력합니다.
#       author_email='jmee2626@gmail.com',
#       # 프로젝트 담당자 혹은 작성자의 이메일 주소를 입력합니다.
#       description='엑셀파일 생성',
#       # 프로젝트에 대한 간단한 설명을 입력합니다.
#       # packages=find_packages(exclude=['tests']),
#       # 기본 프로젝트 폴더 외에 추가로 입력할 폴더를 입력합니다.
#       long_description=open('README.md').read(),
#       # 프로젝트에 대한 설명을 입력합니다. 보통 README.md로 관리합니다.
#       long_description_content_type='text/markdown',
#       # 마크다운 파일로 description를 지정했다면 text/markdown으로 작성합니다.
#       install_requires=['win32com'],
#       # 설치시 설치할 라이브러리를 지정합니다.
#       zip_safe=False,
#       classifiers=[
#           'License :: OSI Approved :: MIT License'
#       ]
#       # 기본적으로 LICENSE 파일이 있다고 하더라도 명시적으로 적어 놓는 것이 좋습니다.
# )
