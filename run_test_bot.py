# coding=utf8
import os
import sys
import telegram_bot


class TestBot(telegram_bot.TelegramBot):
    def __init__(self, token):
        super(TestBot, self).__init__('test_bot', token, os.path.expanduser('~'))

    def message_handler(self, message):
        if not message.text:
            return

        if message.text == '/start':
            self.send_message(message.chat.id, u'Привет')

        elif message.text == '/name':
            result = self.get_me()
            self.send_message(message.chat.id, u'Меня зовут {} :)'.format(result.first_name))

    def start(self):
        self.checking_updates(self.message_handler)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python run_test_bot.py <telegram_bot_token>')
        sys.exit(-1)

    test_bot = TestBot(sys.argv[1])
    test_bot.start()
