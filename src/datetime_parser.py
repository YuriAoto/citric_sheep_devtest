"""A parser for datetime, to obtain the desired information

"""
class ParserNotConfiguredError(Exception):
    pass


class DateTimeParser:
    """Class to parse the date and time
    
    This class intends to obtain the desired information from datetime
    to be used in the ML engine.
    This can be customized by the user

    Once the parser is configured, it can be used with the `parse` method,
    that transforms the datetime to an object that can be directly added
    to the database or as input to the predictor engine.
    
    """
    
    def __init__(self):
        self._parserinfo = None

    def parse(self, datetime):
        """Parse the time according to current parser.
        
        Parameters:
        -----------
        datetime ()
        
        Return:
        -------

        """
        if self._parserinfo is None: raise ParserNotConfiguredError()
        info = {'plain_dt': datetime}
        info['hour'] = 1
        info['week_day'] = 1
        info['month'] = 1
        return info

    def set(self, info):
        """Sets the parser"""
        self._parserinfo = info

    def __repr__(self):
        """A string representation of the parser."""
        if self._parserinfo is None: raise ParserNotConfiguredError()
        return str(self._parserinfo)
