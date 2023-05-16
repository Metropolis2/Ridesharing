import json
import zstandard as zstd
import math
import pandas as pd
import numpy as np
import copy
from tqdm import tqdm
import time

start = time.time()

matching_id = pd.read_csv("Possible matchings_01.csv", index_col = None)     
#matching_id = matching_id.sample(frac=0.05)   

all_travelers = pd.read_csv("all_travelers", index_col = None)
all_travelers = all_travelers.rename(columns={'id': 'id driver'})
all_travelers = all_travelers.drop(['Driver utility', 'Passenger utility', 'epsilon P','epsilon D'],axis = 1)

merged_df = pd.merge(matching_id,all_travelers,  on='id driver', how='left')
merged_df = merged_df.rename(columns={'origin': 'origin driver', 'destination': 'destination driver', 'Travel alone utility': 'Driver alone utility'})

all_travelers_p = all_travelers[['id driver', 'origin', 'destination', 'Travel alone utility' ]]
all_travelers_p = all_travelers_p.rename(columns={'id driver': 'id passenger', 'Travel alone utility': 'Passenger alone utility'})
final_df = pd.merge(merged_df , all_travelers_p,  on='id passenger', how='left')
final_df = final_df.rename(columns={'origin': 'origin passenger', 'destination': 'destination passenger'})
df = final_df

unique_matches = pd.DataFrame()
unique_driver = df['id driver'].unique()
for i in unique_driver:
    passengers = df[df['id driver'] == i]
    unique_rows = passengers.drop_duplicates(subset=['origin passenger',	'destination passenger'])
    #unique_matches = unique_matches.append(unique_rows)
    unique_matches = pd.concat((unique_matches, unique_rows))
unique_matches = unique_matches.reset_index(drop=True)

unique_matches["O1"] = unique_matches["origin driver"]
unique_matches["IO1"] = unique_matches["origin passenger"]
unique_matches["ID1"] = unique_matches["destination passenger"]
unique_matches["D1"] = unique_matches["destination driver"]

unique_matches["O2"] = unique_matches["origin driver"]
unique_matches["IO2"] = unique_matches["origin passenger"]
unique_matches["D2"] = unique_matches["destination driver"]

unique_matches["O3"] = unique_matches["origin driver"]
unique_matches["ID3"] = unique_matches["destination passenger"]
unique_matches["D3"] = unique_matches["destination driver"]

unique_matches["O4"] = unique_matches["origin driver"]
unique_matches["D4"] = unique_matches["destination driver"]

print("% s seconds" % (time.time() - start))

unique_matches.to_csv("Possible detour.csv", index=False)
