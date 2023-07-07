import json
from .events import BasicEvent

class BasicPosiEpisode:
    def __init__(self, epName, cloc = (0.0,0.0), agent="auv"):
        self.start = BasicEvent(name="{}-s".format(epName))
        self.end = BasicEvent(name="{}-f".format(epName))
        self.duration = {'$type': 'simpleDuration', 'lowerBound': 1, 'upperBound': 1}
        self.constraints = [{'$type': 'stateConstraint',
                             'expression': {'$type': 'equalApplication',
                                            'left': {'$type': 'stateVarApplication',
                                                     'stateVar': '{}.x-loc'.format(agent)},
                                            'right': cloc[0]}},
                            {'$type': 'stateConstraint',
                             'expression': {'$type': 'equalApplication',
                                            'left': {'$type': 'stateVarApplication',
                                                     'stateVar': '{}.y-loc'.format(agent)},
                                            'right': cloc[1]}}]
        self.annotations = {'basicGui': True, 'magellan': False}
        self.episode = self.populate()
        self.episode_json = json.dumps(self.episode)

    def populate(self):
        return {'$type': 'episode',
                'startEvent': self.start.id,
                'endEvent': self.end.id,
                'duration': self.duration,
                'endConstraints': self.constraints,
                '$annotations': self.annotations}

    def __repr__(self):
        return self.episode_json