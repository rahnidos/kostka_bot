from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint
import re
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Wystartowałem!')


def help(bot, update):
    update.message.reply_text('Tutaj przyjdzie kiedyś help')

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def dice_replace(match):
    arg=match.group()
    kosci=arg.split('k')
    try:
        liczba=int(kosci[0])
    except ValueError:
        liczba=1
    kmax=int(kosci[1])
    wynik=''
    if(liczba>1):
        for x in range(0,liczba):
            if (x==0): wynik='('+str(randint(1,kmax))
            else: wynik=wynik+'+'+str(randint(1,kmax))
        wynik=wynik+')'
    else: wynik=str(randint(1,kmax))

    return wynik

def roll(bot, update, args):
    try:
        rzut=args[0]
    except IndexError:
        update.message.reply_text('Ale czym mam rzucać?')
        rzut=''
    if(rzut):
        rzut = re.sub('(\d+)?k\d+',dice_replace,rzut)
        try:
            wrzut=int(rzut)
        except ValueError:
            wrzut = rzut+'='+str(eval(rzut))
        update.message.reply_text(str(wrzut))

def main():

    updater = Updater("")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rzut", roll, pass_args=True))
    dp.add_handler(CommandHandler("roll", roll, pass_args=True))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
main()