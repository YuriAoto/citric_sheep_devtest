"""The machine learning functions

"""
import logging

from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
import numpy as np

from util import now


class MLPredictionError(Exception):
    pass


def training(dt_demands, floors, ML_model='nn'):
    """Create a ML engine that returns a floor based that best fits on the db data
    
    Parameters:
    -----------
    dt_demands    The (parsed) datetimes demands
    floors        The floors associated to the dt_demands
    
    Return:
    -------
    A ML engine trained from Parameters
    
    """
    if ML_model == 'svm':
        classifier = SVC(kernel='linear', C=1)
    elif ML_model == 'nn':
        classifier = MLPClassifier(solver='lbfgs',
                                   alpha=1e-5,
                                   hidden_layer_sizes=(10, 10),
                                   random_state=1)
    else:
        raise ValueError(f'Unknown ML model: {ML_model}')
    logging.debug('ML training is starting ...')
    try:
        classifier.fit(dt_demands, floors)
    except ValueError:
        raise MLPredictionError(str(ValueError))
    logging.debug('ML training is complete!')
    return classifier


def predict(mlp, dt_parser, dt):
    return mlp.predict(np.array(dt_parser.parse_list(dt)).reshape(1, -1))
