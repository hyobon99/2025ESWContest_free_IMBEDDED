// Velostat 압력 센서 어레이 (8x8)를 위한 Arduino 코드
// 8채널 MUX와 8비트 Shift Register 사용

// 핀 정의
const int shiftDataPin = 2;
const int shiftClockPin = 3;
const int shiftLatchPin = 4;

// 8채널 MUX는 3비트 선택 사용 (예: CD4051 등)
const int muxSelectPins[] = {5, 6, 7};
const int muxAnalogPin = A0;

const int numRows = 8;
const int numCols = 8;
const int knownResistor = 10000; // 필요할 경우 사용 (10k 옴)

void setup() {
  Serial.begin(115200);
  
  pinMode(shiftDataPin, OUTPUT);
  pinMode(shiftClockPin, OUTPUT);
  pinMode(shiftLatchPin, OUTPUT);
  
  for (int i = 0; i < 3; i++) {
    pinMode(muxSelectPins[i], OUTPUT);
  }
}

void loop() {
  for (int row = 0; row < numRows; row++) {
    selectRow(row);
    for (int col = 0; col < numCols; col++) {
      selectMux(col);
      delayMicroseconds(50); // 채널 안정화를 위해 잠시 대기
      int val = analogRead(muxAnalogPin);
      Serial.print(val);
      if (col < numCols - 1) {
        Serial.print(",");
      }
    }
    Serial.println();
  }
  delay(100); // 약 10fps로 데이터 출력
}

void selectRow(int row) {
  digitalWrite(shiftLatchPin, LOW);
  // row 0이 실제 상단 행과 매칭되도록 순서를 반전시킵니다.
  shiftOut(shiftDataPin, shiftClockPin, MSBFIRST, 1 << (numRows - 1 - row));
  digitalWrite(shiftLatchPin, HIGH);
  delayMicroseconds(10);  // 선택 후 안정화 딜레이
}

void selectMux(int col) {
  // MUX 채널 선택: 0 ~ 7 (3비트)
  for (int i = 0; i < 3; i++) {
    digitalWrite(muxSelectPins[i], (col >> i) & 1);
  }
}