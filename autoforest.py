__author__ = 'SergySanJj'

"""
Autobot for ChatWars.
"""

from pytg.sender import Sender
from pytg.receiver import Receiver


import time
import datetime
import logging
import math

#logs everything connected with tg-cli into console
logging.basicConfig(level=logging.DEBUG)

#path to telegram-cli dir:
tg_cli_dir = "/loc/to/tg/"

ru_bot = "@ChatWarsBot"
eu_bot = "@chtwrsbot"

debug_bot = "@ChatGrinding_bot"

#use next command in tg/bin/:
#./telegram-cli --json -P 4458
#after what port 4458 will be opened

receiver = Receiver(host="localhost", port=4458)
sender = Sender(host="localhost", port=4458)

activities_ru = {
	'forest': "🌲Лес",
	'defend': "🛡Защита"}

activities_eu = {
	'forest': "🌲Forest",
	'defend': "🛡Defend"}

battle_table_ru = [
	datetime.datetime.strptime("01:00:00", "%H:%M:%S"),
	datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
	datetime.datetime.strptime("17:00:00", "%H:%M:%S")]

battle_table_eu = [
	datetime.datetime.strptime("02:00:00", "%H:%M:%S"),
	datetime.datetime.strptime("10:00:00", "%H:%M:%S"),
	datetime.datetime.strptime("18:00:00", "%H:%M:%S")]

#returns time difference in seconds
def diff(start, end):
	start_sec = start.hour*3600 + start.minute*60 + start.second
	end_sec = end.hour*3600 + end.minute*60 + end.second
	return (end_sec - start_sec)

#returns True if it's time to defend
def defend_check(input_time):
	for t in battle_table_ru:
		differ = diff(input_time,t)
		#print(differ)
		if differ>0 and differ<30*60:
			return True
	return False

def main():	
	message = "лу"
	while True:
		sender.send_msg(debug_bot, message)
		message += "у"
		curr_time = datetime.datetime.now()
		
		print("Time to defend:", defend_check(curr_time))
		time.sleep(5)
		

main()
