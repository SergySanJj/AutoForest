from telethon import TelegramClient, sync
from telethon import utils


import datetime
import time
import json
import sys


import variables

DEBUG = True

api_id = variables.api_id
api_hash = variables.api_hash

ru_bot = "@ChatWarsBot"
eu_bot = "@chtwrsbot"


debug_bot = "@ChatGrinding_bot"

time_before_def = 40*60


emoji_list = {
    'tree'     : u"🌲",
    'shield'   : u"🛡",
    'bed'      : u"🛌",
    'medal'    : u"🏅",
    'gorn'     : u"📯",
    'play'     : u"▶️",
    'mushroom' : u"🍄",
    'mountain' : u"🏔",
    'map'      : u"🗺"
}

activities_ru = {
    'forest': emoji_list['tree'] + u"Лес",
    'def': emoji_list['shield'] + u"Защита",
    'fight': emoji_list['play'] +  u"Быстрый бой",
    'hero': emoji_list['medal'] + u"Герой",
    'idle' : emoji_list['bed'] + u"Отдых"}




battle_table_ru = [
    datetime.datetime.strptime("01:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("17:00:00", "%H:%M:%S"),]

class Hero:
    def __init__(self):
        #True - free, False in the forest or defending -
        state = True
        activity = "idle"

    def change_state(self, new_state, new_activity):
        self.state = new_state
        self.activity = new_activity


def main():
    hero = Hero()
    client = TelegramClient('autoforest', api_id, api_hash)
    client.start()

    #print(client.get_me().stringify())
    #client.add_event_handler(update_handler)


    main_cycle(client, hero)

    with client.start():
        print('(Press Ctrl+C to stop this)')
        client.run_until_disconnected()

    client.disconnect()




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


def main_cycle(client, hero):
    checker = True
    while checker:
        if defend_check():
            client.send_message(debug_bot, activities_ru['def'])
            time.sleep(1)
            client.send_message(debug_bot, "HERO DEFENDS for")
            while (defend_check()):
                time.sleep(5)
        for message in client.iter_messages(ru_bot, limit=10):
            # print(utils.get_display_name(message.sender), message.message)
            if activities_ru['idle'] in message.message:
                print("HERO IDLE")
                hero.change_state(True, activities_ru['idle'])

        time.sleep(5)





    return 0


async def update_handler(update):
    print(update)







########### RUN ############




