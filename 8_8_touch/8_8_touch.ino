#include <Arduino.h>
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
  Serial.begin(115200); // 통신 속도는 유지, 데이터 포맷만 변경
  pinMode(shiftDataPin,  OUTPUT);
  pinMode(shiftClockPin, OUTPUT);
  pinMode(shiftLatchPin, OUTPUT);
  for (int i = 0; i < numMuxBits; i++) {
    pinMode(muxSelectPins[i], OUTPUT);
  }

  // ADC Prescaler 변경 (기본값 128 -> 16)
  // ADCSRA (ADC Control and Status Register A)
  // ADPS2, ADPS1, ADPS0: ADC Prescaler Select Bits
  // 0b111 (128), 0b110 (64), 0b101 (32), 0b100 (16)
  // 16MHz / 16 = 1MHz ADC clock. 13 cycles for conversion = ~13µs.
  ADCSRA &= ~((1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0)); // 현재 설정된 prescaler 비트 클리어
  ADCSRA |= (1 << ADPS2); // ADPS2 = 1, ADPS1 = 0, ADPS0 = 0 (Prescaler 16)
}

void loop() {
  // 프레임 시작 표시
  Serial.write(0xFF);
  
  // 각 행을 차례로 활성화
  for (int row = 0; row < numRows; row++) {
    selectRow(row);
    int count = 0;

    for (int col = 0; col < 8; col++) {
      selectMux(col); //MUX 신호 선택
      delayMicroseconds(50);  // MUX 안정화 시간
      //선택된 MUX신호에서, MUX의 신호를 읽어들임, ex> 1 9 17의 순서로 읽는 느낌
      for (int dev = 0; dev < numMuxDevices; dev++) {
        unsigned char val_byte = analogRead(muxAnalogPins[dev]) >> 2; // 0-1023 값을 0-255 값으로 변환
        Serial.write(val_byte); // 변환된 1바이트 값을 바이너리로 전송
      }
      if (count >= numCols) break; 
    }
  }
  // 프레임 간 약간의 지연 추가
  delay(5);
}

// ─── 행 선택 (40비트 중 하나만 '1') ──────────────────────
void selectRow(int row) {
  digitalWrite(shiftLatchPin, LOW);
  // 5바이트(5×8비트)만큼 보낼 데이터 계산
  for (int reg = 0; reg < numShiftRegs; reg++) {
    uint8_t b = 0;
    int startBit = reg * 8;
    if (row >= startBit && row < startBit + 8) {
      b = 1 << (row - startBit);
    }
    shiftOut(shiftDataPin, shiftClockPin, LSBFIRST, b);
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
