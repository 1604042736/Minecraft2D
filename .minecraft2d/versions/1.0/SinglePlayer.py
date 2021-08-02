import sys
import time
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from World import *
from Player import *
from Block import *
from HotBar import *
from Bag import *

class SinglePlayer(QWidget):
    Exit=pyqtSignal()
    def __init__(self,savename):
        super().__init__()
        self.setWindowTitle('SinglePlayer')
        self.resize(1000,618)
        self.initsize=[1000,618]    #初始大小
        self.savename=savename  #存档名称
        
        QFontDatabase.addApplicationFont('res/font/minecraft.ttf')
        #状态显示
        self.label_state=QLabel(self)
        self.label_state.resize(256,32)
        self.label_state.setAlignment(Qt.AlignCenter)
        self.label_state.setFont(QFont("minecraft",16))

        self.bag=Bag(self)
        self.bag.resize(32*10,32*5)
        self.bag.move(int((self.width()-self.bag.width())/2),int((self.height()-self.bag.height())/2))
        self.bag.close()

        self.frame_timeout=QFrame(self)
        self.frame_timeout.resize(256,256)
        self.frame_timeout.move(int((self.width()-self.frame_timeout.width())/2),int((self.height()-self.frame_timeout.height())/2))
        self.vbox=QVBoxLayout()
        self.pb_backtogame=QPushButton('回到游戏',self.frame_timeout)
        self.pb_backtogame.clicked.connect(self.backtogame)
        self.pb_exit=QPushButton('退出',self.frame_timeout)
        self.pb_exit.clicked.connect(self.closeEvent)
        self.vbox.addWidget(self.pb_backtogame)
        self.vbox.addWidget(self.pb_exit)
        self.frame_timeout.setLayout(self.vbox)
        self.frame_timeout.close()
        
        self.debugmode=False    #调试模式
        self.bagmode=False  #有无打开背包
        self.timeout=False #暂停
        self.mousepos=[None,None]
        self.fps=0
        self.count=0
        self.world=World()

    def backtogame(self):
        self.timeout=False
        self.frame_timeout.close()

    def closeEvent(self,e):
        self.save()
        self.Exit.emit()
        self.close()

    def initworld(self):
        '''
        初始化世界
        '''
        #世界还未创建
        if not os.path.exists(f'saves/{self.savename}'):
            self.world.connect(Player(480,288,32,64,'res/skin/player.png'),'player')
            for i in range(30):
                for j in range(20):
                    self.label_state.setText(f'正在初始化世界{int((i*20+j)/600*100)}%')
                    if j*32==352:
                        block=Block(i*32,j*32,32,32,'grass')
                    elif j*32>352 and j*32<480:
                        block=Block(i*32,j*32,32,32,'dirt')
                    else:
                        block=Block(i*32,j*32,32,32,'stone')
                    if j*32<=341:
                        block.display=False
                    self.world.connect(block,'block')
            #快捷栏
            x=int((self.width()-32*9)/2)
            y=self.height()-32
            self.hotbars=[HotBar(x+i*32,y,32,32,'res/gui/hotbar.png') for i in range(9)]
            for i in range(9):
                if f'0_{i}' in self.bag.block_tag:
                    self.hotbars[i].obj=self.bag.block_tag[f'0_{i}']
            self.world.player[0].__dict__['hotbars']=self.hotbars
            self.world.player[0].__dict__['selected_hotbar']=0 #当前选择的快捷栏
            self.lookblock=[None,None,None,None,None]    #看的方块
            self.world.player[0].__dict__['lookblock']=self.lookblock
            self.world.ready=True
            self.label_state.hide()
        else:
            self.readData()

        self.setMouseTracking(True)
        self.t=threading.Thread(target=self.display)
        self.t.setDaemon(True)
        self.t.start()

    def paintEvent(self,e):
        if self.world.ready:
            qp=QPainter()
            qp.begin(self)
            for obj in self.world.block:
                if obj.display:
                    qp.drawImage(QRect(obj.real_x,obj.real_y,obj.w,obj.h),obj.image)
            for obj in self.world.player:
                qp.drawImage(QRect(obj.real_x,obj.real_y,obj.w,obj.h),obj.image)
            if self.lookblock[-1]!=None:
                qp.drawRect(*self.lookblock[:-1])

            for hotbar in self.world.player[0].hotbars:
                qp.drawImage(QRect(hotbar.real_x,hotbar.real_y,hotbar.w,hotbar.h),hotbar.image)
                if hotbar.obj:
                    qp.drawImage(QRect(hotbar.real_x+5,hotbar.real_y+5,hotbar.w-10,hotbar.h-10),QImage(hotbar.obj.image))

            selected_hotbar= self.world.player[0].hotbars[self.world.player[0].selected_hotbar]
            qp.drawImage(QRect(selected_hotbar.real_x,selected_hotbar.real_y,selected_hotbar.w,selected_hotbar.h),QImage('res/gui/selected_hotbar.png'))
                
            if self.debugmode:
                qp.setFont(QFont('minecraft', 8))
                qp.setPen(QColor(0,0,0))
                qp.drawText(QRect(0,0,256,16),Qt.AlignLeft,'Minecraft2D [Python Version %d.%d.%d]'%(sys.version_info[0],sys.version_info[1],sys.version_info[2]))
                qp.drawText(QRect(0,16,256,16),Qt.AlignLeft,f'FPS: {self.fps}')
                qp.drawText(QRect(0,48,256,16),Qt.AlignLeft,f'Player Position: {self.world.player[0].x} {self.world.player[0].y}')
                if self.lookblock[-1]:
                    qp.drawText(QRect(0,80,256,16),Qt.AlignLeft,f'Block Position: {self.lookblock[-1].x} {self.lookblock[-1].y}')
                    qp.drawText(QRect(0,96,256,16),Qt.AlignLeft,f'Block Name: {self.lookblock[-1].name}')
                qp.drawRect(self.world.player[0].real_x,self.world.player[0].real_y,self.world.player[0].w,self.world.player[0].h)
            qp.end()

    def keyPressEvent(self,e):
        if self.world.ready:
            if e.key()==Qt.Key_F3:
                self.debugmode=not self.debugmode
            elif e.key()==Qt.Key_E:
                if self.bagmode:
                    self.bag.close()
                else:
                    self.bag.show()
                self.bagmode=not self.bagmode
            elif e.key()==Qt.Key_Escape:
                if self.timeout:
                    self.frame_timeout.close()
                else:
                    self.frame_timeout.show()
                self.timeout=not self.timeout
            elif not self.bagmode and e.key()in self.world.player[0].control_state:
                self.world.player[0].control_state[e.key()]=True

    def keyReleaseEvent(self,e):
        if self.world.ready:
            if not self.bagmode and e.key()in self.world.player[0].control_state:
                self.world.player[0].control_state[e.key()]=False

    def mouseMoveEvent(self,e):
        self.mousepos=[e.x(),e.y()]
        if self.world.ready and not self.bagmode:
            for obj in self.world.block:
                if e.x()>=obj.real_x and e.x()<=obj.real_x+obj.w and e.y()>=obj.real_y and e.y()<=obj.real_y+obj.h:
                    self.lookblock[0]=obj.real_x
                    self.lookblock[1]=obj.real_y
                    self.lookblock[2]=obj.w
                    self.lookblock[3]=obj.h
                    self.lookblock[4]=obj
                    return
            self.lookblock[-1]=None

    def mousePressEvent(self,e):
        if self.world.ready and not self.bagmode:
            if e.button()in self.world.player[0].control_state:
                self.world.player[0].control_state[e.button()]=True
        elif self.bagmode:
            #获取鼠标点击的快捷栏
            for hotbar in self.hotbars:
                if self.mousepos[0]>=hotbar.real_x and self.mousepos[0]<=hotbar.real_x+hotbar.w and self.mousepos[1]>=hotbar.real_y and self.mousepos[1]<=hotbar.real_y+hotbar.h:
                    if self.bag.selected:   #背包中选中了
                        r,c=self.bag.selected
                        if f'{r}_{c}' in self.bag.block_tag:
                            hotbar.obj=self.bag.block_tag[f'{r}_{c}']
                    break

    def mouseReleaseEvent(self,e):
        if self.world.ready and not self.bagmode:
            if e.button()in self.world.player[0].control_state:
                self.world.player[0].control_state[e.button()]=False

    def resizeEvent(self,e):
        if self.world.ready:
            x,y=self.world.player[0].real_x,self.world.player[0].real_y
            #保持人物居中
            self.world.player[0].real_x=int((self.width()-self.world.player[0].w)/2)
            self.world.player[0].real_y=int((self.height()-self.world.player[0].h)/2)
            for obj in self.world.block:
                obj.real_x+=(self.world.player[0].real_x-x)
                obj.real_y+=(self.world.player[0].real_y-y)
            #保持快捷栏居中
            self.world.player[0].hotbars[0].real_x=int((self.width()-32*9)/2)
            self.world.player[0].hotbars[0].real_y=self.height()-32
            for i in range(1,9):
                self.world.player[0].hotbars[i].real_x=self.world.player[0].hotbars[0].real_x+i*32
                self.world.player[0].hotbars[i].real_y=self.world.player[0].hotbars[0].real_y
            self.bag.move(int((self.width()-self.bag.width())/2),int((self.height()-self.bag.height())/2))
            self.frame_timeout.move(int((self.width()-self.frame_timeout.width())/2),int((self.height()-self.frame_timeout.height())/2))
        else:
            self.label_state.move(int((self.width()-self.label_state.width())/2),int((self.height()-self.label_state.height())/2))

    def display(self):
        start=time.perf_counter()
        while True:
            self.update()
            time.sleep(0.01)
            self.count+=1
            if self.count==60:
                end=time.perf_counter()
                self.fps=self.count/(end-start)
                self.count=0

    def save(self):
        if not os.path.exists(f'saves/{self.savename}'):#世界没有创建就生成文件夹:
            os.mkdir(f'saves/{self.savename}')
        with open(f'saves/{self.savename}/world.txt',mode='w',encoding='utf-8')as file:
            for key,val in self.world.__dict__.items():
                if isinstance(val,list):
                    for obj in val:
                        for i in obj.save(file):
                            file.write(i+'\n')

    def readData(self):
        lines=open(f'saves/{self.savename}/world.txt',encoding='utf-8').readlines()
        i=0
        for line in lines:
            self.label_state.setText(f'正在初始化世界{int(i/len(lines)*100)}%')
            a=line.split(':')
            b=a[-1].split(',')
            if a[0]=='Player':
                player=Player(int(b[0]),int(b[1]),32,64,'res/skin/player.png')
                player.x,player.y=int(b[2]),int(b[3])
                self.world.connect(player,'player')
            elif a[0]=='Block':
                block=Block(int(b[0]),int(b[1]),32,32,b[2])
                block.display=bool(int(b[3]))
                block.x,block.y=int(b[4]),int(b[5])
                self.world.connect(block,'block')
            i+=1
        x=int((self.width()-32*9)/2)
        y=self.height()-32
        self.hotbars=[HotBar(x+i*32,y,32,32,'res/gui/hotbar.png') for i in range(9)]
        for i in range(9):
            if f'0_{i}' in self.bag.block_tag:
                self.hotbars[i].obj=self.bag.block_tag[f'0_{i}']
        self.world.player[0].__dict__['hotbars']=self.hotbars
        self.world.player[0].__dict__['selected_hotbar']=0 #当前选择的快捷栏
        self.lookblock=[None,None,None,None,None]    #看的方块
        self.world.player[0].__dict__['lookblock']=self.lookblock
        self.world.ready=True
        self.label_state.hide()
