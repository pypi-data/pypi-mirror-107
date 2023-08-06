#!/usr/bin/env python3
#-*-coding:utf-8-*-

import os
import logging
import logging.config
import json
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver
from logging.handlers import RotatingFileHandler

__version__ = "0.9.6"
__author__ = 'IoT Team'
__credits__ = 'L-mobile solutions'

current_path = os.path.dirname(__file__)
config = current_path + "/logger4py.json"

def load_logging_configuration():
    try:
        with open(config, 'r') as f:
            config_log = json.load(f)
            #print(config_log)
        logging.config.dictConfig(config_log)
    except Exception as e:
        logging.basicConfig\
        (   level=logging.DEBUG
        ,   format='%(asctime)s.%(msecs)03d\t%(levelname)-s\t%(thread)d\t%(process)d\t%(module)s\t%(message)s'
        ,   datefmt='%Y-%m-%dT%H:%M:%S'
        ,   handlers=[RotatingFileHandler('default.log', maxBytes=10485760, backupCount=20)]
        )

class MyHandler(PatternMatchingEventHandler): 
    def on_modified(self, event):
        print ("file modified " + event.src_path)
        load_logging_configuration()
      
def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()

@singleton
class Logger():
    def __init__(self):
        path = current_path + '/logger4py.json'
        event_log = MyHandler()
        observer = PollingObserver()
        observer.schedule(event_log, path, recursive=False)
        observer.start()
        # logging.config.dictConfig(config_log)
        load_logging_configuration()
 
    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        return logger

