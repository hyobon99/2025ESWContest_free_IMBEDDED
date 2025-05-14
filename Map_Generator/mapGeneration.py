import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPen
import os

# app.py에서 맵 생성 로직 import
import app  # app.py에서 함수 가져오기

class MapGeneratorWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Polytopia Map Generator")
        self.setGeometry(100, 100, 800, 800)  # 창 크기 설정

        self.map_size = 16
        self.world_map = [{'type': 'ocean', 'above': None, 'road': False, 'tribe': 'Xin-xi'} for i in range(self.map_size ** 2)]
        
        # app.py의 generate_map 함수로 맵 생성
        self.generate_map()

        layout = QVBoxLayout()
        self.generate_button = QPushButton("Generate Map")
        self.generate_button.clicked.connect(self.generate_map)
        self.label = QLabel(self)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def generate_map(self):
        app.generate_map(self.world_map, self.map_size, initial_land=0.5, smoothing=3, relief=4, tribes=['Vengir', 'Bardur', 'Oumaji'])
        self.update()  # 맵을 새로 그리기 위해 화면 갱신

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        tile_size = 50  # 타일 크기 설정

        # 현재 실행 중인 Python 파일의 경로를 기준으로 상대경로 설정
        assets_path = os.path.join(os.path.dirname(__file__), 'assets')  # 현재 디렉토리 -> assets 폴더

        for row in range(self.map_size):
            for column in range(self.map_size):
                # 각 셀의 위치 계산
                x = column * tile_size
                y = row * tile_size
                tile = self.world_map[row * self.map_size + column]

                # 부족 이름 가져오기
                tribe = tile['tribe']
                tile_type = tile['type']

                # 이미지 경로 생성
                try:
                    if tile_type == 'ground':
                        image_path = os.path.join(assets_path, tribe, 'Ai-mo ground.png')
                    elif tile_type == 'forest':
                        image_path = os.path.join(assets_path, tribe, 'Ai-mo forest.png')
                    elif tile_type == 'mountain':
                        image_path = os.path.join(assets_path, tribe, 'Ai-mo mountain.png')
                    elif tile_type == 'water':
                        image_path = os.path.join(assets_path, tribe, 'Ai-mo game.png')
                    elif tile_type == 'ocean':
                        image_path = os.path.join(assets_path, tribe, 'Ai-mo city 1.png')  # 예시: ocean에 대한 이미지 사용

                    # 이미지 불러오기
                    pixmap = QPixmap(image_path)

                    # 이미지가 로드되지 않으면 기본 배경을 설정
                    if pixmap.isNull():
                        pixmap = QPixmap(tile_size, tile_size)
                        pixmap.fill(QColor(255, 255, 255))  # 흰색 배경

                    # 이미지 크기 맞추기
                    pixmap = pixmap.scaled(tile_size, tile_size)

                    # 이미지를 타일에 그리기
                    painter.drawPixmap(x, y, pixmap)

                except Exception as e:
                    print(f"Error loading image: {e}")
                    pixmap = QPixmap(tile_size, tile_size)
                    pixmap.fill(QColor(255, 0, 0))  # 에러 시 빨간색으로 표시

                # 마을 또는 수도 표시
                if tile['above'] == 'village':
                    painter.setPen(QPen(QColor(255, 215, 0), 3))
                    painter.drawEllipse(x + tile_size // 4, y + tile_size // 4, tile_size // 2, tile_size // 2)
                elif tile['above'] == 'capital':
                    painter.setPen(QPen(QColor(255, 0, 0), 3))
                    painter.drawRect(x + tile_size // 4, y + tile_size // 4, tile_size // 2, tile_size // 2)

        painter.end()




def main():
    app = QApplication(sys.argv)
    window = MapGeneratorWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
