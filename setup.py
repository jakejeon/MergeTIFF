from distutils.core import setup
import py2exe

setup(
    windows=[{'script': 'MultiFileProcessor.py'}], # 변환할 스크립트 파일 이름
    # console=['MultiFileProcessor.py'], # 변환할 스크립트 파일 이름
    options={
        'py2exe': {
            'bundle_files': 1, # 모든 종속성 라이브러리를 단일 exe에 포함
            'compressed': True, # 바이트 코드를 압축하여 exe 파일 크기 줄임
            'optimize': 2, # 최적화 플래그 (0 = 최소, 1 = 일반, 2 = 전체)
        }
    },
    py_modules=['MergeTIFF', 'MultiFileProcessor', 'strategy'],
    zipfile=None
)