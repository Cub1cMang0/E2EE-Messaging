# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_new_gc.ui'
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
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_add_gc_window(object):
    def setupUi(self, add_gc_window):
        if not add_gc_window.objectName():
            add_gc_window.setObjectName(u"add_gc_window")
        add_gc_window.resize(655, 476)
        self.verticalLayout_2 = QVBoxLayout(add_gc_window)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.user_to_add_label = QLabel(add_gc_window)
        self.user_to_add_label.setObjectName(u"user_to_add_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.user_to_add_label.sizePolicy().hasHeightForWidth())
        self.user_to_add_label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(22)
        self.user_to_add_label.setFont(font)

        self.horizontalLayout.addWidget(self.user_to_add_label)

        self.user_search_box = QLineEdit(add_gc_window)
        self.user_search_box.setObjectName(u"user_search_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.user_search_box.sizePolicy().hasHeightForWidth())
        self.user_search_box.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.user_search_box)

        self.search_button = QPushButton(add_gc_window)
        self.search_button.setObjectName(u"search_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.search_button.sizePolicy().hasHeightForWidth())
        self.search_button.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.search_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.error_label = QLabel(add_gc_window)
        self.error_label.setObjectName(u"error_label")
        sizePolicy.setHeightForWidth(self.error_label.sizePolicy().hasHeightForWidth())
        self.error_label.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(16)
        self.error_label.setFont(font1)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.error_label)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.users_being_added_label = QLabel(add_gc_window)
        self.users_being_added_label.setObjectName(u"users_being_added_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.users_being_added_label.sizePolicy().hasHeightForWidth())
        self.users_being_added_label.setSizePolicy(sizePolicy3)
        self.users_being_added_label.setFont(font)

        self.verticalLayout.addWidget(self.users_being_added_label)

        self.user_list = QListWidget(add_gc_window)
        self.user_list.setObjectName(u"user_list")
        sizePolicy1.setHeightForWidth(self.user_list.sizePolicy().hasHeightForWidth())
        self.user_list.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.user_list)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_2 = QPushButton(add_gc_window)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy4)
        self.pushButton_2.setFont(font1)

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.horizontalSpacer = QSpacerItem(228, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_3 = QPushButton(add_gc_window)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy4.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy4)
        self.pushButton_3.setFont(font1)

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.retranslateUi(add_gc_window)

        QMetaObject.connectSlotsByName(add_gc_window)
    # setupUi

    def retranslateUi(self, add_gc_window):
        add_gc_window.setWindowTitle(QCoreApplication.translate("add_gc_window", u"Add New Group Chat", None))
        self.user_to_add_label.setText(QCoreApplication.translate("add_gc_window", u"User to add:", None))
        self.search_button.setText(QCoreApplication.translate("add_gc_window", u"Search", None))
        self.error_label.setText(QCoreApplication.translate("add_gc_window", u"TextLabel", None))
        self.users_being_added_label.setText(QCoreApplication.translate("add_gc_window", u"Users being added:", None))
        self.pushButton_2.setText(QCoreApplication.translate("add_gc_window", u"Cancel", None))
        self.pushButton_3.setText(QCoreApplication.translate("add_gc_window", u"Create Group Chat", None))
    # retranslateUi

