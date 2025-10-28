# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialpad.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_DialpadWindow(object):
    def setupUi(self, DialpadWindow):
        if not DialpadWindow.objectName():
            DialpadWindow.setObjectName(u"DialpadWindow")
        DialpadWindow.resize(317, 521)
        self.centralwidget = QWidget(DialpadWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.dailpadInput = QPlainTextEdit(self.centralwidget)
        self.dailpadInput.setObjectName(u"dailpadInput")
        self.dailpadInput.setMinimumSize(QSize(0, 40))
        self.dailpadInput.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_2.addWidget(self.dailpadInput)

        self.contactsLayout = QVBoxLayout()
        self.contactsLayout.setObjectName(u"contactsLayout")

        self.verticalLayout_2.addLayout(self.contactsLayout)

        self.btnFrame = QFrame(self.centralwidget)
        self.btnFrame.setObjectName(u"btnFrame")
        self.btnFrame.setMinimumSize(QSize(0, 40))
        self.btnFrame.setMaximumSize(QSize(16777215, 40))
        self.btnFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.btnFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.btnFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.saveBtn = QPushButton(self.btnFrame)
        self.saveBtn.setObjectName(u"saveBtn")

        self.horizontalLayout.addWidget(self.saveBtn)

        self.callBtn = QPushButton(self.btnFrame)
        self.callBtn.setObjectName(u"callBtn")

        self.horizontalLayout.addWidget(self.callBtn)


        self.verticalLayout_2.addWidget(self.btnFrame)

        DialpadWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(DialpadWindow)
        self.statusbar.setObjectName(u"statusbar")
        DialpadWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DialpadWindow)

        QMetaObject.connectSlotsByName(DialpadWindow)
    # setupUi

    def retranslateUi(self, DialpadWindow):
        DialpadWindow.setWindowTitle(QCoreApplication.translate("DialpadWindow", u"MainWindow", None))
        self.saveBtn.setText(QCoreApplication.translate("DialpadWindow", u"Save", None))
        self.callBtn.setText(QCoreApplication.translate("DialpadWindow", u"Call", None))
    # retranslateUi

