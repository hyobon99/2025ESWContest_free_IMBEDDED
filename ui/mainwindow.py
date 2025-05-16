# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLayout,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTextBrowser, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(800, 0))
        self.verticalLayout_12 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.stack_page = QStackedWidget(self.centralwidget)
        self.stack_page.setObjectName(u"stack_page")
        self.main = QWidget()
        self.main.setObjectName(u"main")
        self.verticalLayout_5 = QVBoxLayout(self.main)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.p1_text_title = QTextEdit(self.main)
        self.p1_text_title.setObjectName(u"p1_text_title")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(50)
        sizePolicy1.setHeightForWidth(self.p1_text_title.sizePolicy().hasHeightForWidth())
        self.p1_text_title.setSizePolicy(sizePolicy1)
        self.p1_text_title.setMaximumSize(QSize(16777215, 50))
        self.p1_text_title.setAutoFillBackground(True)
        self.p1_text_title.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.p1_text_title)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout_3.addItem(self.verticalSpacer)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.p1_to_p2_btn = QPushButton(self.main)
        self.p1_to_p2_btn.setObjectName(u"p1_to_p2_btn")

        self.verticalLayout_4.addWidget(self.p1_to_p2_btn)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.stack_page.addWidget(self.main)
        self.gamelist = QWidget()
        self.gamelist.setObjectName(u"gamelist")
        self.horizontalLayout_2 = QHBoxLayout(self.gamelist)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.p2_text_pagename = QTextEdit(self.gamelist)
        self.p2_text_pagename.setObjectName(u"p2_text_pagename")
        self.p2_text_pagename.setEnabled(True)
        self.p2_text_pagename.setMaximumSize(QSize(16777215, 20))
        self.p2_text_pagename.setReadOnly(True)
        self.p2_text_pagename.setAcceptRichText(True)

        self.verticalLayout_6.addWidget(self.p2_text_pagename)

        self.p2_game_list = QListWidget(self.gamelist)
        self.p2_game_list.setObjectName(u"p2_game_list")

        self.verticalLayout_6.addWidget(self.p2_game_list)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.p2_make_game_btn = QPushButton(self.gamelist)
        self.p2_make_game_btn.setObjectName(u"p2_make_game_btn")

        self.verticalLayout_8.addWidget(self.p2_make_game_btn)

        self.p2_del_game_btn = QPushButton(self.gamelist)
        self.p2_del_game_btn.setObjectName(u"p2_del_game_btn")

        self.verticalLayout_8.addWidget(self.p2_del_game_btn)

        self.p2_to_p1_btn = QPushButton(self.gamelist)
        self.p2_to_p1_btn.setObjectName(u"p2_to_p1_btn")

        self.verticalLayout_8.addWidget(self.p2_to_p1_btn)


        self.horizontalLayout_2.addLayout(self.verticalLayout_8)

        self.stack_page.addWidget(self.gamelist)
        self.charlist = QWidget()
        self.charlist.setObjectName(u"charlist")
        self.horizontalLayout = QHBoxLayout(self.charlist)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.p3_text_gamename = QTextEdit(self.charlist)
        self.p3_text_gamename.setObjectName(u"p3_text_gamename")
        self.p3_text_gamename.setMaximumSize(QSize(16777215, 20))
        self.p3_text_gamename.setReadOnly(True)

        self.verticalLayout_7.addWidget(self.p3_text_gamename)

        self.p3_text_pagename = QTextBrowser(self.charlist)
        self.p3_text_pagename.setObjectName(u"p3_text_pagename")
        self.p3_text_pagename.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_7.addWidget(self.p3_text_pagename)

        self.p3_char_list = QListWidget(self.charlist)
        self.p3_char_list.setObjectName(u"p3_char_list")

        self.verticalLayout_7.addWidget(self.p3_char_list)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.p3_make_char_btn = QPushButton(self.charlist)
        self.p3_make_char_btn.setObjectName(u"p3_make_char_btn")

        self.verticalLayout_2.addWidget(self.p3_make_char_btn)

        self.p3_to_p2_btn = QPushButton(self.charlist)
        self.p3_to_p2_btn.setObjectName(u"p3_to_p2_btn")

        self.verticalLayout_2.addWidget(self.p3_to_p2_btn)

        self.p3_play_btn = QPushButton(self.charlist)
        self.p3_play_btn.setObjectName(u"p3_play_btn")

        self.verticalLayout_2.addWidget(self.p3_play_btn)

        self.p3_del_char_btn = QPushButton(self.charlist)
        self.p3_del_char_btn.setObjectName(u"p3_del_char_btn")

        self.verticalLayout_2.addWidget(self.p3_del_char_btn)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.stack_page.addWidget(self.charlist)
        self.makechar = QWidget()
        self.makechar.setObjectName(u"makechar")
        self.verticalLayout_3 = QVBoxLayout(self.makechar)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.p4_text_gamename = QTextEdit(self.makechar)
        self.p4_text_gamename.setObjectName(u"p4_text_gamename")
        self.p4_text_gamename.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_9.addWidget(self.p4_text_gamename)

        self.p4_text_pagename = QTextEdit(self.makechar)
        self.p4_text_pagename.setObjectName(u"p4_text_pagename")
        self.p4_text_pagename.setMaximumSize(QSize(16777215, 20))
        self.p4_text_pagename.setReadOnly(True)

        self.verticalLayout_9.addWidget(self.p4_text_pagename)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")

        self.horizontalLayout_6.addLayout(self.horizontalLayout_10)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.p4_goback_btn = QPushButton(self.makechar)
        self.p4_goback_btn.setObjectName(u"p4_goback_btn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.p4_goback_btn.sizePolicy().hasHeightForWidth())
        self.p4_goback_btn.setSizePolicy(sizePolicy2)

        self.verticalLayout_11.addWidget(self.p4_goback_btn)

        self.p4_goon_btn = QPushButton(self.makechar)
        self.p4_goon_btn.setObjectName(u"p4_goon_btn")
        sizePolicy2.setHeightForWidth(self.p4_goon_btn.sizePolicy().hasHeightForWidth())
        self.p4_goon_btn.setSizePolicy(sizePolicy2)

        self.verticalLayout_11.addWidget(self.p4_goon_btn)


        self.horizontalLayout_6.addLayout(self.verticalLayout_11)


        self.verticalLayout_9.addLayout(self.horizontalLayout_6)


        self.verticalLayout_3.addLayout(self.verticalLayout_9)

        self.stack_page.addWidget(self.makechar)
        self.playmap = QWidget()
        self.playmap.setObjectName(u"playmap")
        self.verticalLayout_10 = QVBoxLayout(self.playmap)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.graphicsView = QGraphicsView(self.playmap)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout.addWidget(self.graphicsView)


        self.verticalLayout_10.addLayout(self.verticalLayout)

        self.stack_page.addWidget(self.playmap)
        self.fightpage = QWidget()
        self.fightpage.setObjectName(u"fightpage")
        self.verticalLayout_13 = QVBoxLayout(self.fightpage)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.graphicsView_2 = QGraphicsView(self.fightpage)
        self.graphicsView_2.setObjectName(u"graphicsView_2")

        self.horizontalLayout_9.addWidget(self.graphicsView_2)


        self.verticalLayout_13.addLayout(self.horizontalLayout_9)

        self.stack_page.addWidget(self.fightpage)

        self.verticalLayout_12.addWidget(self.stack_page)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.stack_page.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.p1_text_title.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">trpg game</span></p></body></html>", None))
        self.p1_to_p2_btn.setText(QCoreApplication.translate("MainWindow", u"start", None))
        self.p2_text_pagename.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">select game</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.p2_make_game_btn.setText(QCoreApplication.translate("MainWindow", u"new game", None))
        self.p2_del_game_btn.setText(QCoreApplication.translate("MainWindow", u"delete game", None))
        self.p2_to_p1_btn.setText(QCoreApplication.translate("MainWindow", u"go back", None))
        self.p3_text_pagename.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">select char</p></body></html>", None))
        self.p3_make_char_btn.setText(QCoreApplication.translate("MainWindow", u"add char", None))
        self.p3_to_p2_btn.setText(QCoreApplication.translate("MainWindow", u"go back", None))
        self.p3_play_btn.setText(QCoreApplication.translate("MainWindow", u"game goon", None))
        self.p3_del_char_btn.setText(QCoreApplication.translate("MainWindow", u"delete ", None))
        self.p4_text_pagename.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">make char</p></body></html>", None))
        self.p4_goback_btn.setText(QCoreApplication.translate("MainWindow", u"\ub4a4\ub85c\uac00\uae30", None))
        self.p4_goon_btn.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud0dd", None))
    # retranslateUi

