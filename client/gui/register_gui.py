# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_gui.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1130, 882)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.login_register_window = QStackedWidget(Dialog)
        self.login_register_window.setObjectName(u"login_register_window")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_register_window.sizePolicy().hasHeightForWidth())
        self.login_register_window.setSizePolicy(sizePolicy)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.username_hlayout = QHBoxLayout()
        self.username_hlayout.setObjectName(u"username_hlayout")
        self.username_label_r = QLabel(self.page)
        self.username_label_r.setObjectName(u"username_label_r")
        font = QFont()
        font.setPointSize(22)
        self.username_label_r.setFont(font)

        self.username_hlayout.addWidget(self.username_label_r)

        self.username_r = QLineEdit(self.page)
        self.username_r.setObjectName(u"username_r")
        font1 = QFont()
        font1.setPointSize(16)
        self.username_r.setFont(font1)

        self.username_hlayout.addWidget(self.username_r)


        self.verticalLayout_2.addLayout(self.username_hlayout)

        self.display_name_hlayout = QHBoxLayout()
        self.display_name_hlayout.setObjectName(u"display_name_hlayout")
        self.display_label = QLabel(self.page)
        self.display_label.setObjectName(u"display_label")
        self.display_label.setFont(font)

        self.display_name_hlayout.addWidget(self.display_label)

        self.display_name = QLineEdit(self.page)
        self.display_name.setObjectName(u"display_name")
        self.display_name.setFont(font1)

        self.display_name_hlayout.addWidget(self.display_name)


        self.verticalLayout_2.addLayout(self.display_name_hlayout)

        self.password_hlayout = QHBoxLayout()
        self.password_hlayout.setObjectName(u"password_hlayout")
        self.password_label_r = QLabel(self.page)
        self.password_label_r.setObjectName(u"password_label_r")
        self.password_label_r.setFont(font)

        self.password_hlayout.addWidget(self.password_label_r)

        self.password_r = QLineEdit(self.page)
        self.password_r.setObjectName(u"password_r")
        self.password_r.setFont(font1)

        self.password_hlayout.addWidget(self.password_r)


        self.verticalLayout_2.addLayout(self.password_hlayout)

        self.register_vlayout = QVBoxLayout()
        self.register_vlayout.setObjectName(u"register_vlayout")
        self.register_button = QPushButton(self.page)
        self.register_button.setObjectName(u"register_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.register_button.sizePolicy().hasHeightForWidth())
        self.register_button.setSizePolicy(sizePolicy1)
        self.register_button.setFont(font)

        self.register_vlayout.addWidget(self.register_button)

        self.error_label_r = QLabel(self.page)
        self.error_label_r.setObjectName(u"error_label_r")
        self.error_label_r.setFont(font1)
        self.error_label_r.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.register_vlayout.addWidget(self.error_label_r)


        self.verticalLayout_2.addLayout(self.register_vlayout)

        self.register_2_login_hlayout = QHBoxLayout()
        self.register_2_login_hlayout.setObjectName(u"register_2_login_hlayout")
        self.login_label = QLabel(self.page)
        self.login_label.setObjectName(u"login_label")
        self.login_label.setFont(font1)

        self.register_2_login_hlayout.addWidget(self.login_label)

        self.register_2_login = QPushButton(self.page)
        self.register_2_login.setObjectName(u"register_2_login")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.register_2_login.sizePolicy().hasHeightForWidth())
        self.register_2_login.setSizePolicy(sizePolicy2)

        self.register_2_login_hlayout.addWidget(self.register_2_login)


        self.verticalLayout_2.addLayout(self.register_2_login_hlayout)

        self.login_register_window.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_4 = QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.username_label_l = QLabel(self.page_2)
        self.username_label_l.setObjectName(u"username_label_l")
        self.username_label_l.setFont(font)

        self.horizontalLayout.addWidget(self.username_label_l)

        self.username_l = QLineEdit(self.page_2)
        self.username_l.setObjectName(u"username_l")
        self.username_l.setFont(font1)

        self.horizontalLayout.addWidget(self.username_l)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.password_label_l = QLabel(self.page_2)
        self.password_label_l.setObjectName(u"password_label_l")
        self.password_label_l.setFont(font)

        self.horizontalLayout_2.addWidget(self.password_label_l)

        self.password_l = QLineEdit(self.page_2)
        self.password_l.setObjectName(u"password_l")
        self.password_l.setFont(font1)

        self.horizontalLayout_2.addWidget(self.password_l)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.login_button = QPushButton(self.page_2)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setFont(font)

        self.verticalLayout_3.addWidget(self.login_button)

        self.error_label_l = QLabel(self.page_2)
        self.error_label_l.setObjectName(u"error_label_l")
        self.error_label_l.setFont(font1)
        self.error_label_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.error_label_l)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.register_label = QLabel(self.page_2)
        self.register_label.setObjectName(u"register_label")
        self.register_label.setFont(font1)

        self.horizontalLayout_3.addWidget(self.register_label)

        self.login_2_register = QPushButton(self.page_2)
        self.login_2_register.setObjectName(u"login_2_register")

        self.horizontalLayout_3.addWidget(self.login_2_register)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.login_register_window.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.login_register_window)


        self.retranslateUi(Dialog)

        self.login_register_window.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Account Registration", None))
        self.username_label_r.setText(QCoreApplication.translate("Dialog", u"Username: ", None))
        self.display_label.setText(QCoreApplication.translate("Dialog", u"Display Name:", None))
        self.display_name.setText("")
        self.password_label_r.setText(QCoreApplication.translate("Dialog", u"Password: ", None))
        self.register_button.setText(QCoreApplication.translate("Dialog", u"Register", None))
        self.error_label_r.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.login_label.setText(QCoreApplication.translate("Dialog", u"Already a user? Login", None))
        self.register_2_login.setText(QCoreApplication.translate("Dialog", u"here", None))
        self.username_label_l.setText(QCoreApplication.translate("Dialog", u"Username: ", None))
        self.password_label_l.setText(QCoreApplication.translate("Dialog", u"Password: ", None))
        self.login_button.setText(QCoreApplication.translate("Dialog", u"Login", None))
        self.error_label_l.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.register_label.setText(QCoreApplication.translate("Dialog", u"New user? Register", None))
        self.login_2_register.setText(QCoreApplication.translate("Dialog", u"here", None))
    # retranslateUi

