"""The machine learning functions

"""
import logging

from sklearn.neural_network import MLPClassifier
import numpy as np

from util import now


class MLPredictionError(Exception):
    pass


def training(dt_demands, floors):
    """Create a ML engine that returns a floor based that best fits on the db data
    
    Parameters:
    -----------
    dt_demands    The (parsed) datetimes demands
    floors        The floors associated to the dt_demands
    
    Return:
    -------
    A ML engine trained from Parameters
    
    """
    clf = MLPClassifier(solver='lbfgs',
                        alpha=1e-5,
                        hidden_layer_sizes=(5, 2),
                        random_state=1)
    logging.debug('ML training is starting ...')
    try:
        clf.fit(dt_demands, floors)
    except ValueError:
        raise MLPredictionError(str(ValueError))
    logging.debug('ML training is complete!')
    return clf


def predict_now(mlp, dt_parser):
    return predict(mlp, dt_parser, now())


def predict(mlp, dt_parser, dt):
    return mlp.predict(np.array(dt_parser.parse_list(dt)).reshape(1, -1))
