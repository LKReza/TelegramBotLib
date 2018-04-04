# coding=utf8
import time
import logger
import traceback
import object_result
import settings_manager
import telegram_bot_api as tba

from threading import Thread, Lock


def tba_warpper(func):
    def wrapper(self, *args, **kwargs):
        try:
            self.logger.info('{}: {} {}'.format(
                func.__name__, args, kwargs
            ))
            start = time.time()
            result = func(self, *args, **kwargs)
            end = time.time()
            self.logger.success(str(func.__name__), end - start)
            if self.disable_object_result:
                return result
            return object_result.ObjectResult(result).data
        except Exception as e:
            self.logger.exception(e)
            return None

    return wrapper


class TelegramBot(object):
    def __init__(self, name, token, root_dir, disable_object_result=False):
        self.name = name
        self.token = token
        self.logger = logger.Logger(name, root_dir)
        self.disable_object_result = disable_object_result
        self.settings = settings_manager.SettingsManager(name, root_dir)
        self.get_updates_mutex = Lock()

    @tba_warpper
    def get_me(self):
        return tba.get_me(self.token)

    @tba_warpper
    def send_message(self, chat_id, text):
        return tba.send_message(self.token, chat_id, text)

    @tba_warpper
    def get_updates(self, offset):
        return tba.get_updates(self.token, offset)

    def checking_updates(self, callback, delay=10, raise_on_error=False):
        offset = 0
        while True:
            with self.get_updates_mutex:
                updates = self.get_updates(offset) or []

            for i, update in enumerate(updates):
                if update.get('message') and update.get('update_id'):
                    offset = update.get('update_id') + 1
                    try:
                        callback(update.get('message'))
                    except Exception as e:
                        trace = traceback.format_exc()
                        self.logger.exception(e)
                        self.logger.traceback(trace)
                        if raise_on_error:
                            raise
            time.sleep(delay)

    def async_checking_updates(self, callback, delay=10, raise_on_error=False):
        thread = Thread(target=self.checking_updates, args=(callback, delay, raise_on_error))
        thread.start()
        return thread

    def working(self, worker, delay=10, raise_on_error=False):
        while True:
            try:
                worker()
            except Exception as e:
                trace = traceback.format_exc()
                self.logger.exception(e)
                self.logger.traceback(trace)
                if raise_on_error:
                    raise
            time.sleep(delay)

    def async_working(self, worker, delay=10, raise_on_error=False):
        thread = Thread(target=self.checking_updates, args=(worker, delay, raise_on_error))
        thread.start()
        return thread
