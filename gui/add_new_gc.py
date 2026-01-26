# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_new_gc.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_add_gc_window(object):
    def setupUi(self, add_gc_window):
        if not add_gc_window.objectName():
            add_gc_window.setObjectName(u"add_gc_window")
        add_gc_window.resize(655, 476)
        self.user_search_box = QTextEdit(add_gc_window)
        self.user_search_box.setObjectName(u"user_search_box")
        self.user_search_box.setGeometry(QRect(180, 30, 351, 41))
        self.user_to_add_label = QLabel(add_gc_window)
        self.user_to_add_label.setObjectName(u"user_to_add_label")
        self.user_to_add_label.setGeometry(QRect(10, 30, 161, 41))
        font = QFont()
        font.setPointSize(22)
        self.user_to_add_label.setFont(font)
        self.pushButton = QPushButton(add_gc_window)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(550, 30, 94, 41))
        self.user_list = QTextEdit(add_gc_window)
        self.user_list.setObjectName(u"user_list")
        self.user_list.setGeometry(QRect(10, 210, 631, 81))
        self.users_being_added_label = QLabel(add_gc_window)
        self.users_being_added_label.setObjectName(u"users_being_added_label")
        self.users_being_added_label.setGeometry(QRect(10, 150, 271, 41))
        self.users_being_added_label.setFont(font)
        self.pushButton_2 = QPushButton(add_gc_window)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(10, 420, 201, 41))
        font1 = QFont()
        font1.setPointSize(16)
        self.pushButton_2.setFont(font1)
        self.pushButton_3 = QPushButton(add_gc_window)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(440, 420, 201, 41))
        self.pushButton_3.setFont(font1)

        self.retranslateUi(add_gc_window)

        QMetaObject.connectSlotsByName(add_gc_window)
    # setupUi

    def retranslateUi(self, add_gc_window):
        add_gc_window.setWindowTitle(QCoreApplication.translate("add_gc_window", u"Add New Group Chat", None))
        self.user_to_add_label.setText(QCoreApplication.translate("add_gc_window", u"User to add:", None))
        self.pushButton.setText(QCoreApplication.translate("add_gc_window", u"Search", None))
        self.users_being_added_label.setText(QCoreApplication.translate("add_gc_window", u"Users being added:", None))
        self.pushButton_2.setText(QCoreApplication.translate("add_gc_window", u"Cancel", None))
        self.pushButton_3.setText(QCoreApplication.translate("add_gc_window", u"Create Group Chat", None))
    # retranslateUi

