// Velostat 센서 어레이 제어용 Arduino 코드 (40×30)
// • 5×8-bit Shift Register → 40개 행(Row) 제어
// • 4×8-ch MUX(CD4051) → 32개 열 중 앞 30개 열(Column) 선택
// • MUX Select 핀 3개는 공통, COM 핀은 A0~A3로 분리

// ─── 핀 정의 ─────────────────────────────────────────────
const int shiftDataPin  = 2;   // DS (시리얼 데이터 입력)
const int shiftClockPin = 3;   // SH_CP (클럭, 모든 SR에 병렬)
const int shiftLatchPin = 4;   // ST_CP (래치)

const int numShiftRegs = 5;    // 5 × 8 = 40개 행

// MUX 선택 핀 (S0, S1, S2) – 공통으로 물림
const int muxSelectPins[3] = {5, 6, 7};
const int numMuxBits       = 3;

// MUX 공통 출력(COM) – 각각 A0~A3에 연결
const int muxAnalogPins[] = {A0, A1, A2, A3};
const int numMuxDevices   = sizeof(muxAnalogPins) / sizeof(muxAnalogPins[0]);

const int numCols = 30;      // 실제로 읽을 열 개수 (4×8=32 중 앞 30개)
const int numRows = numShiftRegs * 8;  // 40

void setup() {
  Serial.begin(115200);
  pinMode(shiftDataPin,  OUTPUT);
  pinMode(shiftClockPin, OUTPUT);
  pinMode(shiftLatchPin, OUTPUT);
  for (int i = 0; i < numMuxBits; i++) {
    pinMode(muxSelectPins[i], OUTPUT);
  }
}

void loop() {
  // 각 행을 차례로 활성화
  for (int row = 0; row < numRows; row++) {
    selectRow(row);

    // 각 열(col)마다 MUX 채널 설정 → 모든 MUX의 COM에서 읽기
    int count = 0;
    for (int col = 0; col < 8; col++) {
      selectMux(col);
      delayMicroseconds(50);  // MUX 안정화

      4개의 MUX에서 값 읽기
    //   for (int dev = 0; dev < numMuxDevices; dev++) {
    //     // 전체 인덱스가 numCols 미만일 때만 출력
    //     if (count < numCols) {
    //       int val = analogRead(muxAnalogPins[dev]);
    //       Serial.print(val);
    //       Serial.print(',');  
    //     }
    //     count++;
    //   }
    // }
    // Serial.println();
      for (int dev = 0; dev < numMuxDevices; dev++) {
        if (count < numCols) {
          Serial.print(val);
          if (count < numCols-1) Serial.print(',');
        }
      }
    Serial.println();
  }
  delay(100);  // 약 10fps
}

// ─── 행 선택 (40비트 중 하나만 ‘1’) ──────────────────────
void selectRow(int row) {
  digitalWrite(shiftLatchPin, LOW);
  // 5바이트(5×8비트)만큼 보낼 데이터 계산
  for (int reg = 0; reg < numShiftRegs; reg++) {
    uint8_t b = 0;
    int startBit = reg * 8;
    if (row >= startBit && row < startBit + 8) {
      b = 1 << (row - startBit);
    }
    shiftOut(shiftDataPin, shiftClockPin, MSBFIRST, b);
  }
  digitalWrite(shiftLatchPin, HIGH);
  delayMicroseconds(10);  // 출력 안정화
}

// ─── MUX 채널 선택 (0~7) ────────────────────────────────
void selectMux(int channel) {
  for (int i = 0; i < numMuxBits; i++) {
    digitalWrite(muxSelectPins[i], (channel >> i) & 1);
  }
}
