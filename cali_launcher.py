import subprocess
import sys
import os

def main():
    print("터치패드 시스템을 시작합니다...")
    
    # 1. 캘리브레이션 실행
    print("1단계: 터치패드 캘리브레이션을 시작합니다...")
    try:
        calibration_process = subprocess.run([sys.executable, 'calibration_gui.py'], 
                                           capture_output=True, text=True)
        
        if calibration_process.returncode == 0:
            print("캘리브레이션이 성공적으로 완료되었습니다!")
        else:
            print("캘리브레이션에 실패했습니다.")
            print("오류:", calibration_process.stderr)
            return
            
    except Exception as e:
        print(f"캘리브레이션 실행 중 오류 발생: {e}")
        return
    
    # 2. 게임 런처 실행
    print("2단계: 게임 런처를 시작합니다...")
    try:
        launcher_process = subprocess.run([sys.executable, 'launcher.py'],
                                        capture_output=True, text=True)
        
        if launcher_process.returncode == 0:
            print("게임 런처가 정상적으로 종료되었습니다.")
        else:
            print("게임 런처 실행 중 오류가 발생했습니다.")
            print("오류:", launcher_process.stderr)
            
    except Exception as e:
        print(f"런처 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main() 