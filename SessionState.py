class SessionState(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


def get(**kwargs):
    if hasattr(st, '_session_state'):
        for key, val in kwargs.items():
            if not hasattr(st._session_state, key):
                setattr(st._session_state, key, val)
    else:
        st._session_state = SessionState(**kwargs)

    return st._session_state

