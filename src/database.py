"""Class to deal with the database of demands

"""
import os
import logging

from datetime_parser import ParserNotConfiguredError

class DemandDatabase:
    """Database for elevator demands
    
    This class wraps all functions to deal with the database.
    
    """

    def __init__(self, dt_parser):
        self._filename = 'elevator.db'
        self.dt_parser = dt_parser

    @property
    def is_set(self):
        return os.path.isfile(self._filename)

    def _add(self, info, floor):
        logging.debug('Adding to database.')

    def _remove_old(self, older_than):
        logging.debug('Removing older demands from database.')

    def add_demand(self, floor, time):
        """Add a demand to the database"""
        try:
            info = self.dt_parser.parse(time)
            self._add(info, floor)
            logging.info('Put demand on database: floor %s at time %s', floor, time)
        except ParserNotConfiguredError:
            logging.warning('Put demand on database failed: parser not configured.')

    def reset(self):
        """Reset the database"""
        if self.is_set:
            os.remove(self._file)

    def set(self):
        if self.is_set:
            self.reset()
        pass

    def extract_demands(self):
        """Extract dt demands info and floors from database

        Return:
        -------
        The datetime and floor demands, in separate objects,
        from the db database.
        """
        dt_demands = None
        floors = None
        return dt_demands, floors
