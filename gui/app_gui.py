# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_gui.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1133, 875)
        self.message_log = QTextEdit(main_window)
        self.message_log.setObjectName(u"message_log")
        self.message_log.setGeometry(QRect(239, 9, 881, 781))
        self.send_button = QPushButton(main_window)
        self.send_button.setObjectName(u"send_button")
        self.send_button.setGeometry(QRect(1040, 810, 80, 51))
        self.texting_box = QTextEdit(main_window)
        self.texting_box.setObjectName(u"texting_box")
        self.texting_box.setGeometry(QRect(240, 810, 791, 51))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.texting_box.sizePolicy().hasHeightForWidth())
        self.texting_box.setSizePolicy(sizePolicy)
        self.texting_box.setMinimumSize(QSize(0, 0))
        self.texting_box.setMaximumSize(QSize(16777215, 16777215))
        self.gc_list = QListWidget(main_window)
        self.gc_list.setObjectName(u"gc_list")
        self.gc_list.setGeometry(QRect(10, 59, 211, 801))
        self.add_group_button = QPushButton(main_window)
        self.add_group_button.setObjectName(u"add_group_button")
        self.add_group_button.setGeometry(QRect(10, 10, 211, 41))

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"E2EE Messaging", None))
        self.send_button.setText(QCoreApplication.translate("main_window", u"Send", None))
        self.add_group_button.setText(QCoreApplication.translate("main_window", u"Add Group", None))
    # retranslateUi

