import threading
import time
from copy import *
from PyQt5.QtCore import *
from PIL import Image,ImageQt

class Player:
    '''
    玩家类
    '''
    def __init__(self,x,y,w,h,image):
        self.real_x,self.real_y,self.w,self.h=x,y,w,h
        self.x,self.y=x,y
        #将原图片切割,并存到数组中
        img=Image.open(image)
        self.move_image=[ImageQt.ImageQt(img.crop((i*32,0,i*32+32,64))) for i in range(12)]
        self.move_index=0
        self.image=self.move_image[self.move_index]   #当前图片
        #控制
        self.control={'up':Qt.Key_W,'down':Qt.Key_S,'right':Qt.Key_D,'left':Qt.Key_A,'destroy':Qt.LeftButton,'build':Qt.RightButton,}
        for i in range(1,10):
            self.control[f'hotbar_{i}']=Qt.__dict__[f'Key_{i}']
        self.control_state={}
        for key,val in self.control.items():
            self.control_state[val]=False
        self.speed=10   #速度
        self.gravity=4  #重力
        self.jump=False #是否跳跃
        self.inity=self.y  #跳跃时的初始高度
        self.t=threading.Thread(target=self.move)
        self.t.setDaemon(True)
        self.t.start()

    def move(self):
        #一直等到准备好后开始
        while not('world' in self.__dict__ and self.world.ready):pass
        while True:
            self.build_block=self.hotbars[self.selected_hotbar].obj #放置的方块
            stop=True   #是否将move_index归零
            touch=False #是否碰到地面
            for key in ['block']:
                for obj in self.world.__dict__[key]:
                    obj.real_y-=self.gravity
            self.y-=self.gravity
            for key in ['block']:
                for obj in self.world.__dict__[key]:
                    if obj.display and self.world.collision(self,obj):
                        add=self.real_y+self.h-(obj.real_y+self.gravity)
                        for k in ['block']:
                            for o in self.world.__dict__[k]:
                                o.real_y=o.real_y+self.gravity-add
                        self.y=self.y+self.gravity-add
                        touch=True
                        break
                    
            if self.jump:
                for key in ['block']:
                    for obj in self.world.__dict__[key]:
                        obj.real_y+=self.gravity*2
                self.y+=self.gravity*2
                for key in ['block']:
                    for obj in self.world.__dict__[key]:
                        if obj.display and self.world.collision(self,obj):
                            add=obj.real_y-self.gravity*2+obj.h-self.real_y
                            for k in ['block']:
                                for o in self.world.__dict__[k]:
                                    o.real_y=o.real_y-self.gravity*2+add
                            self.y=self.y-self.gravity*2+add
                            self.jump=False #碰到障碍物停止跳跃
                            break
                if self.y>=self.inity+32:   #只跳1格
                    self.jump=False
                    
            if self.control_state[self.control['right']]:
                for key in ['block']:
                    for obj in self.world.__dict__[key]:
                        obj.real_x-=self.speed
                self.x+=self.speed
                #判断是否碰撞
                for key in ['block']:
                    for obj in self.world.__dict__[key]:
                        if obj.display and self.world.collision(self,obj):
                            add=obj.real_x+self.speed-self.real_x-self.w   #计算相差的位置
                            for k in ['block']:
                                for o in self.world.__dict__[k]:
                                    o.real_x=o.real_x+self.speed-add #让人物正好碰到方块
                            self.x=self.x-self.speed+add
                            break
                self.move_index=(self.move_index+1)%12
                self.image=self.move_image[self.move_index]
                stop=False
            if self.control_state[self.control['left']]:
                for key in ['block']:
                    for obj in self.world.__dict__[key]:
                        obj.real_x+=self.speed
                self.x-=self.speed
                #判断是否碰撞
                for key in ['block']:
                    for obj in self.world.__dict__[key]:
                        if obj.display and self.world.collision(self,obj):
                            add=self.real_x-(obj.real_x-self.speed+obj.w)   #计算相差的位置
                            for k in ['block']:
                                for o in self.world.__dict__[k]:
                                    o.real_x=o.real_x-self.speed+add #让人物正好碰到方块
                            self.x=self.x+self.speed-add
                            break
                self.move_index=(self.move_index+1)%12
                self.image=self.move_image[self.move_index]
                stop=False
            if self.control_state[self.control['up']]and touch: #只有当碰地后才能再次起跳
                self.inity=self.y
                self.jump=True
            if self.control_state[self.control['destroy']]:
                if self.lookblock[-1]!=None:
                    self.lookblock[-1].display=False
            if self.control_state[self.control['build']]:
                if self.lookblock[-1]!=None and self.build_block!=None:
                    if not self.world.collision(self,self.lookblock[-1]) and not self.lookblock[-1].display:   #玩家占有的地方不能放方块,已有方块的地方不能放方块
                        real_x,real_y=self.lookblock[-1].real_x,self.lookblock[-1].real_y
                        x,y=self.lookblock[-1].x,self.lookblock[-1].y
                        self.lookblock[-1].copy(self.build_block)
                        self.lookblock[-1].real_x=real_x
                        self.lookblock[-1].real_y=real_y
                        self.lookblock[-1].x=x
                        self.lookblock[-1].y=y
                        self.lookblock[-1].w=32
                        self.lookblock[-1].h=32
                        self.lookblock[-1].display=True
            for i in range(1,10):
                if self.control_state[self.control[f'hotbar_{i}']]:
                    self.selected_hotbar=i-1
            if stop:
                self.move_index=0
                self.image=self.move_image[self.move_index]
            time.sleep(0.01)

    def save(self,file):
        return [f'Player:{self.real_x},{self.real_y},{self.x},{self.y}']
        
