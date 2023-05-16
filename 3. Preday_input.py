import os
import json
#import numpy as np
import pandas as pd
import time
import random

# Path to the directory where the output files should be stored.
OUTPUT_DIR = "."
# Vehicle length in meters.
VEHICLE_LENGTH = 7.0
# Vehicle passenger-car equivalent.
VEHICLE_PCE = 1.0
# Simulation period.
PERIOD = [5.0 * 3600, 10.0 * 3600.0]
# Capacity per lane, used to compute the number of lanes on each edge (the total capacity of each
# edge is given by the input files and fixed).
CAPACITY_PER_LANE = 2000
# Edges' speed limit (set to 60 km/h so that free-flow travel time in minutes is equal to edge
# length in kilometers, just like in the input data).
SPEED_LIMIT = 60
# If `True`, vehicles can overtake each other at the edge's exit bottleneck (only if they have a
# different downstream edge). Recommanded value is: `True`.
ENABLE_OVERTAKING = True

MU = 2.0
# Simulation parameters.
start = time.time()

print("Reading trips")

def sam(a):
    
    od_matrix = pd.read_csv("Possible detour.csv")
    
    print("Generating trips")
    
    agents = list()
    
    i = 1
    for _, od_pair in od_matrix.iterrows():
        departure_time_model = {
            "type": "ContinuousChoice",
            "value": {
                "period": PERIOD,
                "choice_model": {
                    "type": "Logit",
                    "value": {
                        "u": od_pair["u"],
                        "mu": MU,
                    },
                },
            },
        }
        schedule_utility = {
            "type": "AlphaBetaGamma",
            "value": {
                "beta": od_pair["Beta"],
                "gamma": od_pair["Gamma"],
                "t_star_high": od_pair["t_star_high"],
                "t_star_low": od_pair["t_star_low"],
            },
        }
        leg1 = {
            "class": {
                "type": "Road",
                "value": {
                    "origin": int(od_pair["O1"]),
                    "destination": int(od_pair["IO1"]),
                    "vehicle": 0,
                },
            },
        }
        leg2 = {
            "class": {
                "type": "Road",
                "value": {
                    "origin": int(od_pair["IO1"]),
                    "destination": int(od_pair["ID1"]),
                    "vehicle": 0,
                },
            },
        }
        leg3 = {
            "class": {
                "type": "Road",
                "value": {
                    "origin": int(od_pair["ID1"]),
                    "destination": int(od_pair["D1"]),
                    "vehicle": 0,
                },
            },
        }
        car_mode = {
            "type": "Trip",
            "value": {
                "total_travel_utility": {
                    "type": "Polynomial",
                    "value": {
                        "b": od_pair["Alpha"],
                    },
                },
                "departure_time_model": departure_time_model,
                "destination_schedule_utility": schedule_utility,
                "legs": [leg1, leg2, leg3],
            },
        }
        agent = {
            "id": int(str(i) + str(1)) ,
            "modes": [car_mode],
        }
        agents.append(agent)
        
        departure_time_model = {
            "type": "ContinuousChoice",
            "value": {
                "period": PERIOD,
                "choice_model": {
                    "type": "Logit",
                    "value": {
                        "u": od_pair["u"],
                        "mu": MU,
                    },
                },
            },
        }
        schedule_utility = {
            "type": "AlphaBetaGamma",
            "value": {
                "beta": od_pair["Beta"],
                "gamma": od_pair["Gamma"],
                "t_star_high": od_pair["t_star_high"],
                "t_star_low": od_pair["t_star_low"],
            },
        }
        leg1 = {
            "class": {
                "type": "Road",
                "value": {
                    "origin": int(od_pair["O2"]),
                    "destination": int(od_pair["IO2"]),
                    "vehicle": 0,
                },
            },
        }
        leg2 = {
            "class": {
                "type": "Road",
                "value": {
                    "origin": int(od_pair["IO2"]),
                    "destination": int(od_pair["D2"]),
                    "vehicle": 0,
                },
            },
        }
        car_mode = {
            "type": "Trip",
            "value": {
                "total_travel_utility": {
                    "type": "Polynomial",
                    "value": {
                        "b": od_pair["Alpha"],
                    },
                },
                "departure_time_model": departure_time_model,
                "destination_schedule_utility": schedule_utility,
                "legs": [leg1, leg2],
            },
        }
        agent = {
            "id": int(str(i) + str(2)),
            "modes": [car_mode],
        }
        agents.append(agent)
        
        departure_time_model = {
            "type": "ContinuousChoice",
            "value": {
                "period": PERIOD,
                "choice_model": {
                    "type": "Logit",
                    "value": {
                        "u": od_pair["u"],
                        "mu": MU,
                    },
                },
            },
        }
        schedule_utility = {
            "type": "AlphaBetaGamma",
            "value": {
                "beta": od_pair["Beta"],
                "gamma": od_pair["Gamma"],
                "t_star_high": od_pair["t_star_high"],
                "t_star_low": od_pair["t_star_low"],
            },
        }
        leg1 = {
            "class": {
                "type": "Road",
                "value": {
                    "origin": int(od_pair["O3"]),
                    "destination": int(od_pair["ID3"]),
                    "vehicle": 0,
                },
            },
        }
        leg2 = {
            "class": {
                "type": "Road",
                "value": {
                    "origin": int(od_pair["ID3"]),
                    "destination": int(od_pair["D3"]),
                    "vehicle": 0,
                },
            },
        }
        car_mode = {
            "type": "Trip",
            "value": {
                "total_travel_utility": {
                    "type": "Polynomial",
                    "value": {
                        "b": od_pair["Alpha"],
                    },
                },
                "departure_time_model": departure_time_model,
                "destination_schedule_utility": schedule_utility,
                "legs": [leg1, leg2],
            },
        }
        agent = {
            "id": int(str(i) + str(3)),
            "modes": [car_mode],
        }
        
        agents.append(agent)
        
        departure_time_model = {
            "type": "ContinuousChoice",
            "value": {
                "period": PERIOD,
                "choice_model": {
                    "type": "Logit",
                    "value": {
                        "u": od_pair["u"],
                        "mu": MU,
                    },
                },
            },
        }
        schedule_utility = {
            "type": "AlphaBetaGamma",
            "value": {
                "beta": od_pair["Beta"],
                "gamma": od_pair["Gamma"],
                "t_star_high": od_pair["t_star_high"],
                "t_star_low": od_pair["t_star_low"],
            },
        }
        leg = {
            "class": {
                "type": "Road",
                "value": {
                    "origin": int(od_pair["O4"]),
                    "destination": int(od_pair["D4"]),
                    "vehicle": 0,
                },
            },
        }
        car_mode = {
            "type": "Trip",
            "value": {
                "total_travel_utility": {
                    "type": "Polynomial",
                    "value": {
                        "b": od_pair["Alpha"],
                    },
                },
                "departure_time_model": departure_time_model,
                "destination_schedule_utility": schedule_utility,
                "legs": [leg],
            },
        }
        agent = {
            "id": int(str(i) + str(4)),
            "modes": [car_mode],
        }
        
        agents.append(agent)
        
        i += 1
        #print(i)
        #break
    return agents

agents= sam(2)

print("% s seconds" % (time.time() - start))


print("Writing data...")
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
with open(os.path.join(OUTPUT_DIR, "agents_preday.json"), "w") as f:
    f.write(json.dumps(agents))


'''

PARAMETERS = {
    "period": PERIOD,
    "learning_model": {
        "type": "Exponential",
        "value": {
            "alpha": 0.99,
        },
    },
    "init_iteration_counter": 1,
    "stopping_criteria": [
        {
            "type": "MaxIteration",
            "value": 100,
        },
    ],
    "update_ratio": 1.0,
    "random_seed": 13081996,
    "network": {
        "road_network": {
            "recording_interval": 300.0,
            "spillback": True,
            "max_pending_duration": 30.0,
        }
    },
}


with open(os.path.join(OUTPUT_DIR, "preday_parameters.json"), "w") as f:
    f.write(json.dumps(PARAMETERS))
    
'''

