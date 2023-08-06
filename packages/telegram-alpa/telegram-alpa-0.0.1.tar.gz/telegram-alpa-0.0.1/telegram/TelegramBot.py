#!/usr/bin/env python3

'''
TelegramBot.py
'''

import json
import logging
import requests

logger = logging.getLogger(__name__)


class TelegramBot():
    '''
    Python class for Telegram Bot API.

    https://core.telegram.org/bots/api
    '''
    bot_id = None
    _API_URL = "https://api.telegram.org/"
    _RETRY = 2  # how many time a message is resent if the return status is not "ok". Set to 0 to disable _RETRY
    _HTTP_TIMEOUT = 30

    def __init__(self, bot_id):
        self.bot_id = bot_id

    def getUpdates(self, offset=None, limit=None, timeout=0, allowed_updates=None):
        '''Send the getUpdates command to the Telegram API

        Useful for getting the chat_id of the group where this bot is a member of
        '''
        data = {}
        if limit:
            data['limit'] = int(limit)
        data['timeout'] = timeout
        if allowed_updates:
            data['allowed_updates'] = allowed_updates

        j = json.dumps(data)
        return self.post_cmd("getUpdates", j)

    def getMe(self):
        return self.send_cmd("getMe")

    @property
    def username(self):
        return self.getMe()['result']['username']

    @property
    def invitation_url(self):
        return "http://telegram.me/" + self.username

    @property
    def id(self):
        return self.getMe()['result']['id']

    def send_telegram(self, chat_id, message, muted=False, parse_mode=None):
        '''
        muted will turn on the disable_notification atribute (boolean)
        Sends the message silently. iOS users will not receive a notification, Android users will receive a notification with no sound.
        '''
        data = {}
        data['chat_id'] = chat_id
        if muted:
            data['disable_notification'] = True
        data['text'] = message
        if parse_mode == 'Markdown' or parse_mode == 'HTML':
            data['parse_mode'] = parse_mode

        j = json.dumps(data)

        msg_sent = False
        attempts = 0
        while not msg_sent and attempts <= self._HTTP_TIMEOUT:
            attempts += 1
            return_msg_json = self.post_cmd('sendMessage', j)
            return_msg = json.loads(return_msg_json)
            if return_msg['ok']:
                msg_sent = True

        if not msg_sent:
            logger.error("Failed to send message. Attempts: {}".format(attempts))
        return return_msg_json

    def send_cmd(self, cmd, as_json=True, raw=False):
        url = self._API_URL + "bot" + self.bot_id + "/" + cmd
        # print("URL: {}".format(url))
        try:
            r = requests.get(url, timeout=self._HTTP_TIMEOUT)
            r.connection.close()
            if raw:
                return r
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise Exception("Error connecting to {}: {}".format(url, e))

        if as_json:
            try:
                j = json.loads(r.content.decode())
                return j
            except (ValueError, AttributeError) as e:
                raise Exception("JSON loads error: {}".format(e))
        else:
            logger.debug("http_get: return text")
            return r.content.decode()

    def post_cmd(self, cmd, json_data, raw=False):
        url = self._API_URL + "bot" + self.bot_id + "/" + cmd
        try:
            # Don't use the the json=<> shortcut as we are using an old requests library
            # that doesnt support it (2.2.1)
            # r = requests.post(url, json=json_data, timeout=self._HTTP_TIMEOUT)
            # print(json_data)
            r = requests.post(url, data=json_data, headers={"content-type": "application/json"})
            r.connection.close()
            if raw:
                return r
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            result = {}
            result['ok'] = False
            result['description'] = "Connection Error: {}".format(e)
            return(json.dumps(result))

        return r.content.decode()

    # TODO
    # Methods in the Telegram Bot API that has not been implemented which might be useful
    # forwardMessage
    # kickChatMember
    # unbanChatMember
    # leaveChat
    def getChat(self, chat_id):
        '''
        Use this method to get up to date information about the chat (current name of the user for one-on-one
        conversations, current username of a user, group or channel, etc.). Returns a Chat object on success.
        '''
        data = {}
        data['chat_id'] = chat_id
        return self.post_cmd('getChat', json.dumps(data))

    def getChatAdministrators(self, chat_id):
        '''
        Use this method to get a list of administrators in a chat. On success, returns an Array of ChatMember
        objects that contains information about all chat administrators except other bots. If the chat is a
        group or a supergroup and no administrators were appointed, only the creator will be returned.
        '''
        data = {}
        data['chat_id'] = chat_id
        return self.post_cmd('getChatAdministrators', json.dumps(data))

    def getChatMembersCount(self, chat_id):
        '''
        Use this method to get the number of members in a chat. Returns Int on success.
        '''
        data = {}
        data['chat_id'] = chat_id
        return self.post_cmd('getChatMembersCount', json.dumps(data))

    def getChatMember(self, chat_id, user_id):
        '''
        Use this method to get information about a member of a chat. Returns a ChatMember object on success.
        '''
        pass


def main():
    pass


if __name__ == "__main__":
    main()
