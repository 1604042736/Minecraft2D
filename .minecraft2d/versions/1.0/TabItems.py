import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Block import *
from HotBar import *

class TabItems:
    dev=36  #偏移
    def __init__(self):
        super().__init__()
        self.x,self.y=306,174
        self.hotbar_x,self.hotbar_y=325,399     #快捷栏的坐标
        self.image=QImage('res/gui/tab_items.png')
        self.block_tag=[]
        self.hotbar_tag=[None for i in range(9)]
        self.selected=None  #选择的方块
        self.set_block_tag()

    def set_block_tag(self):
        #第一个格子的坐标
        basic_x=x=325
        basic_y=y=210
        for i in os.listdir('data/block'):
            name=i.split('.')[0]
            tag={'name':name}
            tag['obj']=Block(x,y,32,32,name)
            self.block_tag.append(tag)
            x+=self.dev
            if x>basic_x+self.dev*8:  #超出范围
                x=basic_x
                y+=self.dev
