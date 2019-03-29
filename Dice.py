from random import randint, choice, shuffle, seed
from time import time
import os, fnmatch

class Dice:


    def __init__(self):
        self.__hampath=''
        self.__mana=time()-3600
        self.__prvchat=''
        self.__special_dices={'ham':'_hamrol',
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
        seed(time())
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
            func='self.'+self.special_dices[key][1:]+'()'
            if (self.__prvchat==chatid):
                return eval(func)
            else:
                print(chatid)
                print(self.__prvchat)
                return ['t','to nie na telefon takie rozmowy']
        else:
            return ['t',self.special_dices[key]]

    def rollImg(self,path):
        img=choice(fnmatch.filter(os.listdir(path), '*.jpg'))
        return path+img


    #above this line there are special dices functions
    def hamrol(self):
        if (self.__hampath==''):
            return ['t','Coś poległo w konfiguracji...']
        if (self.__mana>time()):
            return ['t','Mam za mało many na tak potężny czar. Musisz poczekać']
        self.__mana=time()+10
        return ['p',self.rollImg(self.__hampath)]
