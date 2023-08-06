import datetime


class SimpleTime:
    @staticmethod
    def now():
        return str(datetime.datetime.now()).split(".")[0]
