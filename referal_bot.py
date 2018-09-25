#! venv/bin/python3

import time
import os
import sys

from common.bot_actions import bot

import logging
import logging.config
# логирование
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('referal_bot')
     
def run():
  
    while True:  
        try:
            logger.critical('critical start')
            logger.info('info start')
            logger.debug('debug start')
            logger.error('error start')

            bot.polling(none_stop=True) 
            
        except (KeyboardInterrupt, SystemExit):
            logger.critical('SystemExit')
            raise SystemExit

        except Exception as ex:
            logger.error('error, {}'.format(ex))
            logger.critical('error, {}'.format(ex))
            time.sleep(10)
        finally:
            logger.critical('stop')
        
if __name__ == '__main__':
    run()
    