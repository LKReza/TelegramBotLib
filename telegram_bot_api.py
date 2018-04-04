# coding=utf8
import errors
import requests


def get_method_url(method_name, bot_token):
    return 'https://api.telegram.org/bot{}/{}'.format(
        bot_token, method_name
    )


def send_get_request(url, data=None):
    data = data or {}
    try:
        response = requests.get(url, data)

        if response.status_code != 200:
            raise errors.ErrorMethodResponseCode(response.status_code)

        json_data = response.json()

        if not json_data or 'ok' not in json_data:
            raise errors.EmptyResponseData('Empty response')

        if not json_data['ok'] or 'result' not in json_data:
            raise errors.ErrorResponseMethod(json_data.get('error', 'None'))

        return json_data['result']

    except ValueError as e:
        raise errors.UnknowResponseDataFormat(e)

    except requests.exceptions.RequestException as e:
        raise errors.CannotSendMethodRequest(e)


def get_me(bot_token):
    url = get_method_url('getMe', bot_token)
    return send_get_request(url)


def get_updates(bot_token, offset):
    url = get_method_url('getUpdates', bot_token)
    return send_get_request(url, {'offset': offset})


def send_message(bot_token, chat_id, message):
    url = get_method_url('sendMessage', bot_token)
    return send_get_request(url, {'chat_id': chat_id, 'text': message})
