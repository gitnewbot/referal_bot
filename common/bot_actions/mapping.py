'''
Created on 23 июн. 2018 г.

@author: asobo
'''
import datetime

import logging
logger = logging.getLogger('referal_bot')

# from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError,OperationalError

from .. import config, Session
from ..models import Users,Projects,Proposition
from . import TITLES, BotKeyboardMain, get_message
from . import keyboard_main, keyboard_back, keyboard_cabinet, keyboard_referal, keyboard_reference,keyboard_run_project

from . import bot

# Состояния диалогао пользователя
STATE_MAIN = 0
STATE_0_ISO = 1
STATE_0_CABINET = 2
STATE_0_REFERAL = 3
STATE_0_REFERENCE = 4
STATE_1_RUN_PROJECT = 5
STATE_1_ARCHIVE = 6
STATE_1_PROPOSE = 7
STATE_2_ARCHIVE = 8
STATE_1_ETN = 9
STATE_1_EMAIL = 10

@bot.message_handler(commands=['start'])
def handle_start(message):
    
    try:
        chat_id = str(message.chat.id)
        
        logger.info('id[{}] START'.format(chat_id))
        
        session = Session()
        user = session.query(Users).filter_by(u_telegram_id=chat_id).first()
        if not user:
            user = Users(u_telegram_id = chat_id,
                         u_first_name = message.from_user.first_name,
                         u_last_name = message.from_user.last_name,
                         u_username = message.from_user.username,
                         u_regisger_date = datetime.datetime.utcnow())
            session.add(user)          
        user.u_dialog_state = STATE_MAIN
        
        # проверяем реферальную ссылку
        input_list = message.text.split(' ')
        if len(input_list)>1 and input_list[1]!=user.u_telegram_id:
            referal_id = input_list[1]
            user_perent = session.query(Users).filter_by(u_telegram_id=referal_id).first()
            if user_perent:
                user_perent.referals.append(user)      
             
        session.commit()

        answer_message,parse_mode = get_message('GREETING')
        
        bot.send_message(chat_id, text=answer_message, reply_markup=keyboard_main, parse_mode="Markdown")
    
    except Exception:
        logger.exception('id[{}] start error'.format(chat_id))
  
  
