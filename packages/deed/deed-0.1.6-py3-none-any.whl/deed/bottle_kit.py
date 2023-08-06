from bottle import request, response

from deed import AuditLog
from deed.tracing import LOCAL_THREAD, audit_span


def audit(**kwargs):
    def wrap(callback):
        callback.audit = kwargs
        return callback

    return wrap


class AuditBuilder:

    def __init__(self, context, session):
        self.context = context
        self.session = session
        self.resource = None
        self.payload = None

    def build(self):
        log = AuditLog(**self.context)
        log.session(**self.session)
        return log


class DeedPlugin:
    name = 'deed'
    api = 2
    status_range = range(200, 400)

    def setup(self, app):
        pass

    def apply(self, callback, _context):
        @audit_span
        def wrapper(*args, **kwargs):
            if hasattr(callback, "audit"):
                LOCAL_THREAD.context.update(callback.audit)
                LOCAL_THREAD.session.update({'where': request.remote_addr})
                request.audit = AuditBuilder(LOCAL_THREAD.context, LOCAL_THREAD.session)
                result = callback(*args, **kwargs)
                if response.status_code in self.status_range and request.audit.resource:
                    payload = request.audit.payload or {}
                    log = request.audit.build()
                    log.audit(request.audit.resource, payload=payload)
                return result
            return callback(*args, **kwargs)

        return wrapper
