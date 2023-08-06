import threading

LOCAL_THREAD = threading.local()


def audit_span(callback):
    def traced(*args, **kwargs):
        prev_context = getattr(LOCAL_THREAD, 'context', {})
        prev_session = getattr(LOCAL_THREAD, 'session', {})
        try:
            LOCAL_THREAD.context = prev_context.copy()
            LOCAL_THREAD.session = prev_session.copy()
            return callback(*args, **kwargs)
        finally:
            LOCAL_THREAD.context = prev_context
            LOCAL_THREAD.session = prev_session
    return traced


def from_context(key: str):
    session = getattr(LOCAL_THREAD, 'context', None)
    if not isinstance(session, dict):
        return None
    return session.get(key)


def from_session(key: str):
    session = getattr(LOCAL_THREAD, 'session', None)
    if not isinstance(session, dict):
        return None
    return session.get(key)
