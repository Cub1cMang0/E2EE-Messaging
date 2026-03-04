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
        add_gc_window.resize(846, 587)
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

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.group_chat_label = QLabel(add_gc_window)
        self.group_chat_label.setObjectName(u"group_chat_label")
        sizePolicy.setHeightForWidth(self.group_chat_label.sizePolicy().hasHeightForWidth())
        self.group_chat_label.setSizePolicy(sizePolicy)
        self.group_chat_label.setFont(font)

        self.horizontalLayout_3.addWidget(self.group_chat_label)

        self.group_chat_name = QLineEdit(add_gc_window)
        self.group_chat_name.setObjectName(u"group_chat_name")
        sizePolicy1.setHeightForWidth(self.group_chat_name.sizePolicy().hasHeightForWidth())
        self.group_chat_name.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.group_chat_name)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cancel_button = QPushButton(add_gc_window)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy4)
        self.cancel_button.setFont(font1)

        self.horizontalLayout_2.addWidget(self.cancel_button)

        self.horizontalSpacer = QSpacerItem(228, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.create_gc_button = QPushButton(add_gc_window)
        self.create_gc_button.setObjectName(u"create_gc_button")
        sizePolicy4.setHeightForWidth(self.create_gc_button.sizePolicy().hasHeightForWidth())
        self.create_gc_button.setSizePolicy(sizePolicy4)
        self.create_gc_button.setFont(font1)

        self.horizontalLayout_2.addWidget(self.create_gc_button)


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
        self.group_chat_label.setText(QCoreApplication.translate("add_gc_window", u"Group Chat Name:", None))
        self.cancel_button.setText(QCoreApplication.translate("add_gc_window", u"Cancel", None))
        self.create_gc_button.setText(QCoreApplication.translate("add_gc_window", u"Create Group Chat", None))
    # retranslateUi

