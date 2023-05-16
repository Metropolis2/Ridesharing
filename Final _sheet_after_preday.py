import time
import json
import pandas as pd
import zstandard as zstd

start = time.time()

# a = open('agents_preday.json')
# input_preday = json.load(a)

def get_agent_results():
    dctx = zstd.ZstdDecompressor()
    with open('agent_results.json.zst', "br") as f:
        reader = dctx.stream_reader(f)
        data = json.load(reader)
    return data

sam = get_agent_results()

df1 = pd.read_csv("Possible detour.csv")
walk = pd.read_csv("Free_flow_times.csv")

df1["Driver expected utility1"] = None
df1["Driver expected utility2"] = None
df1["Driver expected utility3"] = None
df1["Driver expected utility4"] = None

df1["passenger departure1"] = None
df1["passenger arrival1"] = None

df1["passenger departure2"] = None
df1["passenger arrival2"] = None
df1["passenger departure3"] = None
df1["passenger arrival3"] = None

df1["passenger departure4"] = None
df1["passenger arrival4"] = None

df1["walk cost1"] = 0
df1["walk cost2"] = None
df1["walk cost3"] = None
df1["walk cost4"] = None

#walk cost is 15 euro per hour
z = 0.25
x = 0
for index,  df in df1.iterrows():
    for j in range(4):
        if j == 0:
            df1.loc[index, "passenger departure1"] = sam[x]['mode_results']['value']['legs'][1]['class']['value']['pre_exp_departure_time']
            df1.loc[index, "passenger arrival1"] = sam[x]['mode_results']['value']['legs'][1]['class']['value']['pre_exp_arrival_time']
            df1.loc[index, "Driver expected utility1"] = sam[x]['expected_utility']
            #print(df["id driver"])
        elif j == 1 :
            df1.loc[index, "passenger departure2"] = sam[x]['mode_results']['value']['legs'][1]['class']['value']['pre_exp_departure_time']
            df1.loc[index, "passenger arrival2"] = sam[x]['mode_results']['value']['legs'][1]['class']['value']['pre_exp_arrival_time']
            df1.loc[index, "Driver expected utility2"] = sam[x]['expected_utility']
            df1.loc[index, "walk cost2"] = walk.iloc[df1.loc[index, "destination driver"], df1.loc[index, "destination passenger"]] * z
            #print(df["id driver"])
        elif j == 2:
            df1.loc[index, "passenger departure3"] = sam[x]['mode_results']['value']['legs'][0]['class']['value']['pre_exp_departure_time']
            df1.loc[index, "passenger arrival3"] = sam[x]['mode_results']['value']['legs'][0]['class']['value']['pre_exp_arrival_time']
            df1.loc[index, "Driver expected utility3"] = sam[x]['expected_utility']
            df1.loc[index, "walk cost3"] = walk.iloc[df1.loc[index, "origin passenger"], df1.loc[index, "origin driver"]] * z
            #print(df["id driver"])
        else:
           df1.loc[index, "passenger departure4"] = sam[x]['mode_results']['value']['legs'][0]['class']['value']['pre_exp_departure_time']
           df1.loc[index, "passenger arrival4"] = sam[x]['mode_results']['value']['legs'][0]['class']['value']['pre_exp_arrival_time']
           df1.loc[index, "Driver expected utility4"] = sam[x]['expected_utility']
           df1.loc[index, "walk cost4"] = (walk.iloc[df1.loc[index, "origin passenger"], df1.loc[index, "origin driver"]] + walk.iloc[df1.loc[index, "destination driver"], df1.loc[index, "destination passenger"]]) * z
           #print(df["id driver"])
        
        x += 1
        #print(x)
    #break


df1["P_car_time_cost1"] = (df1["passenger arrival1"] - df1["passenger departure1"]) * (- df1["Alpha"])
df1["P_car_time_cost2"] = (df1["passenger arrival2"] - df1["passenger departure2"]) * (- df1["Alpha"])
df1["P_car_time_cost3"] = (df1["passenger arrival3"] - df1["passenger departure3"]) * (- df1["Alpha"])
df1["P_car_time_cost4"] = (df1["passenger arrival4"] - df1["passenger departure4"]) * (- df1["Alpha"])


df1['schedule delay cost1'] = df1.apply(lambda row: (row['t_star_high'] - (row['passenger arrival1'] + (row['walk cost1']*240)))*row['Beta'] if (row['passenger arrival1']  + (row['walk cost1']*240)) <= row['t_star_high'] else ((row['passenger arrival1']  + (row['walk cost1']*240)) - row['t_star_high'])*row['Gamma'], axis=1)
df1['schedule delay cost2'] = df1.apply(lambda row: (row['t_star_high'] - (row['passenger arrival2'] + (row['walk cost2']*240)))*row['Beta'] if (row['passenger arrival2'] + (row['walk cost2']*240)) <= row['t_star_high'] else ((row['passenger arrival2'] + (row['walk cost2']*240)) - row['t_star_high'])*row['Gamma'], axis=1)
df1['schedule delay cost3'] = df1.apply(lambda row: (row['t_star_high'] - (row['passenger arrival3'] + (row['walk cost3']*240)))*row['Beta'] if (row['passenger arrival3'] + (row['walk cost3']*240)) <= row['t_star_high'] else ((row['passenger arrival3'] + (row['walk cost3']*240))- row['t_star_high'])*row['Gamma'], axis=1)
df1['schedule delay cost4'] = df1.apply(lambda row: (row['t_star_high'] - (row['passenger arrival4'] + (row['walk cost4']*240)))*row['Beta'] if (row['passenger arrival4'] + (row['walk cost4']*240)) <= row['t_star_high'] else ((row['passenger arrival4'] + (row['walk cost4']*240)) - row['t_star_high'])*row['Gamma'], axis=1)


df1["P_T_cost1"] = df1["P_car_time_cost1"] + df1['walk cost1'] + df1['schedule delay cost1']
df1["P_T_cost2"] =  df1["P_car_time_cost2"] + df1['walk cost2'] + df1['schedule delay cost2']
df1["P_T_cost3"] =  df1["P_car_time_cost3"] + df1['walk cost3'] + df1['schedule delay cost3']
df1["P_T_cost4"] =  df1["P_car_time_cost4"] + df1['walk cost4'] + df1['schedule delay cost4']

df1.to_csv("Final Match Matrix_01.csv", index=False)


print("% s seconds" % (time.time() - start))  


