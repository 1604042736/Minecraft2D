import sys
import os
import threading
import shutil
from PyQt5.QtWidgets import *

from SinglePlayer import *
from Minecraft2D_ui import *

class Minecraft2D(QStackedWidget,Ui_Minecraft2D):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pb_singleplayer.clicked.connect(self.singleplayer)
        self.pb_back.clicked.connect(lambda:self.setCurrentIndex(0))
        self.pb_new.clicked.connect(lambda:self.setCurrentIndex(2))
        self.pb_cancel.clicked.connect(lambda:self.setCurrentIndex(1))
        self.pb_create.clicked.connect(self.create)
        self.pb_startgame.clicked.connect(lambda:self.startgame(self.lw_saves.currentItem().text()))
        self.pb_del.clicked.connect(lambda:self.setCurrentIndex(3))
        self.pb_no.clicked.connect(lambda:self.setCurrentIndex(1))
        self.pb_yes.clicked.connect(self.delsave)
        self.pb_edit.clicked.connect(self.editsave)
        self.pb_openfoder.clicked.connect(lambda:os.startfile(f'{os.getcwd()}/saves/{self.lw_saves.currentItem().text()}'))
        self.pb_done.clicked.connect(self.done)
        self.lw_saves.itemClicked.connect(self.choosesave)
        self.currentChanged.connect(self.changepage)
        self.set_lw_saves()

    def singleplayer(self):
        self.set_lw_saves()
        self.setCurrentIndex(1)

    def editsave(self):
        self.le_name.setText(self.lw_saves.currentItem().text())
        self.setCurrentIndex(4)

    def done(self):
        os.rename('saves/'+self.lw_saves.currentItem().text(),'saves/'+self.le_name.text())
        self.set_lw_saves()
        self.setCurrentIndex(1)

    def delsave(self):
        savename=self.lw_saves.currentItem().text()
        shutil.rmtree(f'saves/{savename}')
        self.set_lw_saves()
        self.setCurrentIndex(1)

    def changepage(self):
        self.pb_startgame.setEnabled(False)
        self.pb_edit.setEnabled(False)
        self.pb_del.setEnabled(False)

    def choosesave(self):
        self.pb_startgame.setEnabled(True)
        self.pb_edit.setEnabled(True)
        self.pb_del.setEnabled(True)

    def set_lw_saves(self):
        self.lw_saves.clear()
        for i in os.listdir('saves'):
            self.lw_saves.addItem(i)

    def create(self):
        self.startgame(self.le_savename.text())

    def startgame(self,savename):
        self.singleplayer=SinglePlayer(savename)
        self.singleplayer.Exit.connect(self.gameexit)
        t=threading.Thread(target=self.singleplayer.initworld)
        t.setDaemon(True)
        t.start()
        self.addWidget(self.singleplayer)
        self.setCurrentIndex(5)

    def gameexit(self):
        self.removeWidget(self.singleplayer)
        self.set_lw_saves()
        self.setCurrentIndex(1)

    def resizeEvent(self,e):
        self.label_logo.move(int((self.width()-self.label_logo.width())/2),self.label_logo.y())
        self.pb_singleplayer.move(int((self.width()-self.pb_singleplayer.width())/2),self.pb_singleplayer.y())
        self.le_savename.move(int((self.width()-self.le_savename.width())/2),self.le_savename.y())
        self.pb_create.move(self.le_savename.x(),self.pb_create.y())
        self.pb_cancel.move(self.le_savename.x()+128,self.pb_cancel.y())

if __name__=='__main__':
    app=QApplication(sys.argv)
    minecraft2d=Minecraft2D()
    minecraft2d.show()
    sys.exit(app.exec_())
