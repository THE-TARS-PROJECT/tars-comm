# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(483, 162)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.emailLabel = QLabel(Dialog)
        self.emailLabel.setObjectName(u"emailLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.emailLabel)

        self.emailInput = QLineEdit(Dialog)
        self.emailInput.setObjectName(u"emailInput")
        self.emailInput.setMinimumSize(QSize(0, 30))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.emailInput)

        self.passwordLabel = QLabel(Dialog)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.passwordLabel)

        self.passwordInput = QLineEdit(Dialog)
        self.passwordInput.setObjectName(u"passwordInput")
        self.passwordInput.setMinimumSize(QSize(0, 30))
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.passwordInput)


        self.verticalLayout.addLayout(self.formLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.submitBtn = QPushButton(Dialog)
        self.submitBtn.setObjectName(u"submitBtn")
        self.submitBtn.setMinimumSize(QSize(0, 30))

        self.verticalLayout_2.addWidget(self.submitBtn, 0, Qt.AlignmentFlag.AlignRight)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"AUTHENTICATE", None))
        self.emailLabel.setText(QCoreApplication.translate("Dialog", u"Email", None))
        self.passwordLabel.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.submitBtn.setText(QCoreApplication.translate("Dialog", u"SUBMIT", None))
    # retranslateUi

