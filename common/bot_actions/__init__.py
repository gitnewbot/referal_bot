import os
import json

from telebot import types, TeleBot
from .. import config

bot = TeleBot(config['TELEGRAM']['BOT_KEY'], num_threads=config.getint('TELEGRAM','BOT_WORKER_COUNT'))

def load_titles():
    
    if os.path.exists('data/titles.json'):
        with open('data/titles.json','r',encoding='utf-8') as file:
            titles = json.loads(file.read())
    else:
        titles = {}    
    return titles

def get_message(field_name):
    
    result = ''
    parse_mode = None
    if field_name in TITLES['MESSAGES']:
        message_list = TITLES['MESSAGES'][field_name]
        if len(message_list)>1: 
            if message_list[0]==0:
                result = message_list[1]
            else: # загружаем текст из файла
                file_name = os.path.join('data',message_list[1])
                if os.path.exists(file_name):
                    with open(file_name,'r',encoding='utf-8') as file:
                        result = file.read()
                        if message_list[0]==2:
                            parse_mode="Markdown"
                        elif message_list[0]==3:
                            parse_mode="html"
            
    return result,parse_mode

TITLES = load_titles()

from .cBotKeyboard import BotKeyboardMain,BotKeyboardInline

keyboard_main = BotKeyboardMain(resize_keyboard=True)
keyboard_main.createMain()

keyboard_back = BotKeyboardMain(row_width=1, resize_keyboard=True)
keyboard_back.createBack()

keyboard_cabinet = BotKeyboardMain(resize_keyboard=True)
keyboard_cabinet.createCabinet()

keyboard_referal = BotKeyboardMain(resize_keyboard=True)
keyboard_referal.createReferal()

keyboard_reference = BotKeyboardInline()
keyboard_reference.createReferenceInline()

keyboard_run_project = BotKeyboardMain(resize_keyboard=True)
keyboard_run_project.createRunProject()

from . import mapping

