# -*- coding: utf-8 -*-
from .serializable import Serializable
from .odict import ODict
from .eq import DeepEqual
from .copyable import Copyable
#from .metadata import ParameterTypes
import datetime
import pdb
from collections import OrderedDict

import logging
# create logger
logger = logging.getLogger(__name__)
# logger.debug('level %d' %  (logger.getEffectiveLevel()))


# A UTC class.


class UTC(datetime.tzinfo):
    """UTC
    https://docs.python.org/2.7/library/datetime.html?highlight=datetime#datetime.tzinfo
    """

    ZERO = datetime.timedelta(0)
    HOUR = datetime.timedelta(hours=1)

    def utcoffset(self, dt):
        return UTC.ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return UTC.ZERO


utcobj = datetime.timezone.utc


class FineTime(Copyable, DeepEqual, Serializable):
    """ Atomic time (SI seconds) elapsed since the TAI epoch
    of 1 January 1958 UT2. The resolution is one microsecond and the
    allowable range is: epoch + /-290, 000 years approximately.

    This has the following advantages, compared with the standard class:

    It has better resolution(microseconds)
    Time differences are correct across leap seconds
    It is immutable
    """
    """ Te starting date in UTC """
    EPOCH = datetime.datetime(1958, 1, 1, 0, 0, 0, tzinfo=utcobj)

    """ number of TAI units in a second """
    RESOLUTION = 1000000  # microsecond

    """ """
    DEFAULT_FORMAT = '%Y-%m-%dT%H:%M:%S.%f UTC'  # ISO

    RETURNFMT = '%s.%06d'

    """ """
    TIMESPEC = 'microseconds'

    def __init__(self, date=None, format=None, **kwds):
        """ Initiate with a UTC date or an integer TAI"""
        leapsec = 0  # leap seconds to be implemented

        self.format = self.DEFAULT_FORMAT if format is None else format
        self.setTime(date)
        # logger.debug('date= %s TAI = %d' % (str(date), self.tai))
        super(FineTime, self).__init__(**kwds)

    @property
    def time(self):
        return self.getTime()

    @time.setter
    def time(self, time):
        self.setTime(time)

    def getTime(self):
        """ Returns the time related to this object."""
        return self.tai

    def setTime(self, time):
        """ Sets the time of this object. 

        If an integer is given, it will be taken as the TAI.
        If a datetime object or a string code is given, the timezone will be set to UTC.
        Only when current TAI is 0, so a non-zero instance is immutable. Violation gets a TypeError.
        """

        if not issubclass(time.__class__, int):
            pass
        if time is None:
            setTai = 0
        elif issubclass(time.__class__, int):
            setTai = time
        elif issubclass(time.__class__, datetime.datetime):
            if time.tzinfo is None:
                d = time.replace(tzinfo=utcobj)
            else:
                d = time
            setTai = self.datetimeToFineTime(d)
        elif issubclass(time.__class__, str):
            try:
                t = time.strip()
                d = datetime.datetime.strptime(time, self.format)
            except ValueError:
                tz = self.format[-3:]
                if not t.endswith(tz):
                    logger.warning('Time zone %s assumed for %s', tz, t)
                    d = datetime.datetime.strptime(t + ' ' + tz, self.format)
            d1 = d.replace(tzinfo=datetime.timezone.utc)
            setTai = self.datetimeToFineTime(d1)
        else:
            raise TypeError('%s must be an integer, a datetime object, or a string, but its type is %s.' % (
                str(time), type(time).__name__))
        try:
            if setTai and self.tai:
                raise TypeError(
                    'FineTime objects with non-zero TAI are immutable.')
        except AttributeError:
            # self.tai not exists
            pass
        self.tai = setTai

    def getFormat(self):
        return self.format

    def microsecondsSinceEPOCH(self):
        """ Return the rounded integer number of microseconds since the epoch: 1 Jan 1958. """
        return int(self.tai * self.RESOLUTION / FineTime.RESOLUTION+0.5)

    def subtract(self, time):
        """ Subract the specified time and return the difference
        in microseconds. """
        return self.tai - time.tai

    def datetimeToFineTime(self, dtm):
        """ Return given  Python Datetime as a FineTime to the precision of the input. Rounded to the last digit. Unit is decided by RESOLUTION."""
        leapsec = 0  # leap seconds to be implemented
        return int(self.RESOLUTION *
                   ((dtm - self.EPOCH).total_seconds() + leapsec)+0.5)

    def toDatetime(self, tai):
        """ Return given FineTime as a Python Datetime. """
        leapsec = 0  # leap seconds to be implemented
        return datetime.timedelta(seconds=(float(tai) / self.RESOLUTION - leapsec))\
            + self.EPOCH

    def toDate(self):
        """ Return this time as a Python Datetime. """

        return self.toDatetime(self.tai)

    def isoutc(self, format='%Y-%m-%dT%H:%M:%S'):
        """ Returns a String representation of this objet in ISO format without timezone. sub-second set to TIMESPEC.

        format: time format. default '%Y-%m-%dT%H:%M:%S' prints like 2019-02-17T12:43:04.577000 """
        s = self.tai / self.RESOLUTION
        sub = s - int(s)
        dt = datetime.timedelta(seconds=(s)) + self.EPOCH
        # return dt.isoformat(timespec=self.TIMESPEC)
        return self.RETURNFMT % (dt.strftime(format), int(sub*self.RESOLUTION+0.5))

    def toString(self, level=0,
                 tablefmt='rst', tablefmt1='simple', tablefmt2='simple',
                 width=0, **kwds):
        """ Returns a String representation of this object according to self.format.
        prints like 2019-02-17T12:43:04.577000 TAI(...)"""
        tais = str(self.tai) if hasattr(self, 'tai') else 'Unknown_TAI'
        if level == 0:
            if width:
                tstr = self.isoutc(
                    format='%Y-%m-%d\n%H:%M:%S') + '\n%s' % tais
                s = tstr
            else:
                tstr = self.isoutc() + ' TAI(%s)' % tais
                s = self.__class__.__name__ + \
                    '{' + tstr + ' fmt=' + self.format + '}'
        elif level == 1:
            if width:
                tstr = self.isoutc(
                    format='%Y-%m-%d\n%H:%M:%S') + '\n%s' % tais
            else:
                tstr = self.isoutc() + ' TAI(%s)' % tais
            s = tstr
        else:
            s = tais
        return s

    def __lt__(self, obj):
        """ can compare TAI directly """
        if 1:
            # if type(obj).__name__ in ParameterTypes.values():
            return self.tai < obj
        else:
            return super(FineTime, self).__lt__(obj)

    def __gt__(self, obj):
        """ can compare TAI directly """
        if 1:
            # if type(obj).__name__ in ParameterTypes.values():
            return self.tai > obj
        else:
            return super(FineTime, self).__gt__(obj)

    def __le__(self, obj):
        """ can compare TAI directly """
        if 1:
            # if type(obj).__name__ in ParameterTypes.values():
            return self.tai <= obj
        else:
            return super(FineTime, self).__le__(obj)

    def __ge__(self, obj):
        """ can compare TAI directly """
        if 1:
            # if type(obj).__name__ in ParameterTypes.values():
            return self.tai >= obj
        else:
            return super(FineTime, self).__ge__(obj)

    def __repr__(self):

        co = ', '.join(str(k)+'=' + ('"'+v+'"' if issubclass(v.__class__, str)
                                     else str(v)) for k, v in self.__getstate__().items())
        return '<'+self.__class__.__name__ + ' ' + co + '>'

    __str__ = toString

    def __getstate__(self):
        """ Can be encoded with serializableEncoder """
        return OrderedDict(tai=self.tai,
                           format=self.format,
                           _STID=self._STID)


class FineTime1(FineTime):
    """ Same as FineTime but Epoch is 2017-1-1 0 UTC and unit is millisecond"""
    EPOCH = datetime.datetime(2017, 1, 1, 0, 0, 0, tzinfo=utcobj)
    RESOLUTION = 1000  # millisecond
    RETURNFMT = '%s.%03d'
    TIMESPEC = 'milliseconds'
