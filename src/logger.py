import datetime
import random
import time


LOG_STRING = '[{0:%Y-%m-%d %H:%M:%S} {1}] {2}'


class Logger(object):
    """ Logs messages for hero """

    def __init__(self, user):
        self.user = user

    def log(self, text):
        """
        Printing message to console
        """
        message = LOG_STRING.format(
            datetime.datetime.now(),
            self.user,
            text
        )

        print(message)

    def sleep(self, duration, message=None, exact=True):
        """
        Sleeps and printing message
        """
        if not exact:
            duration += random.random() * 30

        if message:
            if "{" in message:
                self.log(message.format(duration / 60))

            else:
                self.log(message)

        else:
            self.log("Сон в секундах: {}".format(duration))

        time.sleep(duration)

        return True
