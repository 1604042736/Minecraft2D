from PyQt5.QtGui import *

class HotBar:
    def __init__(self,x,y,w,h,image,obj=None):
        self.real_x,self.real_y=x,y
        self.w,self.h=w,h
        self.image=QImage(image)
        self.obj=obj
