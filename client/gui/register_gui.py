# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_gui.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1121, 882)
        self.username = QLineEdit(Dialog)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(240, 50, 511, 51))
        font = QFont()
        font.setPointSize(16)
        self.username.setFont(font)
        self.username_label = QLabel(Dialog)
        self.username_label.setObjectName(u"username_label")
        self.username_label.setGeometry(QRect(80, 60, 141, 31))
        font1 = QFont()
        font1.setPointSize(22)
        self.username_label.setFont(font1)
        self.password_label = QLabel(Dialog)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setGeometry(QRect(90, 260, 131, 31))
        self.password_label.setFont(font1)
        self.password = QLineEdit(Dialog)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(240, 250, 511, 51))
        self.password.setFont(font)
        self.display_label = QLabel(Dialog)
        self.display_label.setObjectName(u"display_label")
        self.display_label.setGeometry(QRect(30, 160, 191, 31))
        self.display_label.setFont(font1)
        self.display_name = QLineEdit(Dialog)
        self.display_name.setObjectName(u"display_name")
        self.display_name.setGeometry(QRect(240, 150, 511, 51))
        self.display_name.setFont(font)
        self.register_button = QPushButton(Dialog)
        self.register_button.setObjectName(u"register_button")
        self.register_button.setGeometry(QRect(560, 390, 181, 51))
        self.register_button.setFont(font1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Account Registration", None))
        self.username_label.setText(QCoreApplication.translate("Dialog", u"Username: ", None))
        self.password_label.setText(QCoreApplication.translate("Dialog", u"Password: ", None))
        self.display_label.setText(QCoreApplication.translate("Dialog", u"Display Name:", None))
        self.display_name.setText("")
        self.register_button.setText(QCoreApplication.translate("Dialog", u"Register", None))
    # retranslateUi

