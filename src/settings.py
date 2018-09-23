import datetime

ru_bot = "@ChatWarsBot"
eu_bot = "@chtwrsbot"

debug_bot = "@ChatGrinding_bot"

time_before_def = 40 * 60
time_in_forest = 8*60

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
    'quests' : emoji_list['map']+u"Квесты"}

battle_table_ru = [
    datetime.datetime.strptime("01:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("17:00:00", "%H:%M:%S"), ]



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