from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from . import config

Base = declarative_base()
    
class Projects(Base):
    __tablename__ = 'projects'
    p_key = Column(Integer, primary_key=True)
    p_name = Column(String(32), index=True, unique=True)
    p_description = Column(String(256))
    p_saved_sum = Column(Float)
    p_full_sum = Column(Float)
    p_active = Column(Boolean,default = True)
        
    
class Users(Base):
    __tablename__ = 'users'
    u_key = Column(Integer, primary_key=True)
    u_telegram_id = Column(String(32), index=True, unique=True)
    u_first_name = Column(String(32))
    u_last_name = Column(String(32))
    u_username = Column(String(32))
    u_parent_key = Column(Integer, ForeignKey('users.u_key')) 
    u_dialog_state = Column(Integer, default = 0)
    u_pay_sum = Column(Float, default = 0)
    u_etn = Column(String(32))
    u_email = Column(String(32))
    u_regisger_date = Column(DateTime)
    referals = relationship("Users")
    
    def get_referal_link(self):
        
        return 'https://t.me/{}?start={}'.format(
            config['TELEGRAM']['BOT_NAME'],self.u_telegram_id)
    
    
class Proposition(Base):
    __tablename__ = 'proposition'
    pp_key = Column(Integer, primary_key=True)
    pp_proposition = Column(String(256))
    pp_u_key = Column(Integer, ForeignKey('users.u_key')) 
    pp_date = Column(DateTime) 
    
    

    
    
    
    
