from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import requests
from lxml import etree

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(130, 20, 541, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(680, 20, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_click)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 60, 761, 511))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.thread = Worker()
        self.thread.sinOut.connect(self.slotAdd)

    def on_click(self):
        self.pushButton.setEnabled(False)
        self.textBrowser.append('请稍等片刻......')
        key_word = self.lineEdit.text()
        self.thread.key_word = key_word
        self.thread.start()

    def slotAdd(self, file_inf):
        self.textBrowser.append(file_inf)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "知网爬虫"))
        self.lineEdit.setText(_translate("MainWindow", "钒钛"))
        self.label.setText(_translate("MainWindow", "爬取关键字:"))
        self.pushButton.setText(_translate("MainWindow", "开始爬取"))


class Worker(QtCore.QThread):
    sinOut = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.key_word = ''
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        if self.working == True:
            self.getstartpaqu(self.key_word)

    def getstartpaqu(self, key_word):
        self.i=1
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        self.driver = webdriver.Firefox(executable_path=".\geckodriver.exe", firefox_options=fireFoxOptions)
        
        self.driver.get("https://www.cnki.net/")
        self.driver.find_element(By.ID, "txt_SearchText").click()
        self.driver.find_element(By.ID, "txt_SearchText").send_keys(key_word)
        self.driver.find_element(By.ID, "txt_SearchText").send_keys(Keys.ENTER)
        time.sleep(2.5)

        for a in range(1,200): #232
            url = "https://kns.cnki.net/kns/brief/brief.aspx?curpage="+str(a)+"&RecordsPerPage=20&QueryID=9&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx&isinEn=1&"
            # print('【输出】'+url)
            self.driver.get(url)
            time.sleep(1)
            parser = GETHREFHTMLParser()
            parser.feed(self.driver.page_source)
            # print('【输出】'+parser.urls)
            self.sonhtmlgetdata(parser.urls)
            parser.clearurl

    def sonhtmlgetdata(self, urllist): #用于处理子网页
        for url in urllist:
            title = ''
            abstract = ''
            keys = []
            papers = []
            abstract_data = []
            keys_data = []

            r = requests.get(url)
            time.sleep(1)
            tree=etree.HTML(r.text)
            title = tree.xpath('//h2[@class="title"]/text()')[0]
            abstract_data = tree.xpath('//span[@id="ChDivSummary"]/text()')
            papers = tree.xpath('//div[@class="author"]/span/a/text()')
            abstract = ''.join(abstract_data).replace('\n', '')
            if tree.xpath('//div[@class="wxBaseinfo"]/p[2]/label/text()')[0] == '关键词：':
                keys_data = tree.xpath('//div[@class="wxBaseinfo"]/p[2]/a/text()')
            if tree.xpath('//div[@class="wxBaseinfo"]/p[2]/label/text()')[0] == '基金：':
                keys_data = tree.xpath('//div[@class="wxBaseinfo"]/p[3]/a/text()')
            if papers == []:
                papers = tree.xpath('//div[@class="author"]/span/text()')
            keys = []
            for key in keys_data:
                keys.append(key.strip().strip(';'))
            # print(i)
            # print('【输出】'+title)
            # print('【输出】'+abstract)
            # print('【输出】'+str(keys))
            # print('【输出】'+str(papers))
            self.sinOut.emit('【序号】'+str(self.i))
            self.sinOut.emit('【标题】'+title)
            self.sinOut.emit('【作者】'+str(papers))
            self.sinOut.emit('【摘要】'+abstract)
            self.sinOut.emit('【关键字】'+str(keys))
            self.sinOut.emit('\n')
            self.i+=1

from html.parser import HTMLParser

class GETHREFHTMLParser(HTMLParser): #处理<a>标签内链接
    urls = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a' and ('class','fz14') in attrs:
            for attr in attrs:
                if attr[0] == 'href':
                    url='https://kns.cnki.net/KCMS' + attr[1][4:]
                    # print('【输出】'+url)
                    self.urls.append (url)

    def clearurl(self):
        self.urls = []
        self.reset()

import time
import json


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())







