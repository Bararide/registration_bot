from PyQt5 import QtCore, QtGui, QtWidgets, uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget

from database_handler import database_handler
from pyqtgraph import PlotWidget
import pyqtgraph as pg

import sys
import os
import subprocess

dh = database_handler()

class Ui_MainWindow_table(QMainWindow):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.menu = Ui_MainWindow()
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(815, 600)
        self.MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(207, 0, 255, 255), stop:1 rgba(70, 0, 255, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 821, 471))
        self.tableWidget.setStyleSheet("QTableWidget {\n"
"  position: absolute;\n"
"  top: 0;\n"
"  left: 0;\n"
"  right: 0;\n"
"  bottom: 0;\n"
"  background-color: ;\n"
"    background-color: rgb(192, 97, 203);\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"  background-color: rrgb(222, 221, 218);\n"
"  padding: 5px;\n"
"  min-width: 100px;\n"
"  height: 30px;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"  background-color: rgb(145, 65, 172);\n"
"  color: rgb(246, 245, 244);\n"
"  padding: 5px;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"  width: 10px;\n"
"  background-color: rgb(220, 138, 221);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background-color: rgb(192, 97, 203);\n"
"  border-radius: 10px;\n"
"}\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical {\n"
"  background: none;\n"
"}\n"
"\n"
"QTableWidget QScrollBar:horizontal {\n"
"  width: 0;\n"
"  background-color: transparent;\n"
"}")
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setTabKeyNavigation(True)
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setDragDropOverwriteMode(True)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setRowCount(15)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(205)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 490, 191, 51))
        self.pushButton.setStyleSheet("background-color: rgb(226, 136, 246);")
        self.pushButton.setObjectName("pushButton")
        self.MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "тема"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "вопрос"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "факт оплаты"))
        self.pushButton.setText(_translate("MainWindow", "Назад"))
        self.pushButton.clicked.connect(self.back)
    
    def include_table(self, users):
        self.tableWidget.setRowCount(len(users))
        for i in range(len(users)):
            for j in range(4):
                self.tableWidget.setItem(i, j, QTableWidgetItem(f"{users[i][j]}"))

    def back(self):
        self.menu.setupUi(self.MainWindow)
        clients     = []
        payers      = []
        users       = []
        dates_count = []
        dates       = []

        dates_count = dh.add_current_date()
        all_clients = dh.get_all_clients()
        all_payers  = dh.get_all_payers()
        users       = dh.get_all_users()

        for i in range(dates_count):
            dates.append(i)

        print(dates, len(dates))

        clients.append(all_clients)
        payers.append(all_payers)
        
        self.menu.plot(dates, clients, 'r')
        self.menu.plot(dates, payers, 'b')
        print(all_clients, all_payers)
        self.menu.include_table(users, all_clients, all_payers)
        self.MainWindow.show()



