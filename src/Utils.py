import datetime
import calendar
import configparser
import os


class Utils:
    @staticmethod
    def get_business_date():
        today = datetime.datetime.now()
        if today.isoweekday() == 6 or today.isoweekday() == 7:
            while today.isoweekday() == 6 or today.isoweekday() == 7:
                one_day = datetime.timedelta(days=1)
                today = today - one_day
        today = today.strftime("%Y-%m-%d")
        return today

    @staticmethod
    def read_properties():
        config = configparser.RawConfigParser()
        config.read(os.getcwd() + "/data/indicator.properties")
        return config
