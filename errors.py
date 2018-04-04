# coding=utf8


class TelegramBotLibException(Exception):
    def __init__(self, e):
        self.message = '[{}]: {}'.format(type(e).__name__, e)

    def __str__(self):
        return self.message


class CannotSendMethodRequest(TelegramBotLibException):
    pass


class ErrorMethodResponseCode(TelegramBotLibException):
    def __init__(self, code):
        self.message = 'Response code {}'.format(code)


class UnknowResponseDataFormat(TelegramBotLibException):
    pass


class EmptyResponseData(TelegramBotLibException):
    pass


class ErrorResponseMethod(TelegramBotLibException):
    def __init__(self, text):
        self.message = '{}'.format(text)
