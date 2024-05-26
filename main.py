from tokens import *
import telebot
import os
import subprocess
from urllib.parse import unquote
from telebot import types


bot = telebot.TeleBot(bot_token)
msid = 0

@bot.callback_query_handler(func = lambda call: True)
def _ (call):
    try:
        if 'sendme' in call.data:
            mkvnum = call.data.replace('sendme ', '')
            path = mkvnum.split()[1]
            mkvnum = mkvnum.split()[0]
            print('path = ', path)
            current_path = use_command_os('pwd')
            if path not in current_path:
                os.chdir('/data/data/com.termux/files/home/storage/movies/' + path)
            ls = use_command_os('ls | grep mkv')
            ls = ls.splitlines()
            mkvname = ls[0]
            for i in ls:
                if mkvnum in i:
                    mkvname = i
                    break
            f = open(mkvname, 'rb')
            print('sending...')
            msid = bot.send_message('Отправляю...')
            bot.send_document(rockxi, f, timeout=200)
            bot.delete_message(chat_id=rockxi, message_id=msid)
            print('sended')
            return
    except Exception as e:
        sm(str(e))


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
                if path == '~':
                    os.chdir('/data/data/com.termux/files/home')
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
            lsList = use_command_os('ls')
            if sendme in mkvname: mkvname.replect(sendme + ' ', '')
            if mkvname not in lsList: sm('File not found.'); return
            f = open(mkvname, 'rb')
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
    ls = ls.splitlines()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    path = use_command_os('pwd')
    path = path.replace('/storage/emulated/0/Movies/', '')
    for i in ls:
        calldata = i.split()[0]
        keyboard.add(types.InlineKeyboardButton(text = i, callback_data=f'sendme {calldata} {path}'))
    ls = '\n'.join(ls)
    bot.send_message(chat_id=rockxi, text='Выберите файл:', reply_markup=keyboard)


#pollingpollingpollingpollingpollingpollingpollingpollingpollingpollingpollingpollingpollingpolling
bot.infinity_polling(20, True)