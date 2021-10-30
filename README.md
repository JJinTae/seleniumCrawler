# seleniumCrawler

## :page_with_curl: 프로젝트 설명
 웹크롤링으로 텍스트(한글) 데이터를 수집하여 분석하는 프로젝트입니다.

## 💬 Commit Message Rule
- Feat : 새로운 기능 추가
- Fix : 버그 수정
- Docs : 문서의 수정
- Style : (코드 수정 없이) 스타일(style)만 변경 (들여쓰기 같은 포맷이나 세미콜론을 빼먹은 경우)
- Refactor : 코드를 리펙토링
- Test : Test 관련한 코드의 추가, 수정
- Chore : (코드 수정 없이) 설정을 변경

## :sparkles: 개발 환경
| Tools | Version | Remarks |
| :------------: | :------------:| :------------:|
| Python | 3.8.11 | Anaconda3-2021.05 |
| Pycharm  | 2021.2.2 | Community Edition |

### pip
| Lib | Version | Remarks |
| :------------: | :------------:| :------------:|
| selenium | 3.141.0 |  |
| request | 2.26.0 |  |
| pandas | 1.3.3 | |
| konlpy | 0.5.2 | |
| Jpype | 1.1.2 | |
| openpyxl | 3.0.7 | |
| win32 | 228 | |


### 개발 환경 구축 메모

1. Anaconda 설치 - Anaconda3-2021.05
2. Pycharm - 2021.2.2 Community Edition<br>
 ![image](https://user-images.githubusercontent.com/46085058/135711889-ecdadfd6-9371-43e5-b9b5-19cb077344e8.png)
3. git clone (this repository)
4. **data_file** folder download & add<br>
 ![image](https://user-images.githubusercontent.com/46085058/135712523-80cd6e03-0af3-4167-8979-a62ed84578a2.png)
5. Install requirements.txt
6. Install JPype - matching python version 
   - www.lfd.uci.edu/~gohlke/pythonlibs/#jpype 
     - pip install JPype1‑1.1.2‑cp38‑cp38‑win_amd64.whl
7. Install ChromeDriver - matching chrome version
   - https://sites.google.com/a/chromium.org/chromedriver/downloads
   - download Chromedriver to /Scraper
8. HWP 한/글 오토메이션용 보안승인모듈 승인<br>
![image](https://user-images.githubusercontent.com/46085058/135719032-47fedd30-1035-4ac4-bf19-fea159e7b13c.png)
    1. C:/HNC/Automation_Module 폴더를 생성하고 다운 받은 zip 파일 내부의 모든 파일을 옮깁니다.
    2. 윈도우 regedit 실행 - HKEY_CURRENT_USER > SOFTWARE > HNC(또는 Hnc) > HwpAutomation > Modules 로 이동
    3. 내부에 HwpAutomation이 없는 경우 생성 : 상위 디렉터리(HNC 또는 Hnc) > 우클릭 > 새로 만들기 > 키(K) > HwpAutomation 입력
    4. 내부에 Modules가 없는 경우 생성 : 상위 디렉터리(HwpAutomation) > 우클릭 > 새로 만들기 > 키(K) > Modules 입력
    5. HwpAutomation > Moduels > 우측 공간에 우클릭 > 새로 만들기 > 문자열 값(S)
    6. 이름을 AutomationModule로 설정 후 우클릭 > 수정 > 값 데이터에 1번 단계에서 저장한 FilePathCheckerModuleExample.dll의 경로를 넣음 
