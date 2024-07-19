"""Class to deal with the elevator

"""
from datetime import datetime, timezone
import logging

from util import now

class Elevator:
    """The elevator
    
    """

    def __init__(self, db):
        """Initializes the elevator
        
        Parameters:
        -----------
        db (database.DemandDatabase) the database
        """
        self.db = db
        self._floor = 0
        self.vacant = True
        self.resting = True
        self.mlp = None

    @property
    def floor(self):
        return self._floor

    def demand(self, floor):
        """A demand for the elevator
        
        Parameters:
        -----------
        floor (int) the floor where the elevator is called from
        
        """
        logging.debug('Demand at floor %s', floor)
        self.db.add_demand(floor, now())
        self._goto(floor)

    def _goto(self, floor):
        """Change elevator position to floor"""
        self._floor = floor

    def goto_if_vacant_AI(self, mlp):
        """If vacant, use prediction engine to change floor
        
        Parameters:
        -----------
        mlp ()  The machine learning predictor
        
        """
        if self.vacant and self.resting and self.mlp is not None:
            self._goto(self.mlp.predict(self.db.dt_parser.parse(now())))
