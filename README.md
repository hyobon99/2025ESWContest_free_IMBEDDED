# TRPG Game

간단한 텍스트 기반 TRPG(테이블탑 롤플레잉 게임) 관리용 데스크탑 애플리케이션입니다.  
PySide6를 사용한 Qt GUI로, 게임(세션) 생성·삭제, 캐릭터 등록·선택, 맵·전투 화면 전환 등의 기본 기능을 제공(할 예정정)

## 폴더 구조

project_root/
├── data/
│ └── games.json # 생성된 게임 세션 정보 저장 파일
├── core/
│ └── game_manager.py # Game, GameManager 클래스 (도메인 로직)
├── gui/
│ └── main_window.py # MainWindow 클래스 (화면 전환, 시그널 연결)
├── ui/
│ ├── mainwindow.ui # Qt Creator 로 만든 .ui 파일 (GPL-3.0)
│ └── mainwindow.py # pyside6-uic 로 생성된 UI 파이썬 모듈
├── tests/ # (선택) 단위 테스트 모듈
├── main.py # 진입점 (python main.py 로 실행)
├── requirements.txt # 의존 패키지 목록
└── README.md # 프로젝트 설명 문서


## 주요 파일 역할

- **main.py**  
  애플리케이션 진입점.  
  ```bash
  $ python main.py


ui/
.ui 파일은 Qt Creator로 디자인했으며, GNU GPL-3.0 라이선스를 따릅니다. - https://www.gnu.org/licenses/gpl-3.0.html
프로그램 실행 전 반드시 아래 명령으로 파이썬 UI 모듈을 생성해야 합니다.
$ pyside6-uic ui/mainwindow.ui -o ui/mainwindow.py
core/game_manager.py
게임 세션(생성시간 기반)의 로드·저장·추가·삭제 비즈니스 로직 담당.

gui/main_window.py
core와 ui를 연결하여 실제 창을 띄우고, 사용자 입력(버튼·리스트 클릭) 처리를 담당.

data/games.json
실행 시 동적으로 생성되는 게임 세션 정보를 보관하는 JSON 파일.

