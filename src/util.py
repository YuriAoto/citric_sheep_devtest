from datetime import datetime, timezone

def now():
    """Return current datetime
    
    This is a direct call to datetime.datetime.now
    Alternatively, timezone.utc could be passed,
    but this seems not to be stored in sqlite,
    leading to failed tests when comparing datetimes
    before and after storing in the database.
    
    """
    return datetime.now()
