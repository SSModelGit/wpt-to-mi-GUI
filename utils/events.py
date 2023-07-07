import json

class BasicEvent:
    def __init__(self, name='ev-1-s', style='event'):
        self.id = name
        self.style = style
        self.domain = {'$type': 'realDomain',
                       'value': self.set_domain_value()}
        self.annotations = {'basicGui': True, 'magellan': False}
        self.event = self.populate()
        self.event_json = json.dumps(self.event)

    def populate(self, use_new=False, name='ev-1-s', style='event'):
        if use_new:
            self.id = name
            self.style = style
            self.domain['value'] = self.set_domain_value()
        return {'$id': self.id,
                '$type': self.style,
                'domain': self.domain,
                '$annotations': self.annotations}

    def set_domain_value(self):
        return 0 if self.id[-1]=='s' else 1

    def __repr__(self):
        return self.event_json