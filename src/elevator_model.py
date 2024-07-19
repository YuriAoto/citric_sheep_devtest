"""Class to deal with the elevator

"""
from datetime import datetime, timezone
import logging


def _now():
    return datetime.now(timezone.utc)


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
        self.floor = 0
        self.vacant = True
        self.resting = True
        self.mlp = None

    def demand(self, floor):
        """A demand for the elevator
        
        Parameters:
        -----------
        floor (int) the floor where the elevator is called from
        
        """
        logging.debug('Demand at floor %s', floor)
        self.db.add_demand(floor, _now())
        self._goto(floor)

    def _goto(self, floor):
        """Change elevator position to floor"""
        self.floor = floor

    def goto_if_vacant_AI(self, mlp):
        """If vacant, use prediction engine to change floor
        
        Parameters:
        -----------
        mlp ()  The machine learning predictor
        
        """
        if self.vacant and self.resting and self.mlp is not None:
            self._goto(self.mlp.predict(self.db.dt_parser.parse(_now())))
