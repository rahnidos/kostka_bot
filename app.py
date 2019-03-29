from telegram.ext import *
import logging, os, time, requests
from pyparsing import *
from Dice import *

#logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
#type of dices and dice notation
dices = Optional(Word(nums), default='1')+oneOf('k K d D')+oneOf('2 3 4 5 6 8 10 12 16 20 50 100')+Optional(oneOf('- + * /')+Word(nums))
#special "dices"
#telegram bot functions
def start(bot, update):
    update.message.reply_text('Wystartowałem!')
def help(bot, update):
    update.message.reply_text('Masz do mnie jakiś problem?')
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
def answer(bot, update, ans):
    ans='@'+findUserName(bot,update)+': '+ans
    bot.sendMessage(chat_id=update.message.chat_id, text=ans)
def answerPhoto(bot, update, path):
    bot.send_photo(chat_id=update.message.chat.id, photo=open(path, 'rb'))
def answerGifUrl(bot, update, url):
    ans='@'+findUserName(bot,update)+': \"'+update.message.text+'\"'
    bot.sendMessage(chat_id=update.message.chat_id, text=ans)
    bot.send_animation(chat_id=update.message.chat_id, animation=url)
def info(bot, update):
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
        answer(bot, update, 'Ale czym mam rzucać?')
        rzut=''
    if(rzut):
        w=''
        if rzut in dice.special_dices.keys():
            result=dice.rollSpecial(rzut,update.message.chat.id)
            if (result[0]=='t'):
                answer(bot,update,result[1])
            elif (result[0]=='p'):
                answerPhoto(bot,update,result[1])
        else:
            s=''
            for el in args:
                s=s+el
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
    fname=os.environ.get('KOSTKA_HAM')+str(int(time.time()))+'.jpg'
    newFile.download(fname)
    bot.sendMessage(chat_id=update.message.chat_id, text="zdjęcie dodane do zasobów, dziękuję")
def choosewho(bot, update):
    group=bot.get_chat_administrators(update.message.chat.id)
    mem=choice(group)
    if (mem.user.username is None): ans=mem.user.last_name
    else: ans='@'+mem.user.username
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

dice=Dice()
dice.hampath=os.environ.get('KOSTKA_HAM')
dice.prvchat=int(os.environ.get('KOSTKA_PRV'))
def main():

    updater = Updater(os.environ.get('KOSTKA_BOTID'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rzut", roll, pass_args=True))
    dp.add_handler(CommandHandler("roll", roll, pass_args=True))
    dp.add_handler(CommandHandler("kto", choosewho))
    dp.add_handler(CommandHandler("who", choosewho))
    dp.add_handler(CommandHandler("i", info))
    #dp.add_handler(CommandHandler("t", test))
    dp.add_handler(CommandHandler("order", setorder, pass_args=True))
    dp.add_handler(MessageHandler(Filters.photo, addhamrol))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
	main()
