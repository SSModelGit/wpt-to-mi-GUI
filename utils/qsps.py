import json

class BasicQSP:
    def __init__(self):
        self.id = 'dispatch-Gui'
        self.type = 'statePlan'
        self.features = []
        self.eventList = []
        self.stateVars = []
        self.startEvent = None
        self.goalEpisodes = []
        self.version='0.0-0'
        self.qsp_json = ''

    def setVariable(self, varName, varValue, agent="auv"):
        var = {'$id': '{}.{}'.format(agent, varName),
                '$type': 'stateVariable',
                'timeDomain': {'$type': 'realDomain',
                               'ranges': [{'bounds': [0, 'Infinity'],
                                           'maxClosed': False,
                                           'minClosed': True}]},
                'range': {'$type': 'realDomain',
                          'ranges': [{'bounds': ['-Infinity', 'Infinity'],
                                      'maxClosed': True,
                                      'minClosed': True}]},
                '$annotations': {'rmpl/initialValue': varValue,
                                 'odo.mtk/trueId': {'$type': 'symbol',
                                                    'symbolName': '{}.{}'.format(agent, varName)}}}
        self.stateVars.append(var)

    def initVariables(self, initloc=(0,0), agent="auv"):
        self.setVariable('x-loc', initloc[0], agent)
        self.setVariable('y-loc', initloc[1], agent)

    def addEpisode(self, episode):
        self.eventList.append(episode.start.event)
        self.eventList.append(episode.end.event)
        if self.startEvent == None:
            self.startEvent = episode.start.id
        else:
            # TODO: Add connector episode
            pass
        self.goalEpisodes.append(episode.episode)
        return True # successful add

    def populate(self):
        self.qsp = self.inner_populate()
        self.qsp_json = json.dumps(self.qsp)
        return self.qsp

    def inner_populate(self):
        if self.startEvent == None:
            print("[WARNING]: There is no starting event - QSP is incomplete!!!!")
        return {'$id': self.id,
                '$type': self.type,
                '$features': self.features,
                'stateSpace': {'events': self.eventList,
                               'stateVariables': self.stateVars},
                'startEvent': self.startEvent,
                'goalEpisodes': self.goalEpisodes,
                '$version': self.version}

    def __repr__(self):
        return self.qsp_json