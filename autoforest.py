# coding=utf-8

__author__ = 'SergySanJj'

"""
Autobot for ChatWars.
"""

from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine

import time
import datetime
import logging
import math
import json

#logs everything connected with tg-cli into console
#logging.basicConfig(level=logging.DEBUG)

#path to telegram-cli dir:
tg_cli_dir = "/loc/to/tg/"

ru_bot = "@ChatWarsBot"
eu_bot = "@chtwrsbot"

debug_bot = "@ChatGrinding_bot"

#use next command in tg/bin/:
#./telegram-cli --json -P 4458
#after what port 4458 will be opened



activities_ru = {
	'forest': "🌲Лес",
	'defend': "🛡Защита",
	'fight' : "▶️Быстрый бой",
	'hero'  : "🏅Герой"}

activities_eu = {
	'forest': "🌲Forest",
	'defend': "🛡Defend",
	'fight' : "▶️Fast fight"}

states_ru = {
	'rest': "Состояние:\n🛌Отдых"}

message_types_ru = {
	'main': "Уровень"}

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
def defend_check():
	curr_time = datetime.datetime.now()
	for t in battle_table_ru:
		differ = diff(input_time,t)
		#print(differ)
		if differ>0 and differ<30*60:
			return True
	return False


def state_check(receiver, sender):
	receiver.start()
	message = activities_ru['hero']
	sender.send_msg(ru_bot, message)
	
	receiver.message(message_handler(sender))


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
				if msg.sender.username ==  'ChatWarsBot':
					print(msg['text'])
					if message_types_ru['main'] in msg['text']:
						print("Main message:")
						if states_ru['rest'] in msg['text']:
							print("Resting")
							return True
						else:
							print("Busy")
							return False

	except GeneratorExit:
		# the generator (pytg) exited (got a KeyboardIterrupt).
        	pass
	except KeyboardInterrupt:
		# we got a KeyboardIterrupt(Ctrl+C/Ctrl+Z)
		pass
	else:
		# the loop exited without exception, becaues _quit was set True
		pass
	print("Busy")
	return False	


@coroutine
def message_handler(sender): 
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
				if msg.sender.username ==  'ChatWarsBot':
					print(msg['text'])

	except GeneratorExit:
		# the generator (pytg) exited (got a KeyboardIterrupt).
        	pass
	except KeyboardInterrupt:
		# we got a KeyboardIterrupt(Ctrl+C/Ctrl+Z)
		pass
	else:
		# the loop exited without exception, becaues _quit was set True
		pass
	print("no new messages")


def main_cycle(receiver, sender):
	while True:
		if defend_check():
			
			print("Time to defend")
		
		receiver.start()

		receiver.message(message_handler(sender))

		receiver.stop()
		time.sleep(5)


def main():	
	receiver = Receiver(host="localhost", port=4458)
	sender = Sender(host="localhost", port=4458)
	main_cycle(receiver, sender)


main()
