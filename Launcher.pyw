import sys
import os
from PyQt5.QtWidgets import *

from Launcher_ui import *

class Launcher(QWidget,Ui_Launcher):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.lw_versions.itemClicked.connect(lambda:self.pb_startgame.setEnabled(True))
        self.pb_startgame.clicked.connect(lambda:os.system(f'cd ".minecraft2d/versions/{self.lw_versions.currentItem().text()}"& start pythonw Minecraft2D.py&cd..&cd..&cd..'))
        self.set_lw_versions()

    def set_lw_versions(self):
        self.lw_versions.clear()
        for i in os.listdir('.minecraft2d/versions'):
            self.lw_versions.addItem(i)

if __name__=='__main__':
    app=QApplication(sys.argv)
    launcher=Launcher()
    launcher.show()
    sys.exit(app.exec_())
