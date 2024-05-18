from tokens import *
import telebot
import os
import subprocess
from urllib.parse import unquote

bot = telebot.TeleBot(bot_token)

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
            os.chdir('~/storage/movies/1ML')
            return
        sendme = 'sendme'
        if sendme in command:
            print(sendme, '- detected.')
            mkvname = command.replace(f'{sendme} ', '')
            print(2)
            if mkvname == sendme or mkvname == '':
                result = use_command('ls | grep .mkv')
                sm(result)
                return
            print(3)
            if '.mkv' not in mkvname: sm(f'{sendme} <имя файла.mkv>'); return 
            print(4)
            lsList = use_command('ls')
            if sendme in mkvname: mkvname.replect(sendme + ' ', '')
            print(f'"{mkvname}"', type(lsList))
            if mkvname not in lsList: sm('File not found.'); return
            print(f'"{mkvname}"')
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

def use_command(command : str):

    subprocess.run(command.split(), capture_output=True)
    output = subprocess.check_output(command)
    return unquote(output)

def sm(message):
    bot.send_message(rockxi, message)
    return message

bot.infinity_polling(20, True)