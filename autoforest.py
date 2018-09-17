# coding=utf-8

__author__ = 'SergySanJj'

"""
Autobot for ChatWars.
"""

from pytg import Telegram

from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine

import time
import datetime
import logging
import math
import json

# logs everything connected with tg-cli into console
# logging.basicConfig(level=logging.DEBUG)

# path to telegram-cli dir:
tg_cli_dir = "/loc/to/tg/"

ru_bot = "@ChatWarsBot"
eu_bot = "@chtwrsbot"

debug_bot = "@ChatGrinding_bot"

time_before_def = 30 * 60

# True if free
hero_state = True

# use next command in tg/bin/:
# ./telegram-cli --json -P 4458
# after what port 4458 will be opened


activities_ru = {
    'forest': u"🌲Лес",
    'def': u"🛡Защита",
    'fight': u"▶️Быстрый бой",
    'hero': u"🏅Герой"}

activities_eu = {
    'forest': "🌲Forest",
    'def': "🛡Defend",
    'fight': "▶️Fast fight"}

states_ru = {
    'rest': u"🛌Отдых",
    'def': u"🛡Защита"}

message_types_ru = {
    'main': u"Уровень"}

battle_table_ru = [
    datetime.datetime.strptime("01:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("17:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("23:58:00", "%H:%M:%S")]

battle_table_eu = [
    datetime.datetime.strptime("02:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("10:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("18:00:00", "%H:%M:%S")]


# returns time difference in seconds
def diff(start, end):
    start_sec = start.hour * 3600 + start.minute * 60 + start.second
    end_sec = end.hour * 3600 + end.minute * 60 + end.second
    return (end_sec - start_sec)


# returns True if it's time to defend
def defend_check():
    curr_time = datetime.datetime.now()
    closest = 10000000000
    for t in battle_table_ru:
        differ = diff(curr_time, t)
        # print(differ)
        if differ > 0 and closest > differ:
            closest = differ
    print("Closest battle", closest)
    if closest < time_before_def:
        return True
    return False


def state_check(receiver, sender):
    # message = activities_ru['hero']
    sender.send_msg(ru_bot, u"🏅Герой")
    # time.sleep(3)
    receiver.start()
    receiver.message(state_handler(sender))
    receiver.stop()
    return hero_state


def update_state(receiver, sender):
    sender.send_msg(ru_bot, activities_ru['hero'])


@coroutine
def state_handler(sender):
    quit = False
    try:
        while not quit:  # loop for messages
            msg = (yield)
            sender.status_online()  # so we will stay online.

            if msg.event != "message":
                continue  # is not a message.
            if msg.text is None:  # we have media instead.
                continue

            if msg.text is not None:
                if msg.sender.username == 'ChatWarsBot':
                    print(msg['text'])
                    if message_types_ru['main'] in msg['text']:
                        print("Main message:")
                        if states_ru['rest'] in msg['text']:
                            print("Resting")
                            hero_state = True
                        if states_ru['def'] in msg['text']:
                            print("Defing")
                            hero_state = False
                        else:
                            print("Busy")
                            hero_state = False
                    quit = True


    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C/Ctrl+Z)
        pass
    except TypeError:
        pass
    else:
        # the loop exited without exception, becaues _quit was set True
        pass
    print("Busy")
    hero_state = False


def main_cycle(receiver, sender):
    while True:
        update_state(receiver=receiver, sender=sender)

        print("hero state", hero_state)
        if defend_check():
            # if True:
            # sender.status_online()
            if state_check(receiver=receiver, sender=sender):
                sender.send_msg(ru_bot, u"🛡Защита")
            print("Time to defend")
        else:
            print("Not to def")

        # receiver.message(message_handler(sender))

        time.sleep(10)


def main():
    # get a Receiver instance, to get messages.
    receiver = Receiver(host="localhost", port=4458)

    # get a Sender instance, to send messages, and other querys.
    sender = Sender(host="localhost", port=4458)

    print("I am done!")
# main_cycle(receiver=receiver, sender=sender)


main()
