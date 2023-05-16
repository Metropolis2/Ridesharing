
import json
import zstandard as zstd
import math
import pandas as pd
import numpy as np

from tqdm import tqdm
import time
start = time.time()

#read matching file
df = pd.read_csv("matchings_and_alone_01.csv")
df = df[['id passenger']]
print(df['id passenger'][5])
df1 = df['id passenger'].tolist()
#Agents input read
i_agents = json.load(open('agents.json'))
input_01 = []
p = 0
for x in i_agents:
    if x['id'] in df1:
        print(x['id'])
    else:
        id = {"id": x["id"]}    
        my_list = x
        input_01.append(my_list)
    p += 1


json_string = json.dumps(input_01)

# Write the JSON formatted string to a file
with open('new_metropolis_input.json', 'w') as file:
    file.write(json_string)

