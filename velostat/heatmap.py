import serial
import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports

# 한글 폰트 설정 (Windows의 Malgun Gothic 사용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 사용 가능한 시리얼 포트 출력
ports = serial.tools.list_ports.comports()
print("Available serial ports:")
for p in ports:
    print(" •", p.device)

# Arduino 시리얼 포트와 전송 속도 설정 (실제 포트명으로 변경하세요)
ser = serial.Serial('COM10', 115200, timeout=1)

# 센서 배열 크기 설정 (40행 x 30열)
num_rows = 40
num_cols = 30

# 실시간 히트맵을 위한 설정
plt.ion()
fig, ax = plt.subplots()
im = ax.imshow(np.zeros((num_rows, num_cols)),
               cmap='hot', vmin=0, vmax=1023)
ax.set_title("40x30 벨로스탯 압력 센서 배열 (오프셋 보정 포함)")

def read_frame():
    """시리얼에서 num_rowsx num_cols 크기의 한 프레임을 읽어 리스트로 반환.
       빈 라인이나 숫자가 부족한 라인은 건너뜀."""
    frame = []
    while len(frame) < num_rows:
        line = ser.readline().decode('utf-8', 'ignore').strip()
        # 빈 문자열이나 쉼표만 있으면 건너뛰기
        if not line or set(line) <= {','}:
            continue
        # 끝 쉼표 제거
        if line.endswith(','):
            line = line[:-1]
        parts = line.split(',')
        # 길이나 숫자 변환 실패 시 건너뛰기
        if len(parts) != num_cols:
            continue
        try:
            vals = list(map(int, parts))
        except ValueError:
            continue
        frame.append(vals)
    return np.array(frame, dtype=np.float32)

# 오프셋 보정을 위한 초기 프레임 수집
print("오프셋 보정: 첫 10개 프레임 수집 중입니다 (센서를 건드리지 마세요).")
calibration = []
for _ in range(10):
    mat = read_frame()
    calibration.append(mat)
offset = np.mean(calibration, axis=0)
print("오프셋 보정 완료.")

# 메인 루프: 데이터 읽기 및 히트맵 업데이트 (blitting)
while True:
    try:
        frame = read_frame()
        corrected = np.clip(frame - offset, 0, None)
        im.set_data(corrected)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
    except Exception as e:
        print("실시간 업데이트 오류:", e)
