import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Block import *

class Bag(QTabWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.p=parent
        self.setBlocktag()
        self.selected=None

    def setBlocktag(self):
        self.block_tag={}
        self.block_tag_table=QTableWidget(3,9,self)
        self.block_tag_table.verticalHeader().setVisible(False)
        self.block_tag_table.horizontalHeader().setVisible(False)
        self.block_tag_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.block_tag_table.cellClicked.connect(self.block_tag_table_cellClicked)
        self.block_tag_table.__dict__['keyPressEvent']=self.p.keyPressEvent #因为它被点击后父窗口接受不到消息,所以将它的消息连接到父窗口的消息上
        for i in range(3):
            self.block_tag_table.setColumnWidth(i,32)
            self.block_tag_table.setRowHeight(i,32)
        for i in range(9):
            self.block_tag_table.setColumnWidth(i,32)
            self.block_tag_table.setRowHeight(i,32)
        self.addTab(self.block_tag_table,"方块")

        i,j=0,0
        for block in os.listdir('data/block'):
            self.block_tag[f'{i}_{j}']=Block(0,0,0,0,block.split('.')[0])
            label=QLabel(self)
            label.setScaledContents(True)
            label.setPixmap(QPixmap(self.block_tag[f'{i}_{j}'].data['image']))
            self.block_tag_table.setCellWidget(i,j,label)
            j+=1
            if j==9:
                j=0
                i+=1

    def block_tag_table_cellClicked(self,r,c):
        self.selected=[r,c]
        print(r,c)
