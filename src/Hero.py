# API info
from src.variables import API_HASH, API_ID, PHONE
# Constants
from src.settings import ru_bot, eu_bot, debug_bot, time_before_def, time_in_forest
# Lists
from src.settings import activities_ru, battle_table_ru, emoji_list
# Functions
from src.settings import defend_check

from src.logger import Logger

import datetime
import os
import random
import sys
import time

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.types import (
    UpdateNewMessage, UpdateNewChannelMessage,
    UpdateShortChatMessage, UpdateShortMessage)


# Hero state
# 0 — idle
# 1 — busy
# 2 — wind
# 3 — forced command
# 4 — defending
# 5 — attacking
# -1 — blocked
class State:
    IDLE = 0
    BUSY = 1
    WIND = 2
    FORCED = 3
    DEF = 4
    ATT = 5
    BLOCKED = -1


class Hero:
    def __init__(self, user, data):

        self.logger = Logger(user)

        super().__init__('sessions/' + user, API_ID, API_HASH, update_workers=4)

        self.phone = PHONE

        self.chats = {}

        self.state = State.IDLE

        self.level = 0

        self.exhaust = time.time()

        # Adventure quest location
        self.adventure = None

        # All locations
        self.locations = create_locations()

        self.logger.log('Сеанс {} открыт'.format(user))

    def connect_with_code(self):
        """
        Connect to tg and recieve a code
         """

        connected = self.connect()
        if not connected:
            raise ConnectionError

        if not self.is_user_authorized():
            print('Первый запуск. Запрашиваю код...')
            self.send_code_request(self.phone)

            code_ok = False
            while not code_ok:
                code = input('Введите полученный в Телеграме код: ')
                code_ok = self.sign_in(self.phone, code)

            # Выходим, чтобы запросить код в следующем боте
            sys.exit('Код верный! Перезапускай {}.'.format(self.user))

    def update_handler(self, update):
        ''' Recieve and handle messages '''

        if isinstance(update, UpdateNewMessage):
            self.acknowledge(update.message, update.message.from_id)

        elif isinstance(update, UpdateShortMessage):
            self.acknowledge(update, update.user_id)

        elif isinstance(update, UpdateShortChatMessage):
            self.acknowledge(update, update.from_id)

        else:
            pass

    def set_state(self, state):
        ''' Sets hero state '''
        # Blocked state always free
        if state == State.BLOCKED:
            pass

        elif self.state == State.ATT:
            if state != State.IDLE and state != State.WIND:
                return False

        elif self.state == State.DEF:
            if state != State.IDLE and state != State.WIND and state != State.ATT:
                return False

        elif self.state == State.FORCED:
            if state != State.IDLE and state != State.WIND:
                return False

        elif self.state == State.WIND:
            if state != State.IDLE:
                return False

        elif self.state == State.BUSY:
            if state != State.IDLE and state != State.WIND:
                return False

        elif self.state == State.IDLE:
            pass

        elif self.state == State.BLOCKED:
            if state != State.IDLE:
                return False

        self.logger.log('Меняю состояние c {} на {}'.format(self.state, state))
        self.state = state
        return True

    def acknowledge(self, message, from_id):
        ''' Sends messages in functions '''
        if self.state == State.BLOCKED:
            return

        time.sleep(2)

        if from_id == self.chats[ru_bot]:
            self.game(message)
            self.send_read_acknowledge(ru_bot, message)




