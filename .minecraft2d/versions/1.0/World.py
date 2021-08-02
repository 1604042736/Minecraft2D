class World:
    '''
    存储世界信息
    '''
    def __init__(self):
        self.ready=False    #是否准备好
        
    def connect(self,obj,type):
        '''
        将一个物品加入到世界中
        '''
        if type not in self.__dict__:
            self.__dict__[type]=[]
        #将世界与物品进行双向绑定
        self.__dict__[type].append(obj)
        #为防止obj中没有world变量,所以用__dict__添加
        obj.__dict__['world']=self

    def collision(self,a,b):
        '''
        碰撞检测
        '''
        x1=list(range(a.real_x,a.real_x+a.w))
        y1=list(range(a.real_y,a.real_y+a.h))
        x2=list(range(b.real_x,b.real_x+b.w))
        y2=list(range(b.real_y,b.real_y+b.h))
        setx=set(x1+x2)
        sety=set(y1+y2)
        if len(setx)==len(x1+x2) or len(sety)==len(y1+y2):
            return False
        return True
