import jsonpatch


class DiffBuilder:
    def __init__(self, audit_log):
        self.audit_log = audit_log

    def build(self, resource, payload):
        changes = {k: v for k, v in {**resource, **payload}.items()
                   if k in payload and (k not in resource or resource[k] != payload[k])}
        return {'changes': changes} if changes else None


class OldAndNewBuilder:
    def __init__(self, audit_log):
        self.audit_log = audit_log

    def build(self, resource, payload):
        new_resource = jsonpatch.make_patch(resource, payload).apply(resource)
        return {'old_resource': resource, 'resource': new_resource} if new_resource else None


class JsonPatchBuilder:
    def __init__(self, audit_log):
        self.audit_log = audit_log

    def build(self, resource, payload):
        patch = list(jsonpatch.make_patch(resource, payload))
        return {'patch': patch} if patch else None


class NewResourceBuilder:
    def __init__(self, audit_log):
        self.audit_log = audit_log

    def build(self, resource, _payload):
        return {'resource': resource}


class ResourceIdBuilder:
    def __init__(self, audit_log):
        self.audit_log = audit_log

    def build(self, resource, _payload):
        return {'resource': {k: v for k, v in resource.items() if k in ['_id', 'id']}}


MODE_BUILDERS = {
    'diff': DiffBuilder,
    'jsonpatch': JsonPatchBuilder,
    'prev_and_new': OldAndNewBuilder,
    'old_and_new': OldAndNewBuilder,
    'read': ResourceIdBuilder,
    'delete': ResourceIdBuilder,
    'destroy': ResourceIdBuilder,
    'remove': ResourceIdBuilder,
    'create': NewResourceBuilder,
}


def get_builder(audit_mode):
    return MODE_BUILDERS[audit_mode]
