# pyside6-uic ui/mainwindow.ui -o ui/mainwindow.py
import sys
from enum import IntEnum
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from ui.mainwindow import Ui_MainWindow
from core.game import GameManager

class Page(IntEnum):
    MAIN       = 0
    GAME_LIST  = 1
    CHAR_LIST  = 2
    MAKE_CHAR  = 3
    PLAY_MAP   = 4
    FIGHT_PAGE = 5

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # OOP 구조: GameManager 인스턴스
        self.manager = GameManager('games.json')
        self.current_game = None

        # 시작 화면을 MAIN으로
        self.switch_page(Page.MAIN)

        # 시그널 연결
        self.ui.p1_to_p2_btn.clicked.connect(lambda: self.switch_page(Page.GAME_LIST))
        self.ui.p2_to_p1_btn.clicked.connect(lambda: self.switch_page(Page.MAIN))
        self.ui.p3_to_p2_btn.clicked.connect(lambda: self.switch_page(Page.GAME_LIST))

        self.ui.p2_make_game_btn.clicked.connect(self.on_new_game)
        self.ui.p2_del_game_btn.clicked.connect(self.on_delete_game)
        self.ui.p2_game_list.itemDoubleClicked.connect(self.on_select_game)

        # p3/p4 텍스트 초기화
        self.ui.p3_text_gamename.clear()
        self.ui.p4_text_gamename.clear()

        # 게임 리스트 표시
        self.refresh_game_list()

    def switch_page(self, page: Page):
        self.ui.stack_page.setCurrentIndex(page.value)

    def refresh_game_list(self):
        self.ui.p2_game_list.clear()
        for game in self.manager.games:
            item = QListWidgetItem(game.display_text)
            self.ui.p2_game_list.addItem(item)

    def on_new_game(self):
        game = self.manager.add_game()
        self.ui.p2_game_list.addItem(QListWidgetItem(game.display_text))

    def on_delete_game(self):
        row = self.ui.p2_game_list.currentRow()
        if row >= 0:
            self.manager.delete_game(row)
            self.refresh_game_list()

    def on_select_game(self, item: QListWidgetItem):
        row = self.ui.p2_game_list.row(item)
        self.current_game = self.manager.games[row]
        text = self.current_game.display_text
        # QLabel일 경우 setText, QTextEdit/QTextBrowser일 경우 setPlainText or setText
        self.ui.p3_text_gamename.setText(text)
        self.ui.p4_text_gamename.setText(text)
        self.switch_page(Page.CHAR_LIST)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