@bot.message_handler(content_types=["text"])
def handle_add(message):
    
    try:
        chat_id = message.chat.id
        chat_title = message.text
        
        session = Session()
        user = session.query(Users).filter_by(u_telegram_id=chat_id).first()
        if not user:
            user = Users(u_telegram_id = chat_id,
                         u_first_name = message.from_user.first_name,
                         u_last_name = message.from_user.last_name,
                         u_username = message.from_user.username,
                         u_regisger_date = datetime.datetime.utcnow())  
            session.add(user)      
            
        # если дальше не будет совпадений
        answer_message,parse_mode = get_message("ERROR")
        answer_keyboard = keyboard_main
        
        # базовый диалог
        if user.u_dialog_state == STATE_MAIN:   
            answer_keyboard = keyboard_main      
            
            if chat_title == TITLES['BUTTONS']['0_ISO']:
                # выводим список проектов
                project_keyboad = BotKeyboardMain()
                project_keyboad.createProject(get_projects(session).keys())
                
                answer_message,parse_mode = get_message('0_ISO')
                answer_keyboard = project_keyboad                
                user.u_dialog_state = STATE_0_ISO
            
            elif chat_title == TITLES['BUTTONS']['0_CABINET']:
                # Сразу видит сообщение, которое содержит текст + ID - 
                # (ID присваивается автоматически и один раз, навсегда к акку) и снизу 3 кнопки (ETH кошелек, Email адрес, Назад)
                answer_message,parse_mode = get_message('0_CABINET')
                answer_message += str(chat_id)
                answer_keyboard = keyboard_cabinet
                user.u_dialog_state = STATE_0_CABINET
             
            elif chat_title == TITLES['BUTTONS']['0_REFERAL_PROGRAM']:
                # выводим данные по реферальной программе
                answer_message,parse_mode = get_message('0_REFERAL_PROGRAM')
                answer_keyboard = keyboard_referal
                user.u_dialog_state = STATE_0_REFERAL
            
            elif chat_title == TITLES['BUTTONS']['0_REFERENCE']:
                # данные кабинета пользователя      
                answer_message,parse_mode = get_message('0_REFERENCE')
                bot.send_message(chat_id, text=answer_message, reply_markup=keyboard_reference, parse_mode=parse_mode)
                # сперва отправили ссылки, затем новую клавиатуру
                answer_message,parse_mode = get_message('1_SUPPORT')
                answer_keyboard = keyboard_back
                user.u_dialog_state = STATE_0_REFERENCE
         
        #======================================
        # вложенные уровни меню ISO
        #======================================        
        elif user.u_dialog_state == STATE_0_ISO:
            profict_dict = get_projects(session)
            
            if chat_title in profict_dict:
                answer_message = profict_dict[chat_title]
                answer_keyboard = keyboard_run_project
                user.u_dialog_state = STATE_1_RUN_PROJECT
                
            elif chat_title == TITLES['BUTTONS']['1_ARCHIVE']:
                # список архивных проектов
                project_keyboad = BotKeyboardMain()
                project_keyboad.createOldProject(get_projects(session, False).keys())
                
                answer_message,parse_mode = get_message('1_ARCHIVE')
                answer_keyboard = project_keyboad                
                user.u_dialog_state = STATE_1_ARCHIVE
                
            elif chat_title == TITLES['BUTTONS']['1_PROPOSE']:
                answer_message,parse_mode = get_message('1_PROPOSE')
                answer_keyboard = keyboard_back
                user.u_dialog_state = STATE_1_PROPOSE
                
            elif chat_title == TITLES['BUTTONS']['BACK']:
                
                answer_message = TITLES['BUTTONS']['BACK']
                answer_keyboard = keyboard_main
                user.u_dialog_state = STATE_MAIN
                
        elif user.u_dialog_state == STATE_1_RUN_PROJECT:
            
            if chat_title == TITLES['BUTTONS']['2_RUNT_PROJECT']:
                answer_message,parse_mode = get_message('2_RUNT_PROJECT')
                answer_keyboard = keyboard_back
                
            elif chat_title == TITLES['BUTTONS']['BACK']:
                project_keyboad = BotKeyboardMain()
                project_keyboad.createProject(get_projects(session).keys())
                
                answer_message,parse_mode = get_message('0_ISO')
                answer_keyboard = project_keyboad
                user.u_dialog_state = STATE_0_ISO
                
        elif user.u_dialog_state == STATE_1_ARCHIVE:
            profict_dict_old = get_projects(session,False)
            
            if chat_title in profict_dict_old:
                answer_message = profict_dict_old[chat_title]
                answer_keyboard = keyboard_back
                user.u_dialog_state = STATE_2_ARCHIVE
                
            elif chat_title == TITLES['BUTTONS']['BACK']:
                project_keyboad = BotKeyboardMain()
                project_keyboad.createProject(get_projects(session).keys())
                
                answer_message,parse_mode = get_message('0_ISO')
                answer_keyboard = project_keyboad
                user.u_dialog_state = STATE_0_ISO
                
        elif user.u_dialog_state == STATE_2_ARCHIVE:
            
            if chat_title == TITLES['BUTTONS']['BACK']:
                project_keyboad = BotKeyboardMain()
                project_keyboad.createOldProject(get_projects(session, False).keys())
                
                answer_message,parse_mode = get_message('1_ARCHIVE')
                answer_keyboard = project_keyboad                
                user.u_dialog_state = STATE_1_ARCHIVE
                
        elif user.u_dialog_state == STATE_1_PROPOSE:
            
            project_keyboad = BotKeyboardMain()
            project_keyboad.createProject(get_projects(session).keys())
            
            if chat_title == TITLES['BUTTONS']['BACK']:
                answer_message,parse_mode = get_message('0_ISO')
                answer_keyboard = project_keyboad
                user.u_dialog_state = STATE_0_ISO
                
            else:
                #TODO: сохранить предложение пользователя 2_PROPOSE
                answer_message,parse_mode = get_message('2_PROPOSE')
                answer_keyboard = project_keyboad
                user.u_dialog_state = STATE_0_ISO
                
                proposition = Proposition(pp_u_key=user.u_key, pp_proposition=chat_title, 
                                          pp_date=datetime.datetime.utcnow())
                session.add(proposition)
                
        #======================================
        # вложенные уровни меню Кабинет
        #======================================  
        
        elif user.u_dialog_state == STATE_0_CABINET:      
            
            if chat_title == TITLES['BUTTONS']['1_ETN']:
                if user.u_etn:
                    answer_message,parse_mode = get_message('1_ETN_GOOD')
                    answer_message = answer_message.format(user.u_etn)
                else:
                    answer_message,parse_mode = get_message('1_ETN_BAD')
                answer_keyboard = keyboard_back
                user.u_dialog_state = STATE_1_ETN   
                
            elif chat_title == TITLES['BUTTONS']['1_EMAIL']:
                if user.u_email:
                    answer_message,parse_mode = get_message('1_EMAIL_GOOD')
                    answer_message = answer_message.format(user.u_email)
                else:
                    answer_message,parse_mode = get_message('1_EMAIL_BAD')
                answer_keyboard = keyboard_back
                user.u_dialog_state = STATE_1_EMAIL          
            
            elif chat_title == TITLES['BUTTONS']['BACK']:
                
                answer_message = TITLES['BUTTONS']['BACK']
                answer_keyboard = keyboard_main
                user.u_dialog_state = STATE_MAIN
                
        elif user.u_dialog_state == STATE_1_ETN:
            
            answer_keyboard = keyboard_cabinet
            user.u_dialog_state = STATE_0_CABINET
            
            if chat_title == TITLES['BUTTONS']['BACK']:    
                answer_message = TITLES['BUTTONS']['BACK']
                   
            else: # сохраняем полученный кошелек
                user.u_etn = chat_title.strip()
                answer_message,parse_mode = get_message('1_ETN_AFTER_ADD')
                
        elif user.u_dialog_state == STATE_1_EMAIL:
            
            answer_keyboard = keyboard_cabinet
            user.u_dialog_state = STATE_0_CABINET
            
            if chat_title == TITLES['BUTTONS']['BACK']:    
                answer_message = TITLES['BUTTONS']['BACK']
                   
            else: # сохраняем полученный электронный адрес
                user.u_email = chat_title.strip()
                answer_message,parse_mode = get_message('1_EMAIL_AFTER_ADD')
                
                
        #======================================
        # вложенные уровни меню Партнерская программа
        #====================================== 
        elif user.u_dialog_state == STATE_0_REFERAL:
            
            if chat_title == TITLES['BUTTONS']['1_REFERAL_LINK']:  
                answer_message,parse_mode = get_message('1_REFERAL_LINK')
                answer_message += user.get_referal_link()
                answer_keyboard = keyboard_referal 
                
            elif chat_title == TITLES['BUTTONS']['1_REFERALS']:  
                answer_message,parse_mode = get_message('1_REFERALS')
                answer_message += str(len(user.referals))
                answer_keyboard = keyboard_referal    
                
            elif chat_title == TITLES['BUTTONS']['1_REWARD']:  
                answer_message,parse_mode = get_message('1_REWARD')
                answer_message += str(user.u_pay_sum)
                answer_keyboard = keyboard_referal        
            
            elif chat_title == TITLES['BUTTONS']['BACK']:
                
                answer_message = TITLES['BUTTONS']['BACK']
                answer_keyboard = keyboard_main
                user.u_dialog_state = STATE_MAIN
                    
        #======================================
        # вложенные уровни меню Партнерская программа
        #======================================     
        elif user.u_dialog_state == STATE_0_REFERENCE:
            answer_keyboard = keyboard_main
            user.u_dialog_state = STATE_MAIN 
            
            if chat_title == TITLES['BUTTONS']['BACK']:
                answer_message = TITLES['BUTTONS']['BACK']
                
            else:
                answer_message,parse_mode = get_message('1_SUPPORT_COMPLETE')
                support_message = 'support message {}\n-----\nfrom user @{}\n-----\n{}'.format(
                    config['TELEGRAM']['BOT_NAME'],user.u_username,chat_title)
                bot.send_message(config['APPLICATION']['SUPPORT_ID'],support_message, parse_mode="Markdown")
                
            
        # если не нашли подходящее сообщение, обнуляем статус и возвращаемся в главное меню
        if answer_message == get_message("ERROR"):
            user.u_dialog_state = STATE_MAIN    
            
               
        session.commit()
        bot.send_message(chat_id, text=answer_message, reply_markup=answer_keyboard, parse_mode=parse_mode)
        
    except Exception:
        logger.exception('id[{}] add error'.format(chat_id))
        
    finally:
        session.close()
            
#TODO: это бы в модель            
def get_projects(session, active=True):
    
    project_list = session.query(Projects).filter_by(p_active = active).all()
    project_dict = {}
    for project in project_list:
        name = '{}, {}/{}'.format(project.p_name,project.p_saved_sum,project.p_full_sum)
        project_dict[name] = project.p_description
       
    return project_dict 

    
    
    