class Ui_MainWindow_setting(QMainWindow):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.menu = Ui_MainWindow()
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(800, 600)
        self.MainWindow.setStyleSheet("QWidget{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(207, 0, 255, 255), stop:1 rgba(70, 0, 255, 255));\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 30, 200, 51))
        self.pushButton.setStyleSheet("background-color: rgb(135, 64, 191);\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 130, 200, 51))
        self.pushButton_2.setStyleSheet("background-color: rgb(135, 64, 191);")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(50, 430, 200, 51))
        self.pushButton_5.setStyleSheet("background-color: rgb(135, 64, 191);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.back)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 30, 131, 43))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_2.setFont(font)
        self.label_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_2.setStyleSheet("color: black;\n"
"background-color: none;")
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(400, 30, 361, 51))
        self.textEdit.setStyleSheet("background-color: rgb(246, 245, 244);")
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(400, 130, 361, 51))
        self.textEdit_2.setStyleSheet("background-color: rgb(246, 245, 244);")
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(260, 130, 131, 43))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_3.setFont(font)
        self.label_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_3.setStyleSheet("color: black;\n"
"background-color: none;")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(260, 230, 131, 43))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_4.setFont(font)
        self.label_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_4.setStyleSheet("color: black;\n"
"background-color: none;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(260, 330, 131, 43))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_5.setFont(font)
        self.label_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_5.setStyleSheet("color: black;\n"
"background-color: none;")
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Добавить кнопку"))
        self.pushButton_2.setText(_translate("MainWindow", "Удалить кнопку"))
        self.pushButton_5.setText(_translate("MainWindow", "назад"))
        self.label_2.setText(_translate("MainWindow", "Текст кнопки"))
        self.label_3.setText(_translate("MainWindow", "номер кнопки"))

    def back(self):
        self.menu.setupUi(self.MainWindow)
        clients     = []
        payers      = []
        users       = []
        dates_count = []
        dates       = []

        dates_count = dh.add_current_date()
        all_clients = dh.get_all_clients()
        all_payers  = dh.get_all_payers()
        users       = dh.get_all_users()

        for i in range(dates_count):
            dates.append(i)

        print(dates, len(dates))

        clients.append(all_clients)
        payers.append(all_payers)
        
        self.menu.plot(dates, clients, 'r')
        self.menu.plot(dates, payers, 'b')
        self.menu.add_function()
        print(all_clients, all_payers)
        self.menu.include_table(users, all_clients, all_payers)
        self.MainWindow.show()

    def add_button(self):
        self.pushButton.clicked.connect(self.add_button_on)

    def add_button_on(self):
        text = self.textEdit.toPlainText()
        dh.add_button(text)
        print(text)

    def delete_button(self):
        self.pushButton_2.clicked.connect(self.delete_button_on)

    def delete_button_on(self):
        text = self.textEdit_2.toPlainText()
        dh.delete_button(int(text))






class Ui_MainWindow(QMainWindow):   
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('Interface.ui', self)

        grid = QtWidgets.QGridLayout(self.centralWidget())
        grid.addWidget(self.widget, 0, 0)

        self.setting = Ui_MainWindow_setting()
        self.table   = Ui_MainWindow_table()

        QtCore.QCoreApplication.instance().setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOption('antialias', True)
        pg.setConfigOptions(antialias=True)

    def plot(self, hour, temperature, pen: str):
        plot_data_item = self.widget.plot(hour, temperature)
        plot_data_item.setPen(pen)

    def add_function(self):
        self.pushButton_2.clicked.connect(self.on_bot)

    def call_setting(self):
        self.setting.setupUi(self.mainWindow)
        self.setting.add_button()
        self.setting.delete_button()
        self.mainWindow.show()

    def on_bot(self):
        current_script_path = sys.argv[0]
        current_script_directory = os.path.dirname(os.path.abspath(current_script_path))
        telegram_bot_script = os.path.join(current_script_directory, 'bot.py')
        subprocess.Popen(['python3', telegram_bot_script])

    def setupUi(self, MainWindow):
        self.mainWindow = MainWindow
        self.mainWindow.setObjectName("MainWindow")
        self.mainWindow.setEnabled(True)
        self.mainWindow.resize(1250, 750)
        self.mainWindow.setMouseTracking(False)
        self.mainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(207, 0, 255, 255), stop:1 rgba(70, 0, 255, 255));\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 310, 43))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label.setStyleSheet("color: black;\n"
"background-color: none;")
        self.label.setObjectName("label")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 50, 590, 491))
        self.tableWidget_2.setMaximumSize(QtCore.QSize(590, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget_2.setAutoFillBackground(False)
        self.tableWidget_2.setStyleSheet("QTableWidget {\n"
"  background-color: rgb(226, 136, 246);\n"
"  border: 2px solid black;\n"
"  border-collapse: collapse;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"  padding: 5px;\n"
"  min-width: 100px;\n"
"  height: 30px;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"  background-color: rgb(145, 65, 172);\n"
"  color: rgb(246, 245, 244);\n"
"  padding: 5px;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"  width: 10px;\n"
"  background-color: rgb(220, 138, 221);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background-color: rgb(192, 97, 203);\n"
"  border-radius: 10px;\n"
"}\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical {\n"
"  background: none;\n"
"}")
        self.tableWidget_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.tableWidget_2.setLineWidth(1)
        self.tableWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_2.setAutoScroll(True)
        self.tableWidget_2.setAutoScrollMargin(16)
        self.tableWidget_2.setTabKeyNavigation(True)
        self.tableWidget_2.setProperty("showDropIndicator", True)
        self.tableWidget_2.setDragEnabled(False)
        self.tableWidget_2.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.tableWidget_2.setAlternatingRowColors(False)
        self.tableWidget_2.setTextElideMode(QtCore.Qt.ElideNone)
        self.tableWidget_2.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_2.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_2.setShowGrid(True)
        self.tableWidget_2.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget_2.setRowCount(15)
        self.tableWidget_2.setProperty("string", "")
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        self.tableWidget_2.horizontalHeader().setVisible(True)
        self.tableWidget_2.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(139)
        self.tableWidget_2.horizontalHeader().setHighlightSections(True)
        self.tableWidget_2.horizontalHeader().setMinimumSectionSize(44)
        self.tableWidget_2.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_2.verticalHeader().setHighlightSections(True)
        self.tableWidget_2.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget_2.verticalHeader().setStretchLastSection(False)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 560, 181, 81))
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(450, 560, 181, 81))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("background-color: rgb(135, 64, 191);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("background-color: rgb(135, 64, 191);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.call_table)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(30, 560, 181, 81))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.pushButton = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("QPushButton{\n"
"background-color: rgb(135, 64, 191);\n"
"\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.call_setting)
        self.widget = PlotWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(610, 50, 611, 491))
        self.widget.setStyleSheet("QWidget\n"
"{\n"
"     background-color: rgb(226, 136, 246);\n"
"    border: 2px solid black; \n"
"}\n"
"")
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(700, 560, 441, 43))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_2.setFont(font)
        self.label_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_2.setStyleSheet("color: black;\n"
"background-color: none;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(700, 600, 471, 43))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_3.setFont(font)
        self.label_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_3.setStyleSheet("color: black;\n"
"background-color: none;")
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "bot analysis"))
        self.label.setText(_translate("MainWindow", "Аналитика бота регистрации"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "имя"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "email"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "телефон"))
        self.pushButton_3.setText(_translate("MainWindow", "Вопросы клиентов"))
        self.pushButton_2.setText(_translate("MainWindow", "Включить бота"))
        self.pushButton.setText(_translate("MainWindow", "Настройки"))
        self.label_2.setText(_translate("MainWindow", f"Количество зарегестрированных(красный) 0"))
        self.label_3.setText(_translate("MainWindow", f"Количество оплативших(синий) 0"))

    def call_table(self):
        self.table.setupUi(self.mainWindow)
        questions = dh.get_all_questions()
        self.table.include_table(questions)
        self.mainWindow.show()        

    def include_table(self, users, reg, pay):
        self.tableWidget_2.setRowCount(len(users))
        self.label_2.setText(QtCore.QCoreApplication.translate("MainWindow", f"Количество зарегестрированных(красный) {reg}"))
        self.label_3.setText(QtCore.QCoreApplication.translate("MainWindow", f"Количество оплативших(синий) {pay}"))
        for i in range(len(users)):
            for j in range(4):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(f"{users[i][j]}"))

def application():
    app = QApplication(sys.argv)
    window = QMainWindow()
    win = Ui_MainWindow()

    clients     = []
    payers      = []
    users       = []
    dates_count = []
    dates       = []

    dates_count = dh.add_current_date()
    all_clients = dh.get_all_clients()
    all_payers  = dh.get_all_payers()
    users       = dh.get_all_users()

    for i in range(dates_count):
        dates.append(i)

    print(dates, len(dates))

    clients.append(all_clients)
    payers.append(all_payers)
    
    win.setupUi(window)
    win.plot(dates, clients, 'r')
    win.plot(dates, payers, 'b')
    win.add_function()
    print(all_clients, all_payers)
    win.include_table(users, all_clients, all_payers)
    win.retranslateUi(window)

    window.show()
    sys.exit(app.exec_())

application()