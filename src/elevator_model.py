"""Class to deal with the elevator

"""
from datetime import datetime, timezone
import logging

from util import now
import ml_prediction

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

    def demand(self, floor, dt=None):
        """A demand for the elevator
        
        Parameters:
        -----------
        floor (int) the floor where the elevator is called from
        dt (datetime) the time of the demand
        
        """
        if dt is None: dt = now()
        logging.debug('Demand from floor %s at %s ', floor, dt)
        self.db.add_demand(floor, dt)
        self._goto(floor)

    def _goto(self, floor):
        """Change elevator position to floor"""
        self._floor = floor

    def predict_best_resting_floor(self, dt=None):
        """Make prediction of the best resting floor at the given datetime"""
        if dt is None: dt = now()
        if self.mlp is not None:
            predicted_floor = ml_prediction.predict(self.mlp, self.db.dt_parser, dt)[0]
            logging.debug('Predicted floor at %s: %s', dt, predicted_floor)
            return predicted_floor
        else:
            return None

    def goto_if_vacant_AI(self):
        """If vacant and resting, use prediction to change floor"""
        if self.vacant and self.resting:
            floor = self.predict_best_resting_floor()
            self._goto(self.floor if floor is None else floor)
