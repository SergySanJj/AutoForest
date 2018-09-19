

from pytg.receiver import Receiver  # get messages
from pytg.sender import Sender  # send messages, and other querys.
from pytg.utils import coroutine

import time
import datetime
import os


time_before_def = 55 * 60

battle_table_ru = [
    datetime.datetime.strptime("01:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("17:00:00", "%H:%M:%S"),]

battle_table_eu = [
    datetime.datetime.strptime("02:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("10:00:00", "%H:%M:%S"),
    datetime.datetime.strptime("18:00:00", "%H:%M:%S")]

ru_bot = "@ChatWarsBot"
eu_bot = "@chtwrsbot"
debug_bot = "@ChatGrinding_bot"



bots = {'ru' : ru_bot,
        'eu' : eu_bot,
        'debug' : debug_bot}

class Hero:
    def __init__(self):
        self.free = True
        self.stamina = 0

ru_hero = Hero()
eu_hero = Hero()



def main():

    #start_cli(4458)

    # get a Receiver instance, to get messages.
    receiver = Receiver(host="localhost", port=4458)

    # get a Sender instance, to send messages, and other querys.
    sender = Sender(host="localhost", port=4458)

    # start the Receiver, so we can get messages!
    receiver.start()  # note that the Sender has no need for a start function.


    receiver.message(message_loop(sender))

    #receiver.stop()

    #sender.safe_quit()

    print("FINISH.")

    # the sender will disconnect after each send, so there is no need to stop it.
    # if you want to shutdown the telegram cli:
    # sender.safe_quit() # this shuts down the telegram cli.
    # sender.quit() # this shuts down the telegram cli, without waiting for downloads to complete.
# end def main


def start_cli(port):
    # TODO:: method that cd to /loc/to/tg/bin/ && ./telegram-cli -p $port
    try:
        os.system('cd ~/tg/bin')
        os.system('./telegram-cli -p 4458')
    except FileNotFoundError:
        pass
    else:
        print("Started at $port port")

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




@coroutine
def message_loop(sender):
    try:
        msg = (yield)
        print(msg, "\n")
        while True:  # loop for a session.
            msg = (yield)

            if should_skip_message(msg, sender):
                continue
            
            user = msg.sender.cmd

            text = msg.text

            print(text, "\n")

            # done.
    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C)
        pass
    else:
        # the loop exited without exception, becaues _quit was set True
        pass


def should_skip_message(msg, sender):

    sender.status_online()  # so we will stay online.
    # (if we are offline it might not receive the messages instantly,
    #  but eventually we will get them)
    print(msg)
    if msg.event != "message":
        return True  # is not a message.
    if msg.own:  # the bot has send this message.
        return True  # we don't want to process this message.
    if msg.receiver.type != "user":
        return True
    if msg.text is None:  # we have media instead.
        return True
    if msg.sender.cmd != eu_bot or msg.sender.cmd != ru_bot:
        #sender.msg(msg.sender.cmd, u"I am currently in use by another user. Please try again later.")
        return True
    return False


# # program starts here # #
main()