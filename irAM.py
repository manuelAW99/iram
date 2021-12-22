# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'irAM.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import mri.sri as s


class Ui_MainWindow(object):
    def __init__(self):
        self.SRI = s.sri()
        self.corpus = ''
        self.query = None
        self.recovered = []
        self.relevant = []
        self.not_relevant = []
        self.groups = []
        self.relevants = []
        self.window = None
        
    def setupUi(self, MainWindow):
        self.window = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1024, 768)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(440, 10, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.search_input = QtWidgets.QComboBox(self.centralwidget)
        self.search_input.setGeometry(QtCore.QRect(180, 50, 705, 31))
        self.search_input.setEditable(True)
        self.search_input.setObjectName("search_input")
        
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(915, 50, 89, 31))
        self.search_button.setObjectName("search_button")
    
        self.corpus_combo = QtWidgets.QComboBox(self.centralwidget)
        self.corpus_combo.setGeometry(QtCore.QRect(20, 50, 131, 31))
        self.corpus_combo.setEditable(False)
        self.corpus_combo.setObjectName("corpus_combo")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 121, 17))
        self.label_2.setObjectName("label_2")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(12, 90, 1000, 655))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1000, 655))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.corpus_combo.currentTextChanged['QString'].connect(self.set_corpus)
        self.search_button.clicked.connect(self.search_query)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def set_corpus(self,text):
        self.corpus = text
        self.SRI.load_corpus(self.corpus)
    
    def search_query(self):
        if self.search_input.currentText() != '':
            if len(self.groups) > 0:
                self.groups = []
                self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
                self.scrollArea.setGeometry(QtCore.QRect(12, 90, 1000, 655))
                self.scrollArea.setWidgetResizable(True)
                self.scrollArea.setObjectName("scrollArea")
                self.scrollAreaWidgetContents = QtWidgets.QWidget()
                self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1000, 655))
                self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
                self.scrollArea.setWidget(self.scrollAreaWidgetContents)
                self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
                self.verticalLayout.setObjectName("verticalLayout")
            
            repeat = 0
            for q in self.SRI.get_querys():
                if q.get_text() == self.search_input.currentText():
                    self.query = q
                    repeat = 1
                    break
            if not repeat:
                self.query = self.SRI.create_query(self.search_input.currentText())
                self.SRI.insert_query(self.query)
                self.search_input.addItem(self.query._text)
                
            r = self.SRI.ranking(self.query) if len(self.query.get_relevants()) == 0 else self.SRI.retro(self.query)
            index = 0
            for d in r:
                g = self.group(self.scrollAreaWidgetContents, self.verticalLayout, d[0], index, self.query)
                self.groups.append(g)
                index += 1
            self.scrollArea.show()
            self.retranslateUi(self.window)
            
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "irAM Searcher"))
        self.search_button.setText(_translate("MainWindow", "Search"))
        self.label_2.setText(_translate("MainWindow", "Select Corpus:"))
        for group in self.groups:
            group.group.setTitle(_translate("MainWindow", "Document: "+group.subject))
            group.check.setText(_translate("MainWindow", "Relevant"))

    class group:
        def __init__(self, ScrollArea, layout, doc, index, query):
            self.area = ScrollArea
            self.doc = doc
            self.subject = doc.get_subject()
            self.index = index
            self.query = query
            
            self.group = QtWidgets.QGroupBox(self.area)
            self.group.setGeometry(QtCore.QRect(10, 10 + 101 * index, 741 , 150))
            self.group.setObjectName(self.subject)
            layout.addWidget(self.group)
            self.my_layout = QtWidgets.QVBoxLayout(self.group)
            self.my_layout.setObjectName("layout"+str(index))
            self.group.show()
            
            self.check = QtWidgets.QCheckBox(self.group)
            self.check.setObjectName("relevant_"+str(index))
            self.check.setGeometry(QtCore.QRect(640, 30, 92, 23))
            if doc in query.get_relevants():
                self.check.setChecked(True)
            self.my_layout.addWidget(self.check)
            self.check.stateChanged.connect(lambda: self.relevant(self.check))
            self.check.show()
            
            self.text = QtWidgets.QTextEdit(self.group)
            self.text.setEnabled(True)
            self.text.setGeometry(QtCore.QRect(0, 19, 631, 81))
            self.text.setFrameShape(QtWidgets.QFrame.Box)
            self.text.setFrameShadow(QtWidgets.QFrame.Plain)
            self.text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.text.setObjectName("text_"+str(index))
            self.text.setText(doc.get_text())
            self.text.setReadOnly(True)
            self.text.setFrameShape(QtWidgets.QFrame.HLine)
            self.my_layout.addWidget(self.text)
            self.text.show()
            
        def relevant(self, c):
            if c.isChecked():
                if self.doc not in self.query.get_relevants():
                    self.query.set_relevant(self.doc)
                if self.doc in self.query.get_not_relevants():
                    self.query.get_not_relevants().remove(self.doc)
            else:
                if self.doc not in self.query.get_not_relevants():
                    self.query.set_not_relevant(self.doc)
                if self.doc in self.query.get_relevants():
                    self.query.get_relevants().remove(self.doc)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    SRI = s.sri()
    options = SRI.select_corpus()
    ui.corpus_combo.addItems(options)
    MainWindow.show()
    sys.exit(app.exec_())
