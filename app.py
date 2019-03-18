from telegram.ext import *
from random import randint, choice, shuffle
import re
import logging
import os
import time
import requests
from pyparsing import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

dice = Optional(Word(nums), default='1')+oneOf('k K d D')+oneOf('2 3 4 5 6 8 10 12 16 20 50 100')+Optional(oneOf('- + * /')+Word(nums))
cuda = {'ham':'hamrol(bot, update)',
        'ka':'answer(bot,update,\'🧻\')',
        'sushi':'answer(bot,update,\'🍣\')',
        'mlecz':'answer(bot,update,\'🥛\')'}

def start(bot, update):
    update.message.reply_text('Wystartowałem!')


def help(bot, update):
    update.message.reply_text('Masz do mnie jakiś problem?')

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def rollDice(t,n,m):
    nn=int(n)
    if(nn>1 or m):
        dtab=[]
        for each in range(int(nn)):
            dtab.append(randint(1,int(t)))
        dtab.sort()
        d='('
        for el in dtab:
            d+=str(el)+'+'
        d=d[:-1]+')'
        ret=evalRoll(d,m)
    else:
        ret=str(randint(1,int(t)))
    return ret
def evalRoll(r,m):
    s=r+m
    w=eval(s)
    s=s+'='+str(w)
    return s

def roll(bot, update, args):
    try:
        rzut=args[0]
    except IndexError:
        answer(bot, update, 'Ale czym mam rzucać?')
        rzut=''
    if(rzut):
        w=''
        if rzut in cuda.keys():
            eval(cuda[rzut])
        else:
            s=''
            for el in args:
                s=s+el
            rolls=''
            for result in dice.scanString(s):
                try:
                    m=result[0][3]+result[0][4]
                except IndexError:
                    m=''
                w=rollDice(result[0][2],result[0][0],m)
                rolls=rolls+w+', '
            if (rolls==''):
                w=requests.get('https://api.tenor.com/v1/random?key='+os.environ.get('KOSTKA_TENORAPI')+'&q=what&limit=1')
                answerGifUrl(bot,update,w.json()['results'][0]['media'][0]['gif']['url'])
            else:
                resp=rolls[:-2]
                answer(bot,update,resp)

def answer(bot, update, ans):
    if (update.message.from_user.username is None): tusername='Niewiadomokto'
    else: tusername=update.message.from_user.username
    ans='@'+tusername+': '+ans
    bot.sendMessage(chat_id=update.message.chat_id, text=ans)
def answerGifUrl(bot, update, url):
    if (update.message.from_user.username is None): tusername='Niewiadomokto'
    else: tusername=update.message.from_user.username
    ans='@'+tusername+': \"'+update.message.text+'\"'
    bot.sendMessage(chat_id=update.message.chat_id, text=ans)
    bot.send_animation(chat_id=update.message.chat_id, animation=url)

def hamrol(bot, update):
    if(update.message.chat.id==int(os.environ.get('KOSTKA_PRV'))):
        img=os.environ.get('KOSTKA_HAM')+choice(os.listdir(os.environ.get('KOSTKA_HAM')))
        bot.send_photo(chat_id=update.message.chat.id, photo=open(img, 'rb'))
    else:
        update.message.reply_text('nie znam człowieka...')
def addhamrol(bot, update):
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    fname=os.environ.get('KOSTKA_HAM')+str(int(time.time()))+'.jpg'
    newFile.download(fname)
    bot.sendMessage(chat_id=update.message.chat_id, text="zdjęcie dodane do zasobów, dziękuję")
def choosewho(bot, update):
    group=bot.get_chat_administrators(update.message.chat.id)
    mem=choice(group)
    ans='@'+mem.user.username
    answer(bot, update, ans)
def setorder(bot, update, args):
    try:
        rzut=args[1]
        shuffle(args)
        ans=''
        for el in args:
            ans+=el+' '
        answer(bot, update, ans)
    except IndexError:
        answer(bot, update, 'Ciężko mi coś takiego ogarnąć')

def main():

    updater = Updater(os.environ.get('KOSTKA_BOTID'))

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rzut", roll, pass_args=True))
    dp.add_handler(CommandHandler("roll", roll, pass_args=True))
    dp.add_handler(CommandHandler("kto", choosewho))
    dp.add_handler(CommandHandler("who", choosewho))
    dp.add_handler(CommandHandler("order", setorder, pass_args=True))
    dp.add_handler(MessageHandler(Filters.photo, addhamrol))
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
	main()
