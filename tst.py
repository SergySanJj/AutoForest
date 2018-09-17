"""
Demonstrates how you could easily do complex conversations.
This conversation consists of the following:
You send
> /start
The bot welcomes you, and asks for your name
You send your name
> Luckydonald
The bot asks you for your age
> 4458
The bots replies with your name and age.
You are done, you now can continue from the beginning.
(after your `/start` until you are done, everyone else will only get a message, saying the bot is currently in use by another user)
"""

from pytg.receiver import Receiver  # get messages
from pytg.sender import Sender  # send messages, and other querys.
from pytg.utils import coroutine

import time
import datetime


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


def main():
    # get a Receiver instance, to get messages.
    receiver = Receiver(host="localhost", port=4458)

    # get a Sender instance, to send messages, and other querys.
    sender = Sender(host="localhost", port=4458)



    passed = 40
    while True:
        if defend_check():
            sender.msg(u"@ChatWarsBot,", u"\ud83d\udee1\ufe0fЗащита")
            time.sleep(10)
            sender.msg(u"ChatWarsBot", u"/tactics_night")
            sender.msg(u"Xxxsanj", u"defing")
            time.sleep(60*60)
            sender.msg(u"Xxxsanj", u"ended defing")
            continue
        else:
            sender.msg(u"ChatWarsBot", u"\ud83c\udf32Лес")
            sender.msg(u"Xxxsanj", u"forest")
            time.sleep(passed * 60)
            sender.msg(u"Xxxsanj", u"returned from forest")

        passed = (passed+2)%50
        if passed<30:
            passed = 40
    # start the Receiver, so we can get messages!
    #receiver.start()  # note that the Sender has no need for a start function.

    # add "example_function" function as message listener. You can supply arguments here (like sender).
    #receiver.message(message_loop(sender))  # now it will call the example_function and yield the new messages.

    # continues here, after exiting the while loop in example_function()

    # please, no more messages. (we could stop the the cli too, with sender.safe_quit() )
   # receiver.stop()

    # continues here, after exiting while loop in example_function()
    print("I am done!")

    # the sender will disconnect after each send, so there is no need to stop it.
    # if you want to shutdown the telegram cli:
    # sender.safe_quit() # this shuts down the telegram cli.
    # sender.quit() # this shuts down the telegram cli, without waiting for downloads to complete.
# end def main


@coroutine
def message_loop(sender):  # name "message_loop" and given parameters are defined in main()
    try:
        while True:  # loop for a session.
            msg = (yield)
            if should_skip_message(msg, sender):
                continue


            # end if
            
            user = msg.sender.cmd  # store his user cmd, we only want to chat with him now.

            msg = (yield)  # get the next message
            while should_skip_message(msg, sender, only_allow_user=user):
                # If msg is a unwanted event/message, get the next one.
                # See should_skip_message for more detail.
                msg = (yield)  # just get the next message.
            # end skip-while-unwanted loop

            name = msg.text

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


def should_skip_message(msg, sender, only_allow_user=None):
    """
    Checks if the event is a message, is not from the bot itself, is in a user-to-user (user-to-bot) chat and has text.
    Also sets the online status to online.
    :keyword only_allow_user: (Optional) Ignore all messages which are not from this user (checks msg.sender.cmd)
    Basically the same code as in bot_ping.py, a little bit extended.
    """
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
    if "text" not in msg or msg.text is None:  # we have media instead.
        return True  # and again, because we want to process only text message.
        # Everything in pytg will be unicode. If you use python 3 thats no problem,
        # just if you use python 2 you have to be carefull! (better switch to 3)
        # for convinience of py2 users there is a to_unicode(<string>) in pytg.encoding
        # for python 3 the using of it is not needed.
        # But again, use python 3, as you have a chat with umlaute and emojis.
        # This WILL brake your python 2 code at some point!
    if only_allow_user is not None and msg.sender.cmd != only_allow_user:
        #sender.msg(msg.sender.cmd, u"I am currently in use by another user. Please try again later.")
        return True
    return False


# # program starts here # #
if __name__ == '__main__':
    main()  # executing main function.
# Last command of file (so everything needed is already loaded above)