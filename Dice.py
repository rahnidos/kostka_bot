from random import randint, choice, shuffle, seed
from time import time, localtime, strftime
import os
from texts import *
class Dice:


    def __init__(self):
        self.__hampath=''
        self.__lastseed=0
        self.__mana=time()
        self.__prvchat=''
        self.__special_dices={'ham':'_hamrol()',
                'coin': '_specimglist(\'./coins/\')',
                'czy' : '_speclist(verd)',
                'card': '_specimglist(\'./cards/\')',
                'ka':'🧻',
                'sushi':'🍣',
                'mlecz':'🥛'}

    def get_special_dices(self):
        return self.__special_dices
    def set_hampath(self,value):
        if(os.path.isdir(value)):
            self.__hampath=value
    def get_hampath(self):
        return __hampath
    def set_prvchat(self,value):
        self.__prvchat=value
    def get_prvchat(self):
        return self.__prvchat

    hampath=property(get_hampath,set_hampath)
    special_dices=property(get_special_dices)
    prvchat=property(get_prvchat,set_prvchat)

    def rollDices(self,type,number,mods,dkeep):
        nn=int(number)
        if (int(type)>1024): type='1024'
        if (nn>100): nn=100
        if (self.__lastseed==time()):
            seed(time())
            self.__lastseed=time()
        if (dkeep=='D' or dkeep=='K'): reroll=1
        else: reroll=0
        dtab=[]
        for each in range(int(nn)):
            dtab.extend(self.rollDice(int(type),reroll))
        dtab.sort()
        rresult='('
        for el in dtab:
            rresult+=str(el)+'+'
        rresult=rresult[:-1]+')'
        ret=self.evalRolls(rresult,mods)
        return ret

    def rollDice(self,itype,reroll):
        tmp_ret=[]
        roll=randint(1,itype)
        tmp_ret.append(roll)
        if (reroll==1 and roll==itype):
            tmp_ret.extend(self.rollDice(itype,1))
        return tmp_ret

    def evalRolls(self,rresult,mods):
        rsum=rresult+mods
        w=eval(rsum)
        rsum=rsum+'='+str(w)
        return rsum

    def rollSpecial(self,key,chatid):
        if (self.special_dices[key][0]=='_'):
            func='self.'+self.special_dices[key][1:]
            if (self.__prvchat==chatid):
                return eval(func)
            else:
                return ['t',comm['noprv']]
        else:
            return ['t',self.special_dices[key]]

    def rollImg(self,path):
        seed(time())
        valid_images = [".jpg",".gif",".png"]
        imgs=[]
        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            imgs.append(f)
        img=choice(imgs)
        return path+img

    def shufflelist(self,list):
        shuffle(list)
        return list

    def listchoice(self,list):
        return choice(list)
    

    #above this line there are special dices functions
    def hamrol(self):
        if (self.__hampath==''):
            return ['t',comm['conferr']]
        elif (self.__mana>time()):
            return ['t',comm['nemana']]
        umana=randint(1,3600)
        self.__mana=time()+umana
        newtime=localtime(self.__mana)
        return ['p',self.rollImg(self.__hampath),comm['cooldown']+str(umana)+'s ('+strftime("%H:%M:%S",newtime)+')']

    def speclist(self,list):
        return ['t',choice(list)]
    def specimglist(self,path):
        img=self.rollImg(path)
        return ['p',img]
