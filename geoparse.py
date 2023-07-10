import os, sys, getopt
import json, geojson
from utils.episodes import BasicPosiEpisode
from utils.qsps import BasicQSP

class GeoParser:
    def __init__(self, geojson_file_path="my_plan.geojson"):
        with open(geojson_file_path) as gjf:
            wpt_data = geojson.load(gjf)
        self.wpts = [dat['geometry']['coordinates'] for dat in wpt_data['features']]
        self.construct_qsp()
        self.write_mi_string()
        self.write_to_file()

    def construct_qsp(self):
        self.qsp = BasicQSP()
        self.qsp.initVariables(tuple(self.wpts[0][::-1]))
        for i in range(1,len(self.wpts)):
            self.qsp.addEpisode(BasicPosiEpisode("ep-{}".format(i), cloc=self.wpts[i][::-1]))
        self.qsp.populate()

    def write_mi_string(self):
        self.mi_string = self.stateplan2ma(self.qsp.qsp_json)

    def write_to_file(self):
        return self.mi_string

    def get_state_var_val(self, state_plan, var_name):
        vars = state_plan["stateSpace"]["stateVariables"]
        for v in vars:
            if v["$id"] == var_name:
                return v["$annotations"]["rmpl/initialValue"]
        return None

    def stateplan2ma(self, state_plan_json):
        state_plan = json.loads(state_plan_json)
        count = 1
        exists = True
        waypoints = []
        init_long = self.get_state_var_val(state_plan, "auv.x-loc")
        init_lat = self.get_state_var_val(state_plan, "auv.y-loc")
        waypoints.append((init_long, init_lat))
        for ep in state_plan["goalEpisodes"]:
            constr = ep["endConstraints"]
            long = constr[0]['expression']['right']
            lat = constr[1]['expression']['right']
            waypoints.append((long,lat))

        return self.waypoints2file(waypoints)

    def waypoints2file(self, waypoints, start_time=0, list_stop_when=7, init_point=-2):
        """
        Given a list of waypoints, generate the string corresponding to the gotolist command
        :param waypoints: list of waypoint tuples
        :param start_time: when to start the list (0-immediatley, 1-stack idle, 2-heading idle)
        :param list_stop_when: When to go to next way point
        :param init_point: which waypoint to start the closest to
        :return: a string matching mi file syntax
        """

        out = "behavior_name=goto_list\n"
        out += "<start:b_arg>\n"

        out += "\tb_arg: start_when(enum) {}\n".format(start_time)
        out += "\tb_arg: list_stop_when(enum) {}\n".format(list_stop_when)
        out += "\tb_arg: init_wpt(enum) {}\n".format(init_point)
        out += "\tb_arg: num_waypoints(nodim) {}\n".format(len(waypoints))
        out += "<end:b_arg>\n<start:waypoints>\n"
        for w in waypoints:
            out+="{}    {}\n".format(w[1],w[0])
        out+="<end:waypoints>"
        return out

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:],"hti:",["filepath=","test="])
    for opt, arg in opts:
        if opt == '-h':
            print('geoparse.py -i <path/to/input/file>')
            sys.exit()
        elif opt in ("-i", "--filepath"):
            print(GeoParser(arg).mi_string)
        elif opt in ("-t", "--test"):
            print(GeoParser("trial-data/trial_plan.geojson").mi_string)
        else:
            print(GeoParser().mi_string)