"""The machine learning functions

"""
import sklearn


def create_predictor_from_db(dt_demands, floors):
    """Create a ML engine that returns a floor based that best fits on the db data
    
    Parameters:
    -----------
    dt_demands    The (parsed) datetimes demands
    floors        The floors associated to the dt_demands
    
    Return:
    -------
    A ML engine trained from Parameters
    
    """
    mlp = 'MLP'
    return mlp

