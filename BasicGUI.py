import sys
from PyQt5 import QtWidgets

class MyApp(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        
        self.count = 0

    def initUI(self):

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.label_1 =QtWidgets.QLabel('Press the Button!!')
        grid.addWidget(self.label_1,0,0)
        self.button_1 = QtWidgets.QPushButton('Hit Me!')
        grid.addWidget(self.button_1,0,1)
        self.button_1.clicked.connect(self.MysteryButton)

        self.setWindowTitle('Mystery Button...')
        self.setGeometry(300,300,300,300)
        self.show()

    def MysteryButton(self):
        self.count += 1
        if self.count == 1:
            self.label_1.setText('Hey, we are GlucoHealth!! Have a cookie!!')
        else:
            self.label_1.setText(f'Hey, we are GlucoHealth!! Have {self.count} Cookies')
        self.button_1.setText('Again!')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    



