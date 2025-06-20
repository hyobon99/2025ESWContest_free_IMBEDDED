# 터치패드 캘리브레이션 GUI

라즈베리파이에서 터치패드와 빔프로젝터를 연결하여 사용하기 위한 PyQt5 기반 캘리브레이션 GUI 애플리케이션입니다.

## 기능

- **직관적인 GUI**: 사용자가 쉽게 캘리브레이션을 진행할 수 있는 시각적 인터페이스
- **4점 캘리브레이션**: 화면의 4개 모서리(좌상단, 우상단, 좌하단, 우하단)를 터치하여 정확한 매핑
- **실시간 터치 감지**: 별도 스레드에서 터치 이벤트를 실시간으로 감지
- **5초 타이머**: 각 포인트마다 5초 타이머로 사용자에게 명확한 안내
- **진행률 표시**: 현재 캘리브레이션 진행 상황을 시각적으로 표시
- **자동 완료**: 터치 감지 시 자동으로 다음 단계로 진행

## 시스템 요구사항

- 라즈베리파이 (Raspberry Pi OS 권장)
- Python 3.7 이상
- 40x30 터치 센서 배열
- 시리얼 통신 가능한 하드웨어

## 설치 방법

### 1. 자동 설치 (권장)

```bash
# 설치 스크립트 실행 권한 부여
chmod +x install_raspberry_pi.sh

# 설치 스크립트 실행
./install_raspberry_pi.sh
```

### 2. 수동 설치

```bash
# 시스템 패키지 업데이트
sudo apt-get update
sudo apt-get upgrade -y

# 필요한 패키지 설치
sudo apt-get install -y python3 python3-pip python3-venv
sudo apt-get install -y python3-pyqt5 python3-serial python3-numpy python3-matplotlib

# 가상환경 생성 및 활성화
python3 -m venv venv_calibration
source venv_calibration/bin/activate

# Python 패키지 설치
pip install -r requirements.txt

# 시리얼 포트 권한 설정
sudo usermod -a -G dialout $USER
```

## 사용 방법

### 1. 하드웨어 연결

1. 터치패드를 라즈베리파이의 USB 포트에 연결
2. 빔프로젝터를 라즈베리파이의 HDMI 포트에 연결
3. 라즈베리파이 전원 연결

### 2. 프로그램 실행

```bash
# 가상환경 활성화
source venv_calibration/bin/activate

# GUI 실행
python3 calibration_gui.py
```

### 3. 캘리브레이션 과정

1. **시작**: "캘리브레이션 시작" 버튼 클릭
2. **오프셋 보정**: 센서를 건드리지 않고 자동으로 오프셋 보정
3. **좌측 상단 터치**: 화면 좌측 상단을 터치 (5초 제한)
4. **우측 상단 터치**: 화면 우측 상단을 터치 (5초 제한)
5. **좌측 하단 터치**: 화면 좌측 하단을 터치 (5초 제한)
6. **우측 하단 터치**: 화면 우측 하단을 터치 (5초 제한)
7. **완료**: 캘리브레이션 완료 메시지 표시

## UI 구성 요소

### 메인 화면
- **제목**: "터치패드 캘리브레이션"
- **상태 메시지**: 현재 진행 상황 안내
- **타이머**: 5초 카운트다운 표시
- **진행률 바**: 전체 진행 상황 표시
- **캘리브레이션 포인트**: 4개 모서리 포인트 시각화
- **시작 버튼**: 캘리브레이션 시작

### 캘리브레이션 포인트 상태
- **회색**: 비활성 상태
- **주황색**: 현재 활성 상태 (터치 대기)
- **녹색**: 완료된 상태

## 파일 구조

```
velostat/
├── calibration_gui.py          # 메인 GUI 애플리케이션
├── Calibration_bytime_raspi.py # 기존 콘솔 버전
├── requirements.txt            # Python 패키지 목록
├── install_raspberry_pi.sh     # 라즈베리파이 설치 스크립트
├── README.md                   # 이 파일
├── clikmap_pc.py              # PC 버전 클릭맵
├── clikmap_raspi.py           # 라즈베리파이 버전 클릭맵
└── vel_control.ino            # 아두이노 제어 코드
```

## 문제 해결

### 시리얼 포트 연결 오류
```bash
# 시리얼 포트 권한 확인
ls -l /dev/ttyACM0

# 권한이 없다면 재부팅 후 다시 시도
sudo reboot
```

### PyQt5 설치 오류
```bash
# 시스템 패키지로 PyQt5 설치
sudo apt-get install -y python3-pyqt5 python3-pyqt5.qtcore python3-pyqt5.qtgui python3-pyqt5.qtwidgets
```

### 터치 감지가 안 될 때
1. 센서 연결 상태 확인
2. 시리얼 포트 번호 확인 (`/dev/ttyACM0` 또는 `/dev/ttyUSB0`)
3. 터치 임계값 조정 (코드에서 `TOUCH_THRESHOLD` 값 수정)

## 개발 정보

- **언어**: Python 3
- **GUI 프레임워크**: PyQt5
- **시리얼 통신**: pyserial
- **수치 계산**: numpy
- **터치 감지**: 커스텀 알고리즘 (행/열 최대값 교집합)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 