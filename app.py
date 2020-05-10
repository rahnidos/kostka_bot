from telegram.ext import *
from time import time
import logging, os, requests
from pyparsing import *
from Dice import *
from texts import *


#logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
#type of dices and dice notation
dices = Optional(Word(nums), default='1')+oneOf('k K d D')+Word(nums)+Optional(oneOf('- + * /')+Word(nums))
#special "dices"
#telegram bot functions
def start(bot, update):
    update.message.reply_text(comm['stared'])
def help(bot, update):
    update.message.reply_text(helptxt)
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
def answer(bot, update, ans):
    ans='@'+findUserName(bot,update)+': '+ans
    bot.sendMessage(chat_id=update.message.chat_id, text=ans)
def answerPhoto(bot, update, path, caption):
    bot.send_photo(chat_id=update.message.chat.id, photo=open(path, 'rb'), caption=caption)
def answerPhotoRaw(bot, update, img, caption):
    bot.send_photo(chat_id=update.message.chat.id, photo=img, caption=caption)
def answerGifUrl(bot, update, url):
    ans='@'+findUserName(bot,update)+': \"'+update.message.text+'\"'
    bot.sendMessage(chat_id=update.message.chat_id, text=ans)
    bot.send_animation(chat_id=update.message.chat_id, animation=url)
def info(bot, update):

    bot.send_photo(chat_id=update.message.chat_id, photo='https://raw.githubusercontent.com/rahnidos/kostka_bot/master/coins/head.png')
    
    print(update.message)
def findUserName(bot,update):
    tusername=update.message.from_user.first_name
    if (update.message.from_user.last_name): tusername=update.message.from_user.last_name
    if (update.message.from_user.username): tusername=update.message.from_user.username
    return tusername
def roll(bot, update, args):
    try:
        rzut=args[0]
    except IndexError:
        answer(bot, update, comm['nodice'])
        rzut=''
    if(rzut):
        w=''
        if rzut in dice.special_dices.keys():
            if(str(update.message.from_user.id) == os.environ.get('KOSTKA_PRVROLLER')):
                dice.set_prvroller(True)
            else:
                dice.set_prvroller(False)
            result=dice.rollSpecial(rzut,update.message.chat.id)
            if (result[0]=='t'):
                answer(bot,update,result[1])
            elif (result[0]=='p'):
                try:
                    caption=result[2]
                except IndexError:
                    caption=''
                answerPhoto(bot,update,result[1],caption)
        else:
            s=''
            for el in args:
                s=s+el+' '
            rolls=''
            for result in dices.scanString(s):
                try:
                    m=result[0][3]+result[0][4]
                except IndexError:
                    m=''
                #print(result[0][2],result[0][0],m)
                w=dice.rollDices(result[0][2],result[0][0],m,result[0][1])
                rolls=rolls+w+', '
            if (rolls==''):
                w=requests.get('https://api.tenor.com/v1/random?key='+os.environ.get('KOSTKA_TENORAPI')+'&q=what&limit=1')
                answerGifUrl(bot,update,w.json()['results'][0]['media'][0]['gif']['url'])
            else:
                resp=rolls[:-2]
                answer(bot,update,resp)

def addhamrol(bot, update):
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    fname=os.environ.get('KOSTKA_HAM')+str(int(time()))+'.jpg'
    newFile.download(fname)
    bot.sendMessage(chat_id=update.message.chat_id, text=comm['phadded'])

def choosewho(bot, update):
    group=bot.get_chat_administrators(update.message.chat.id)
    mem=dice.listchoice(group)
    ans=mem.user.first_name
    if (mem.user.last_name): ans=mem.user.last_name
    if (mem.user.username): ans=mem.user.username
    answer(bot, update, ans)
def answerczy(bot, update):
    ans=dice.listchoice(verd)
    answer(bot, update, ans)
def rpsCh(bot, update):
    ans=dice.listchoice(rps)
    answer(bot, update, ans)
def rpslsCh(bot, update):
    ans=dice.listchoice(rpsls)
    answer(bot, update, ans)
def card(bot, update, args):
    try:
        arg=args[0]
    except IndexError:
        arg=1
    try:
        liczba=int(arg)
    except ValueError:
        liczba=1

    answerPhotoRaw(bot, update, dice.drawCards(liczba), '')
def coin(bot, update, args):
    try:
        set=args[0]
    except IndexError:
        set='none'
    result=dice.flipCoin(set)
    answerPhoto(bot, update, result[1], result[2])
def setorder(bot, update, args):
    try:
        rzut=args[1]
        ans=''
        for el in dice.shufflelist(args):
            ans+=el+' '
        answer(bot, update, ans)
    except IndexError:
        answer(bot, update, comm['nunderstand'])

dice=Dice()
dice.hampath=os.environ.get('KOSTKA_HAM')
dice.prvchat=int(os.environ.get('KOSTKA_PRV'))

def main():

    updater = Updater(os.environ.get('KOSTKA_BOTID'), use_context=False)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rzut", roll, pass_args=True))
    dp.add_handler(CommandHandler("roll", roll, pass_args=True))
    dp.add_handler(CommandHandler("card", card, pass_args=True))
    dp.add_handler(CommandHandler("coin", coin, pass_args=True))
    dp.add_handler(CommandHandler("kto", choosewho))
    dp.add_handler(CommandHandler("who", choosewho))
    dp.add_handler(CommandHandler("czy", answerczy))
    dp.add_handler(CommandHandler("rps", rpsCh))
    dp.add_handler(CommandHandler("rpsls", rpslsCh))
    dp.add_handler(CommandHandler("i", info))
    dp.add_handler(CommandHandler("order", setorder, pass_args=True))
    dp.add_handler(MessageHandler(Filters.photo, addhamrol))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
	main()
