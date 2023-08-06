# General Data Protection Regulation Utils
from copy import deepcopy
import re


class AttributeHandler:
    def __init__(self, node, attr):
        self.node = node
        self.attr = attr

    def process(self, meth, **_params):
        self.node[self.attr] = meth(self.node[self.attr])


class RenameAttributeHandler:
    def __init__(self, node, attr):
        self.node = node
        self.attr = attr

    def process(self, _meth, **params):
        self.node[params['rename_to']] = self.node[self.attr]
        del self.node[self.attr]


class ProtectionRules:
    def __init__(self):
        self.rules = []

    def add(self, path: str, meth, handler=AttributeHandler, **kwargs):
        self.rules.append({'path': path.split('.'), 'meth': meth,
                           'handler': handler, 'params': kwargs})

    def protect(self, obj, copy=True):
        if copy:
            obj = deepcopy(obj)
        for rule in self.rules:
            self._protect_attribute(obj, rule)
        return obj

    @classmethod
    def process(cls, obj, path: str, meth, handler=AttributeHandler, **kwargs):
        cls._protect_attribute(obj, {'path': path.split('.'), 'meth': meth,
                                      'handler': handler, 'params': kwargs})

    @classmethod
    def _protect_attribute(cls, obj, rule):
        path, meth = rule['path'], rule['meth']
        for handler in cls.__handle_attribute(obj, [] + path, rule['handler']):
            handler.process(meth, **rule['params'])

    @classmethod
    def __handle_attribute(cls, node, attrs: list, handler):
        attr = attrs.pop(0)
        if isinstance(node, dict):
            if '**' == attr:
                for k in list(node.keys()):
                    if k == attrs[0]:
                        yield from cls.__handle_attribute(node, [] + attrs, handler)
                    else:
                        yield from cls.__handle_attribute(node[k], [attr] + attrs, handler)
            elif attrs:
                yield from cls.__handle_attribute(node.get(attr), attrs, handler)
            else:
                yield handler(node, attr)
        if isinstance(node, list):
            if '**' == attr:
                for ix in range(len(node)):
                    if attrs:
                        yield from cls.__handle_attribute(node[ix], [attr] + attrs, handler)
                    else:
                        yield handler(node, ix)
            if '*' == attr:
                for ix in range(len(node)):
                    if attrs:
                        yield from cls.__handle_attribute(node[ix], [] + attrs, handler)
                    else:
                        yield handler(node, ix)


def mask_card_number(number):
    return re.sub(r'^(\d\d)(.+)(\d\d\d\d)$',
                  lambda m: '%s%s%s' % (m.group(1), re.sub(r'\d', '*', m.group(2)), m.group(3)), number)


def mask_doc_number(number):
    return re.sub(r'^(.+)(\d\d)$',
                  lambda m: '%s%s' % (re.sub(r'\d', '*', m.group(1)), m.group(2)), number)


def mask_email(email):
    return re.sub(r'^(\w)[^@]+@(\w)[^\.]*(\..*)', '\\1*@\\2*\\3', email)


if __name__ == '__main__':
    import json


    obj = {
        "items": [
            {"doc_number": "123.456.789-09", "mail": "example@gmail.com", "card": "5421 6745 4312 6578"},
            {"doc_number": "22.333.333/0001-99", "mail": "blabows@gmail.com"}],
        "doc_number": "123.456.789-99",
        "elem": {
            "items": [
                {"doc_number": "123.456.789-09", "mail": "example2@gmail.com"},
                {"doc_number": "22.333.333/0001-99", "mail": "blabows2@gmail.com"}]
        },
        "docs": ["12345678909", "123.456.789-09"]
    }
    rules = ProtectionRules()
    rules.add('elem.**.doc_number', mask_doc_number)
    rules.add('items.**.doc_number', meth=None, handler=RenameAttributeHandler, rename_to='document_number')
    rules.add('items.**.card', mask_card_number)
    rules.add('items.*.mail', mask_email)
    rules.add('docs.*', mask_doc_number)
    obj2 = rules.protect(obj)
    print(json.dumps(obj2, indent=4))
