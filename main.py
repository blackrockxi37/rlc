from tokens import *
import telebot
import os
import subprocess
from urllib.parse import unquote

bot = telebot.TeleBot(bot_token)

@bot.message_handler()
def _ (message):
    user_id = message.chat.id
    command = message.text.strip()
    if user_id != rockxi:
        bot.send_message(user_id, "Кря.")
        return

    try:
        if 'cd' in command:
                os.chdir(command.split()[1])
                out = sm(use_command('pwd'))
                return
        result = use_command(command)
        sm(result)
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