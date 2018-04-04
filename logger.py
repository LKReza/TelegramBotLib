# coding=utf8
import os

from datetime import datetime


class Logger(object):
    def __init__(self, name, logs_root_dir):
        self.name = name
        self.logs_dir = os.path.join(
            logs_root_dir,
            name,
            'logs'
        )

        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

    def info(self, text):
        self.__logging('INFO', text)

    def call(self, text):
        self.__logging('CALL', text)

    def success(self, text, work_time=None):
        if work_time:
            self.__logging('SUCCESS', '{} by {}s'.format(text, work_time))
        else:
            self.__logging('SUCCESS', text)

    def time(self, func, work_time):
        self.__logging('TIME', '{}: {}'.format(func.__name__, work_time))

    def error(self, text):
        self.__logging('ERROR', text)

    def exception(self, e):
        self.__logging('EXCEPTION', '{}: {}'.format(
            type(e).__name__, e
        ))

    def traceback(self, text):
        self.__logging('TRACEBACK', '\n{}\n{}'.format(
            text, '-' * 80
        ))

    def __logging(self, block, text):
        logfile = '{}_{}.log'.format(datetime.now().strftime('%d-%m-%Y'), self.name)
        logfile = os.path.join(self.logs_dir, logfile)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not os.path.exists(self.logs_dir):
            os.mkdir(self.logs_dir)

        print('[{}]\t{{{}}}\t{}\n'.format(block, timestamp, text))
        with open(logfile, 'a') as out:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            out.write('[{}]\t{{{}}}\t{}\n\n'.format(
                block, timestamp, text
            ))
