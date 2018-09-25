#! venv/bin/python3
import sys
import os
import csv

from common import Session
from common.models import Projects,Users

DELIMETER = ';'
USER_FILE = 'data/users.csv'
PROJECT_FILE = 'data/projects.csv'

def help():
    print('Выбирите одну из комманд:')
    for key,value in command_dict.items():
        print('    {} - {}'.format(key,value[1])) 


def get_users():
    session = Session()
    user_list = session.query(Users).all()
    with open(USER_FILE, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=DELIMETER, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['key','telegram_id','first_name','last_name','username',
                            'parent_key','dialog_state','pay_sum','etn','email','date','referal_count','referal_list'])
        for user in user_list:
            spamwriter.writerow([user.u_key,
                                user.u_telegram_id,
                                user.u_first_name,
                                user.u_last_name,
                                user.u_username,
                                user.u_parent_key, 
                                user.u_dialog_state,
                                user.u_pay_sum,
                                user.u_etn,
                                user.u_email,
                                user.u_regisger_date,
                                len(user.referals),
                                ','.join([referal.u_telegram_id for referal in user.referals])])
    
    print('Файл с пользователями {} получен'.format(USER_FILE))    
    session.close()
    
    
def get_projects():
    session = Session()
    project_list = session.query(Projects).all()
    with open(PROJECT_FILE, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=DELIMETER, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['key','name','description','saved_sum','full_sum','active'])
        for project in project_list:
            spamwriter.writerow([project.p_key,
                                 project.p_name,
                                 project.p_description,
                                 project.p_saved_sum,
                                 project.p_full_sum,
                                 1 if project.p_active else 0])
    
    print('Файл с проектами {} получен'.format(PROJECT_FILE))    
    session.close()
    
    
def save_users():
    session = Session()
    if os.path.exists(USER_FILE):
        with open(USER_FILE, newline='') as csvfile:
            index = 0
            spamreader = csv.reader(csvfile, delimiter=DELIMETER, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in spamreader:
                index += 1
                if index == 1:
                    continue
                (u_key,u_telegram_id,u_first_name,u_last_name,u_username,u_parent_key,
                 u_dialog_state,u_pay_sum,u_etn,u_email,u_date,u_referal_count,u_referal_list) = row
                user = session.query(Users).filter_by(u_key=u_key).first()
                if user:
                    user.u_pay_sum = u_pay_sum
                    #user.u_etn = u_etn
                    #user.u_email = u_email
                    session.commit()
                else:
                    print('Пользователь с ключем {} не найден'.format(u_key))                    
        print('Сохранение пользователей в базу данных завершено')
    else:
        print('файл {} не найден, сперва необходимо его сохранить коммандой get_users'.format(USER_FILE))
    session.close()
    
    
def save_projects():
    session = Session()
    if os.path.exists(PROJECT_FILE):
        with open(PROJECT_FILE, newline='') as csvfile:
            index = 0
            spamreader = csv.reader(csvfile, delimiter=DELIMETER, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in spamreader:
                index += 1
                if index == 1:
                    continue
                p_key,p_name,p_description,p_saved_sum,p_full_sum,p_active = row
                # обновляем существующий проект
                if p_key:
                    project = session.query(Projects).filter_by(p_key=p_key).first()
                    if project:
                        project.p_name = p_name
                        project.p_description = p_description
                        project.p_saved_sum = float(0 if not p_saved_sum else p_saved_sum)
                        project.p_full_sum = float(0 if not p_full_sum else p_full_sum)
                        project.p_active = True if p_active=='1' else False
                    else:
                        print('Проект {} с ключем {} не найден'.format(p_name,p_key))
                # создаем новый проект
                else:
                    project = Projects(p_name=p_name,
                                       p_description = p_description,
                                       p_saved_sum = float(0 if not p_saved_sum else p_saved_sum),
                                       p_full_sum = float(0 if not p_full_sum else p_full_sum),
                                       p_active = True if p_active=='1' else False)
                    session.add(project)
                session.commit()                   
        print('Сохранение проектов в базу данных завершено')
    else:
        print('файл {} не найден, сперва необходимо его сохранить коммандой get_projects'.format(PROJECT_FILE))
    session.close()
    
    
def msg():
    msg_data = input('Введите сообщение для рассылки:\n')
    from common.bot_actions import bot
    
    session = Session()
    users = session.query(Users).all()
    for user in users:
        try:
            bot.send_message(user.u_telegram_id, msg_data)
        except:
            pass
    
    session.close()


command_dict = {
    'get_users':[get_users,'получить список пользователей из базы данных'],
    'save_users':[save_users,'сохранить в базу список пользователей с откоректированными суммами'],
    'get_projects':[get_projects,'получить список проектов из базы данных'],
    'save_projects':[save_projects,'сохранить в базу список проектов '],
    'msg':[msg,'разослать сообщение всем пользователям'],
    }


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) == 2 else None
    
    if command and command in command_dict:
        command_dict[command][0]()
    else:
        help()