# -*- coding: utf-8 -*-
# coding=utf8
import sys
from PyQt5 import  QtGui,QtCore,QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import  QApplication,QMainWindow,QPushButton,QAction,QMessageBox,QCheckBox,QComboBox,QLineEdit , QPlainTextEdit
from PyQt5.uic import loadUi
import NaiveBayesCat as nb
import DecisionTreeCat as dt
from pandas import *

data = read_csv('data3.csv')
model_training = nb.NaiveBayesClassfier().fit(data,"Phuong_Phap")

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        loadUi('Interface.ui',self) ## load file .ui
        self.setWindowTitle("BLASTRec") ## set the tile
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))


        gionglua = list(np.unique(data['Giong_Lua']))
        nhietdo = np.arange(0, 51)
        matdosa = np.arange(0,101)
        doam = np.arange(0,101)
        self.input_gionglua.addItems([str(s) for s in gionglua])
        self.input_matdosa.addItems([str(s) for s in matdosa])
        self.input_nhietdo.addItems([str(s) for s in nhietdo])
        self.input_doam.addItems([str(s) for s in doam])

        #   Slots :
        self.btn_run.clicked.connect(self.on_btn_run_clicked)
        self.info_color_leaf_btn.clicked.connect(self.on_info_color_leaf_btn_clicked)
        self.info_lesion_btn.clicked.connect(self.on_info_lesion_btn_clicked)


    @pyqtSlot()

    #Work in progress
    def on_info_color_leaf_btn_clicked(self):
        pass

    #Work in progress
    def on_info_lesion_btn_clicked(self):
        pass


    def on_btn_run_clicked(self):
        if(self.input_matdosa.currentText() == "unselected" or self.input_nhietdo.currentText() == "unselected" or self.input_doam.currentText() == "unselected" or self.input_gionglua.currentText() == "unselected" or self.input_maula.currentText() == "unselected" or self.input_tinhtrangbenh.currentText() == "unselected" ):
            QMessageBox.about(self, 'Message', "Some Feature are empty !")
        else:
            value_matdosa = None
            value_nhietdo = None
            value_doam = None
            if(int(self.input_matdosa.currentText()) >= 20):
                value_matdosa = 'high'
            else:
                value_matdosa = 'low'
            if(int(self.input_nhietdo.currentText()) > 27):
                value_nhietdo = 'high'
            else:
                value_nhietdo = 'low'
            if(int(self.input_doam.currentText()) > 80):
                value_doam = 'high'
            else:
                value_doam = 'low'

            tup =(self.input_gionglua.currentText(),value_matdosa,value_nhietdo,value_doam,
                         int(self.input_maula.currentText()),int(self.input_tinhtrangbenh.currentText()))
            sample = [tup]
            sample = pandas.DataFrame.from_records(sample,
                                          columns=["Giong_Lua", "Mat_Do_Sa", "Nhiet_Do", "Do_Am", "Mau_La",
                                                   "Tinh_Trang_Benh"])
            solution = model_training.predict(sample)

            if solution[0] == 0:
                self.txt_pp.setPlainText('Không phát hiện bệnh đạo ôn, ngưng bón đạm, tăng cường bón kali cho lúa. Tiếp tục chăm sóc và quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 1:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh hình chấm kim, ẩm độ không khí thấp, nhiệt độ môi trường cao. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị phòng ngừa bệnh đạo ôn với lượng thuốc phun 160-240 lít/ha. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 2:
                 self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh hình chấm kim, ẩm độ không khí cao, nhiệt độ môi trường thấp. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị phòng ngừa bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời. ')
            if solution[0] == 3:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá với vết bệnh điển hình (dạng mắt én). Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng.Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha.')
            if solution[0] == 4:
                self.txt_pp.setPlainText('Bệnh xuất hiện nhiều vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha.')
            if solution[0] == 5:
                self.txt_pp.setPlainText('Bệnh có vết điển hình (dạng mắt én) xuất hiện nhiều ở tầng lá bên trên. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha. Theo dõi bệnh và phun lặp lại sau 1 tuần.')
            if solution[0] == 6:
                self.txt_pp.setPlainText('Bệnh điển hình (dạng mắt én) xuất hiện nhiều, vết bệnh xuất hiện xuống các tầng lá bên dưới. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 600-800 lít/ha để đảm bảo thuốc xuống được các lá bên dưới (phun chồng lối hoặc phun đẫm). Tiếp tục theo dõi bệnh đặc biệt là ở các lá bên dưới, tiến hành phun lặp lại sau khi phun lần đầu 5 ngày với lượng thuốc 300-400 lít/ha trong trường hợp bệnh thuyên giảm; đổi thuốc phun với lượng 600-800 lít/ha trong trường hợp bệnh không giảm.')
            if solution[0] == 7:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị phòng ngừa bệnh đạo ôn với lượng thuốc phun 160-240 lít/ha. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 8:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá với vết bệnh điển hình (dạng mắt én) .Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha.')
            if solution[0] == 9:
                self.txt_pp.setPlainText('Bệnh xuất hiện nhiều vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha.')
            if solution[0] == 10:
                self.txt_pp.setPlainText('Bệnh có vết điển hình (dạng mắt én) xuất hiện nhiều ở tầng lá bên trên. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha. Theo dõi bệnh và phun lặp lại sau 1 tuần.')
            if solution[0] == 11:
                self.txt_pp.setPlainText('Bệnh điển hình (dạng mắt én) xuất hiện nhiều, vết bệnh xuất hiện xuống các tầng lá bên dưới. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 600-800 lít/ha để đảm bảo thuốc xuống được các lá bên dưới (phun chồng lối hoặc phun đẫm). Tiếp tục theo dõi bệnh đặc biệt là ở các lá bên dưới, tiến hành phun lặp lại sau khi phun lần đầu 5 ngày với lượng thuốc 300-400 lít/ha trong trường hợp bệnh thuyên giảm; đổi thuốc phun với lượng 600-800 lít/ha trong trường hợp bệnh không giảm.')
            if solution[0] == 12:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị phòng ngừa bệnh đạo ôn với lượng thuốc phun 160-240 lít/ha. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 13:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá với vết bệnh điển hình (dạng mắt én). Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha.')
            if solution[0] == 14:
                self.txt_pp.setPlainText('Xuất hiện nhiều vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha.')
            if solution[0] == 15:
                self.txt_pp.setPlainText('Bệnh có vết điển hình (dạng mắt én) xuất hiện nhiều ở tầng lá bên trên. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha. Theo dõi bệnh và phun lặp lại sau 1 tuần.')
            if solution[0] == 16:
                self.txt_pp.setPlainText('Bệnh điển hình (dạng mắt én) xuất hiện nhiều, vết bệnh xuất hiện xuống các tầng lá bên dưới. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng.Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 600-800 lít/ha để đảm bảo thuốc xuống được các lá bên dưới (phun chồng lối hoặc phun đẫm). Tiếp tục theo dõi bệnh đặc biệt là ở các lá bên dưới, tiến hành phun lặp lại sau khi phun lần đầu 5 ngày với lượng thuốc 300-400 lít/ha trong trường hợp bệnh thuyên giảm; đổi thuốc phun với lượng 600-800 lít/ha trong trường hợp bệnh không giảm.')
            if solution[0] == 17:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh hình chấm kim, ẩm độ không khí thấp, nhiệt độ môi trường cao. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 18:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh hình chấm kim, ẩm độ không khí cao, nhiệt độ môi trường thấp. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị phòng ngừa bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 19:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá với vết bệnh điển hình (dạng mắt én). Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha')
            if solution[0] == 20:
                self.txt_pp.setPlainText('Bệnh xuất hiện nhiều vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha')
            if solution[0] == 21:
                self.txt_pp.setPlainText('Bệnh có vết điển hình (dạng mắt én) xuất hiện nhiều ở tầng lá bên trên. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha. Theo dõi bệnh và phun lặp lại sau 1 tuần.')
            if solution[0] == 22:
                self.txt_pp.setPlainText('Bệnh điển hình (dạng mắt én) xuất hiện nhiều, vết bệnh xuất hiện xuống các tầng lá bên dưới. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 600-800 lít/ha để đảm bảo thuốc xuống được các lá bên dưới (phun chồng lối hoặc phun đẫm). Tiếp tục theo dõi bệnh đặc biệt là ở các lá bên dưới, tiến hành phun lặp lại sau khi phun lần đầu 5 ngày với lượng thuốc 300-400 lít/ha trong trường hợp bệnh thuyên giảm; đổi thuốc phun với lượng 600-800 lít/ha trong trường hợp bệnh không giảm.')
            if solution[0] == 23:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 24:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá với vết bệnh điển hình (dạng mắt én). Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 160-240 lít/ha.')
            if solution[0] == 25:
                self.txt_pp.setPlainText('Bệnh xuất hiện nhiều vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 160-240 lít/ha')
            if solution[0] == 26:
                self.txt_pp.setPlainText('Bệnh có vết điển hình (dạng mắt én) xuất hiện nhiều ở tầng lá bên trên. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha. Theo dõi bệnh để tiếp tục phòng trừ bệnh đạo ôn.')
            if solution[0] == 27:
                self.txt_pp.setPlainText('Bệnh điển hình (dạng mắt én) xuất hiện nhiều, vết bệnh xuất hiện xuống các tầng lá bên dưới. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 600-800 lít/ha để đảm bảo thuốc xuống được các lá bên dưới (phun chồng lối hoặc phun đẫm). Tiếp tục theo dõi bệnh đặc biệt là ở các lá bên dưới, tiến hành phun lặp lại sau khi phun lần đầu 5 ngày với lượng thuốc 300-400 lít/ha trong trường hợp bệnh thuyên giảm; đổi thuốc phun với lượng 600-800 lít/ha trong trường hợp bệnh không giảm.')
            if solution[0] == 28:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 29:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh điển hình (dạng mắt én). Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 30:
                self.txt_pp.setPlainText('Bệnh xuất hiện nhiều vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 160-240 lít/ha.')
            if solution[0] == 31:
                self.txt_pp.setPlainText('Bệnh có vết điển hình (dạng mắt én) xuất hiện nhiều ở tầng lá bên trên. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha. Theo dõi bệnh để tiếp tục phòng trừ bệnh đạo ôn.')
            if solution[0] == 32:
                self.txt_pp.setPlainText('Bệnh điển hình (dạng mắt én) xuất hiện nhiều, vết bệnh xuất hiện xuống các tầng lá bên dưới. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng.Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 600-800 lít/ha để đảm bảo thuốc xuống được các lá bên dưới (phun chồng lối hoặc phun đẫm). Tiếp tục theo dõi bệnh đặc biệt là ở các lá bên dưới, tiến hành phun lặp lại sau khi phun lần đầu 5 ngày với lượng thuốc 300-400 lít/ha trong trường hợp bệnh thuyên giảm; đổi thuốc phun với lượng 600-800 lít/ha trong trường hợp bệnh không giảm.')
            if solution[0] == 33:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá, vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng.Phun thuốc đặc trị phòng ngừa bệnh đạo ôn với lượng thuốc phun 160-240 lít/ha. Tiếp tục quan sát lúa để phòng trừ bệnh đạo ôn kịp thời.')
            if solution[0] == 34:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá với vết bệnh điển hình (dạng mắt én). Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng.Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha.')
            if solution[0] == 35:
                self.txt_pp.setPlainText('Bệnh xuất hiện lác đác trên lá với xuất hiện nhiều vết bệnh hình chấm kim. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng.Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha.')
            if solution[0] == 36:
                self.txt_pp.setPlainText('Bệnh có vết điển hình (dạng mắt én) xuất hiện nhiều ở tầng lá bên trên. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng.Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 300-400 lít/ha. Theo dõi bệnh và phun lặp lại sau 1 tuần.')
            if solution[0] == 37:
                self.txt_pp.setPlainText('Bệnh điển hình (dạng mắt én) xuất hiện nhiều, vết bệnh xuất hiện xuống các tầng lá bên dưới. Cần ngừng ngay việc bón phân, duy trì mực nước trong ruộng. Phun thuốc đặc trị bệnh đạo ôn với lượng thuốc phun 600-800 lít/ha để đảm bảo thuốc xuống được các lá bên dưới (phun chồng lối hoặc phun đẫm). Tiếp tục theo dõi bệnh đặc biệt là ở các lá bên dưới, tiến hành phun lặp lại sau khi phun lần đầu 5 ngày với lượng thuốc 300-400 lít/ha trong trường hợp bệnh thuyên giảm; đổi thuốc phun với lượng 600-800 lít/ha trong trường hợp bệnh không giảm.')





app = QApplication(sys.argv)
GUI = Window()
GUI.show()
sys.exit(app.exec_())
