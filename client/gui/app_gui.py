# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1137, 880)
        self.horizontalLayout_2 = QHBoxLayout(main_window)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.add_group_button = QPushButton(main_window)
        self.add_group_button.setObjectName(u"add_group_button")
        font = QFont()
        font.setPointSize(16)
        self.add_group_button.setFont(font)

        self.verticalLayout.addWidget(self.add_group_button)

        self.gc_list = QListWidget(main_window)
        self.gc_list.setObjectName(u"gc_list")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gc_list.sizePolicy().hasHeightForWidth())
        self.gc_list.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.gc_list)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.message_log = QTextEdit(main_window)
        self.message_log.setObjectName(u"message_log")

        self.verticalLayout_2.addWidget(self.message_log)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.texting_box = QTextEdit(main_window)
        self.texting_box.setObjectName(u"texting_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.texting_box.sizePolicy().hasHeightForWidth())
        self.texting_box.setSizePolicy(sizePolicy1)
        self.texting_box.setMinimumSize(QSize(0, 0))
        self.texting_box.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.texting_box)

        self.send_button = QPushButton(main_window)
        self.send_button.setObjectName(u"send_button")
        self.send_button.setFont(font)

        self.horizontalLayout.addWidget(self.send_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"E2EE Messaging", None))
        self.add_group_button.setText(QCoreApplication.translate("main_window", u"Add Group", None))
        self.send_button.setText(QCoreApplication.translate("main_window", u"Send", None))
    # retranslateUi

