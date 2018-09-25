'''
Created on 26 апр. 2018 г.

@author: asobo
'''
import json

from telebot import types

from ..bot_actions import TITLES

class BotKeyboardInline(types.InlineKeyboardMarkup):

    def __init__(self):
        super().__init__()
        
    def createReferenceInline(self):
                
        self.add(types.InlineKeyboardButton(text=TITLES['BUTTONS']['1_AGREEMENT'],
                                            url=TITLES['MESSAGES']['1_AGREEMENT']))
        self.add(types.InlineKeyboardButton(text=TITLES['BUTTONS']['1_INSTRUCTION'],
                                            url=TITLES['MESSAGES']['1_INSTRUCTION']))
        self.add(types.InlineKeyboardButton(text=TITLES['BUTTONS']['1_EVENT'],
                                            url=TITLES['MESSAGES']['1_EVENT']))
                    
            
class BotKeyboardMain(types.ReplyKeyboardMarkup):
    
    def createMain(self):
        self.add(types.KeyboardButton(TITLES['BUTTONS']['0_ISO']))
        self.add(types.KeyboardButton(TITLES['BUTTONS']['0_CABINET'])) 
        self.add(types.KeyboardButton(TITLES['BUTTONS']['0_REFERAL_PROGRAM']))
        self.add(types.KeyboardButton(TITLES['BUTTONS']['0_REFERENCE']))  

        
    def createBack(self):
        self.add(types.KeyboardButton(TITLES['BUTTONS']['BACK']))
        

    def _create_project(self,project_list):
        key_list = []
        for project_name in project_list:
            if len(key_list)==2:
                self.add(*key_list)
                key_list = []
            key_list.append(project_name)
            
        if key_list:
            self.add(*key_list)

        
    def createProject(self,project_list):
        self._create_project(project_list) 
        self.add(types.KeyboardButton(TITLES['BUTTONS']['1_ARCHIVE']),
                 types.KeyboardButton(TITLES['BUTTONS']['1_PROPOSE']),
                 types.KeyboardButton(TITLES['BUTTONS']['BACK'])) 

       
    def createOldProject(self,project_list): 
        self._create_project(project_list)          
        self.add(types.KeyboardButton(TITLES['BUTTONS']['BACK']))        
        
        
    def createCabinet(self):
        self.add(types.KeyboardButton(TITLES['BUTTONS']['1_ETN'])) 
        self.add(types.KeyboardButton(TITLES['BUTTONS']['1_EMAIL']))
        self.add(types.KeyboardButton(TITLES['BUTTONS']['BACK']))
        
        
    def createReferal(self):
        self.add(types.KeyboardButton(TITLES['BUTTONS']['1_REFERAL_LINK'])) 
        self.add(types.KeyboardButton(TITLES['BUTTONS']['1_REFERALS']))
        self.add(types.KeyboardButton(TITLES['BUTTONS']['1_REWARD']))
        self.add(types.KeyboardButton(TITLES['BUTTONS']['BACK']))


    def createRunProject(self):
        self.add(types.KeyboardButton(TITLES['BUTTONS']['2_RUNT_PROJECT'])) 
        self.add(types.KeyboardButton(TITLES['BUTTONS']['BACK']))
        
        