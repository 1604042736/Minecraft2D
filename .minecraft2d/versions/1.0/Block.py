import json
from copy import *
from PyQt5.QtGui import *

class Block:
    datas={}   #存储已加载的方块
    def __init__(self,x,y,w,h,name):
        self.real_x,self.real_y,self.w,self.h=x,y,w,h
        self.x,self.y=x,y
        self.name=name
        if name not in self.datas:
            self.data=json.load(open(f'data/block/{name}.json',encoding='utf-8'))
            self.datas[name]=self.data
        else:
            self.data=self.datas[name]
        self.image=QImage(self.data['image'])
        self.display=True

    def copy(self,other):
        '''
        复制方块
        '''
        self.real_x=other.real_x
        self.real_y=other.real_y
        self.x,self.y=other.x,other.y
        self.name=other.name
        self.data=deepcopy(other.data)
        self.image=other.image

    def save(self,file):
        return [f'Block:{self.real_x},{self.real_y},{self.name},{int(self.display)},{self.x},{self.y}']
