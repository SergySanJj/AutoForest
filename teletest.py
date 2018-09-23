from telethon import TelegramClient

import datetime
import time

from src import variables

DEBUG = True

# You need to create variables.py file and add there variables with api_id
# and api_hash.
api_id = variables.api_id
api_hash = variables.api_hash

ru_bot = "@ChatWarsBot"
eu_bot = "@chtwrsbot"

debug_bot = "ChatGrinding_bot"

time_before_def = 40 * 6000
time_in_forest = 8 * 60

emoji_list = {
    'tree': u"🌲",
    'shield': u"🛡",
    'bed': u"🛌",
    'medal': u"🏅",
    'gorn': u"📯",
    'play': u"▶️",
    'mushroom': u"🍄",
    'mountain': u"🏔",
    'map': u"🗺"
}

activities_ru = {
    'forest': emoji_list['tree'] + u"Лес",
    'def': emoji_list['shield'] + u"Защита",
    'duel': emoji_list['play'] + u"Быстрый бой",
    'hero': emoji_list['medal'] + u"Герой",
    'idle': emoji_list['bed'] + u"Отдых",
    'quests': emoji_list['map'] + u"Квесты"}

battle_table_ru = [
    datetime.datetime.strptime("01:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("17:00:00", "%H:%M:%S"), ]


class Hero:
    def __init__(self):
        # True - free, False in the forest or defending -
        self.state = True
        self.activity = "idle"

    def change_state(self, new_state, new_activity):
        self.state = new_state
        self.activity = new_activity


def main():
    hero = Hero()
    client = TelegramClient('autoforest', api_id, api_hash)
    client.start()

    main_cycle(client, hero)

    with client.start():
        print('(Press Ctrl+C to stop this)')
        client.run_until_disconnected()

    client.disconnect()


def main_cycle(client, hero):
    checker = True

    try:
        while checker:
            if defend_check():
                client.send_message(debug_bot, activities_ru['def'], parse_mode='markdown')
                time.sleep(3)
                client.send_message(debug_bot, u"/tactics_amber", parse_mode='markdown')
                time.sleep(10)
                client.send_message(debug_bot, activities_ru['hero'], parse_mode='markdown')
                # time.sleep(1)
                # client.send_message(debug_bot, "HERO DEFENDS")
                while (defend_check()):
                    time.sleep(5)

            message = client.get_messages(ru_bot)
            # print(utils.get_display_name(message.sender), message.message)
            #print(message.message())
            if activities_ru['idle'] in message.message:
                print("HERO IDLE")
                hero.change_state(True, activities_ru['idle'])
            elif activities_ru['forest'] in message.message:
                print("HERO IN FOREST")
                hero.change_state(False, activities_ru['forest'])
            elif "🔋Выносливость: 1" in message.message:
                print("Ready for forest")
            elif "🔋Выносливость: 2" in message.message:
                print("Ready for forest")
            elif "🔋Выносливость: 0" in message.message:
                print("TIRED")
                time.sleep(10)
            elif "/go" in message.message:
                print("GO")

            if hero.state:
                client.send_message(debug_bot, activities_ru['quests'])
                time.sleep(3)
                client.send_message(debug_bot, activities_ru['forest'])
                print("IN FOREST, sleeping")
                time.sleep(10)

            time.sleep(5)
    except KeyboardInterrupt:
        pass
    else:
        pass

    return 0


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


async def update_handler(update):
    print(update)


########### RUN ############

main()
