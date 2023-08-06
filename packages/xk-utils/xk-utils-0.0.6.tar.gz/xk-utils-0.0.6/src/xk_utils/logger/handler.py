import datetime
import os
from logging import FileHandler


class TimeFileHandler(FileHandler):
    """
    A handler class which writes formatted logging records to files with date.
    """
    def __init__(self, filename, mode='a', encoding=None, delay=False, when='d'):
        """
        :param filename: test
        :param mode:
        :param encoding:
        :param delay:
        :param when: create log file with time format,
                y: year
                m: month
                d: day
                w: week
                H: hour
                M: minute
        """
        self.when = when
        self.date = self.__get_current_date()

        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        filename = f'{filename}_{self.date}.log'
        self.baseFilename = os.path.abspath(filename)
        FileHandler.__init__(self, filename, mode, encoding, delay)

    def __get_current_date(self):
        now = datetime.datetime.now()
        if self.when == 'd':
            date = now.strftime('%Y-%m-%d')
        elif self.when == 'w':
            w = int(now.strftime('%w'))
            start = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(days=w-1)
            date = start.strftime('%Y-%m-%d')
        elif self.when == 'm':
            start = datetime.datetime(now.year, now.month, 1)
            date = start.strftime('%Y-%m-%d')
        elif self.when == 'y':
            start = datetime.datetime(now.year, 1, 1)
            date = start.strftime('%Y-%m-%d')
        elif self.when == 'H':
            date = now.strftime('%Y-%m-%d_%H')
        elif self.when == 'M':
            date = now.strftime('%Y-%m-%d_%H-%M')
        else:
            date = now.strftime('%Y-%m-%d')

        return date

    def emit(self, record):
        date = self.__get_current_date()
        if date != self.date:
            self.date = date
            filename = f'{self.filename}_{self.date}.log'
            self.baseFilename = os.path.abspath(filename)
            self.stream = self._open()

        FileHandler.emit(self, record)

