import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QMainWindow, QStackedWidget, QTextEdit
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

class GameCard(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # 썸네일 이미지
        self.thumbnail = QLabel(self)
        pixmap = QPixmap(self.game["thumbnail"])
        if pixmap.isNull():
            pixmap = QPixmap(200, 150)
            pixmap.fill(Qt.gray)
        else:
            pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.thumbnail.setPixmap(pixmap)
        self.thumbnail.setAlignment(Qt.AlignCenter)
        self.thumbnail.setCursor(QCursor(Qt.PointingHandCursor))
        self.thumbnail.mousePressEvent = self.launch_game

        # hover 효과
        self.thumbnail.setStyleSheet("""
            QLabel {
                border: 2px solid transparent;
                border-radius: 8px;
            }
            QLabel:hover {
                border: 2px solid #00BFFF;
            }
        """)

        # 게임 이름
        name_label = QLabel(self.game["name"])
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        # 게임 설명 (스크롤 가능한 텍스트 박스)
        desc_box = QTextEdit()
        desc_box.setText(self.game.get("description", ""))
        desc_box.setReadOnly(True)
        desc_box.setFixedSize(200, 60)
        desc_box.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        desc_box.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 11px;
                color: #555555;
            }
        """)

        layout.addWidget(self.thumbnail)
        layout.addSpacing(5)
        layout.addWidget(name_label)
        layout.addSpacing(5)
        layout.addWidget(desc_box)

        self.setLayout(layout)
        self.setFixedSize(220, 340)

    def launch_game(self, event):
        script_path = os.path.abspath(self.game["path"])
        game_dir = os.path.dirname(script_path)
        print(f"Launching {script_path} in {game_dir}")
        subprocess.Popen(["python3", script_path], cwd=game_dir)


class GameLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("게임 런처")
        self.setGeometry(100, 100, 800, 600)
        self.current_page = 0
        self.games_per_page = 3
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.stacked_widget = QStackedWidget()

        self.quit_btn = QPushButton("종료")
        self.quit_btn.clicked.connect(self.close)
        self.quit_btn.setFixedWidth(80)

        self.prev_btn = QPushButton("이전")
        self.prev_btn.clicked.connect(self.prev_page)

        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignCenter)

        self.next_btn = QPushButton("다음")
        self.next_btn.clicked.connect(self.next_page)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.page_label)
        nav_layout.addWidget(self.next_btn)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.quit_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.stacked_widget)
        main_layout.addLayout(nav_layout)

        central_widget.setLayout(main_layout)

        self.load_games()
        self.create_pages()
        self.update_page()

    def load_games(self):
        self.games = []
        games_root = "games"

        if not os.path.exists(games_root):
            return

        for game_dir in os.listdir(games_root):
            game_path = os.path.join(games_root, game_dir)
            if os.path.isdir(game_path):
                script_path = os.path.join(game_path, "app.py")
                if not os.path.exists(script_path):
                    continue  # app.py 없으면 스킵

                thumb_files = [f for f in os.listdir(game_path) if f.lower().endswith((".jpg", ".png"))]
                if thumb_files:
                    thumbnail = os.path.join(game_path, thumb_files[0])
                else:
                    thumbnail = ""

                desc_path = os.path.join(game_path, "description.txt")
                description = ""
                if os.path.exists(desc_path):
                    with open(desc_path, "r", encoding="utf-8") as f:
                        description = f.read().strip()

                self.games.append({
                    "name": game_dir,
                    "path": script_path,
                    "thumbnail": thumbnail,
                    "description": description
                })

    def clear_stacked_widget(self):
        while self.stacked_widget.count():
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()

    def create_pages(self):
        self.pages = []
        self.clear_stacked_widget()

        for i in range(0, len(self.games), self.games_per_page):
            page_games = self.games[i:i+self.games_per_page]

            page_widget = QWidget()
            grid = QGridLayout()
            grid.setSpacing(30)
            grid.setAlignment(Qt.AlignCenter)

            for j, game in enumerate(page_games):
                card = GameCard(game)
                grid.addWidget(card, j // 3, j % 3)

            page_widget.setLayout(grid)
            self.stacked_widget.addWidget(page_widget)
            self.pages.append(page_widget)

    def update_page(self):
        self.stacked_widget.setCurrentIndex(self.current_page)
        total_pages = len(self.pages)
        self.page_label.setText(f"{self.current_page + 1} / {total_pages}")

        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < total_pages - 1)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.update_page()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = GameLauncher()
    launcher.show()
    sys.exit(app.exec_())
