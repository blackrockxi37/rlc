from tokens import *
import telebot
import os
import subprocess
from urllib.parse import unquote
from telebot import types


bot = telebot.TeleBot(bot_token)


@bot.callback_query_handler(func = lambda call: True)
def _ (call):
    if 'sendme' in call.data:
        mkvname = call.data.replace('sendme ', '')
        print(f'7:"{mkvname}"')
        f = open(mkvname, 'rb')
        print('sending...')
        bot.send_document(rockxi, f, timeout=200)
        print('sended')
        return


@bot.message_handler()
def _ (message):
    user_id = message.chat.id
    command = message.text
    
    if user_id != rockxi:
        bot.send_message(user_id, "Кря.")
        return

    try:
        if 'cd' in command:
                path = command.replace('cd ', '')
                print(command)
                os.chdir(path)
                out = sm(use_command('pwd'))
                return
        if command == 'course':
            os.chdir('/data/data/com.termux/files/home/storage/movies')
            sm(use_command('pwd'))
            return
        sendme = 'sendme'
        if sendme in command:
            if sendme == command:
                link_generator()
                return
            mkvname = command.replace(f'{sendme} ', '')
            if len(mkvname) == 3 and mkvname[1] == '.':
                mkvname = sm(use_command_os('ls | grep ' + mkvname))
                print(f'mkvname = "{mkvname}"')
            if '.mkv' not in mkvname: sm(f'{sendme} <имя файла.mkv>'); return
            print(1, mkvname)
            lsList = use_command_os('ls')
            if sendme in mkvname: mkvname.replect(sendme + ' ', '')
            if mkvname not in lsList: sm('File not found.'); return
            print(2, mkvname)
            f = open(mkvname, 'rb')
            print(3, f"{mkvname}")
            print('sending...')
            bot.send_document(rockxi, f, timeout=200)
            print('sended')
            return
        result = use_command(command)
        sm(result)
        print(command)
        


    except Exception as e:
        try:
            os.system(command)
            out = os.popen(command).read()
            if not out:
                out = '-> empty string <-'
            sm(out)
        except Exception as e:
            print(e)
            sm(str(e))

def use_command(command : str) -> str:
    subprocess.run(command.split(), capture_output=True)
    output = subprocess.check_output(command)
    return unquote(output)

def use_command_os(command : str) -> str:
    os.system(command)
    out = os.popen(command).read()
    if not out:
        out = '-> empty string <-'
    return out


def sm(message):
    bot.send_message(rockxi, message)
    return message

#wtf
def link_generator():
    ls = use_command_os('ls | grep mkv')
    print('lg1')
    ls = ls.splitlines()
    print('lg2')
    keyboard = types.InlineKeyboardMarkup()
    print('lg3')
    for i in ls:
        calldata = i.split()[1]
        print(calldata)
        keyboard.add(types.InlineKeyboardButton(text = i, callback_data=f'sendme {calldata}'))
    print('lg4')
    ls = '\n'.join(ls)
    print('lg5' + str(keyboard))
    bot.send_message(chatid= rockxi, text='Выберите файл:', reply_markup=keyboard)
    print('lg6')

bot.infinity_polling(20, True)