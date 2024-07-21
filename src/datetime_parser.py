"""A parser for datetime, to obtain the desired information

"""
import logging

from sqlalchemy import Integer

_possible_cols = {'hour': (Integer, lambda x: x.hour),
                  'month': (Integer, lambda x: x.month),
                  'year': (Integer, lambda x: x.month),
                  'month day': (Integer, lambda x: x.day),
                  'week day': (Integer,lambda x: x.weekday())
                  }


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
        self._names = []
        self._types = []
        self._funcs = []
        self._iter_index = 0

    def __repr__(self):
        return f'DateTimeParser: {self._names}'

    def __len__(self):
        return len(self._names)

    def __iter__(self):
        return self

    def __next__(self):
        if self._iter_index < len(self):
            ntf = (self._names[self._iter_index],
                   self._types[self._iter_index],
                   self._funcs[self._iter_index])
            self._iter_index += 1
            return ntf
        else:
            self._iter_index = 0
            raise StopIteration

    def clear(self):
        self._names = []
        self._types = []
        self._funcs = []

    def parse(self, datetime):
        """Parse the time according to current parser.
        
        Parameters:
        -----------
        datetime ()
        
        Return:
        -------

        """
        info = {'plain_dt': datetime}
        for col_name, col_type, dt_func in self:
            info[col_name] = dt_func(datetime)
        return info

    def parse_list(self, datetime):
        """Parse the time according to current parser, returning a list
        
        Parameters:
        -----------
        datetime ()
        
        Return:
        -------
        A list with the parsed information only
        """
        return [dt_func(datetime) for _, _, dt_func in self]

    @classmethod
    def from_list(cls, info):
        """Creates a DateTimeParser instance from a list of strings
        
        Each string is an information that will be used to parse the
        datetime. Possible values are:
        hour
        week day
        month day
        month
        year
        """
        new_dt_parser = cls()
        for entry in info:
            try:
                new_dt_parser.set_new_col(entry.strip().lower())
            except ValueError:
                new_dt_parser.clear() 
                raise ValueError(f'Invalid value for DateTimeParser: {entry}')
        return new_dt_parser

    @classmethod
    def from_file(cls, filename):
        """Creates a DateTimeParser instance from file
        
        Structure of file `filename`:
        Each line is an information that will be used to parse the
        datetime. Possible values are:
        hour
        week day
        month day
        month
        year
        """
        new_dt_parser = cls()
        with open(filename) as f:
            for line in f:
                if line.strip():
                    try:
                        new_dt_parser.set_new_col(line.strip().lower())
                    except ValueError:
                        new_dt_parser.clear() 
                        raise ValueError(
                            f'Invalid line in config file for DateTimeParser:\n{line}')
        return new_dt_parser

    def set_new_col(self, col_name):
        """Sets new entry to the parser, only for a possible col_name"""
        try:
            col_type, dt_func = _possible_cols[col_name]
        except KeyError:
            raise ValueError(f'Invalid column DateTimeParser: {col_name}')
        self._names.append(col_name)
        self._types.append(col_type)
        self._funcs.append(dt_func)

    def _set_new_col_inner(self, col_name, col_type, dt_func):
        """Sets new entry to the parser, directly
        
        Parameters:
        -----------
        col_name    The column name
        col_type    a type dealt with sqlalchemy, such as sqlalchemy.Integer
                    or sqlalchemy.String
        dt_func     a function with signature
                    df_func(dt: datetime.datetime) -> type
                    where type has correspondence with sqlalchemy.col_type
        """
        if col_name in self._names:
            raise ValueError(f'{col_name} is already used in this DateTimeParser.')
        if col_name in ('dtid', 'plain_dt', 'floor'):
            raise ValueError(f'{col_name} is invalid, as it is already in Table.')
        self._names.append(col_name)
        self._types.append(col_type)
        self._funcs.append(dt_func)

    def __repr__(self):
        """A string representation of the parser."""
        return str(self._names)
