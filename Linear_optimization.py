import pulp
import pandas as pd
from pulp import*
import time

start = time.time()

df = pd.read_csv("optimization input_01.csv")
df = df[df['matching'] == 1]
df = df[['id driver', 'id passenger', 'max_matching_utility', 'Driver alone utility', 'Passenger alone utility']]
df1 = df.to_dict()
df1 = pd.DataFrame(df1)

# get the unique drivers and passengers
unique_drivers = df1['id driver'].unique()
unique_passengers = df1['id passenger'].unique()

driver = df1["id driver"].tolist()
passenger = df1['id passenger'].tolist()
cost = df1['max_matching_utility'].tolist()
costs = dict(zip(zip(driver, passenger), cost))

#create travel alone utility dataframe
df_d = df[['id driver', 'Driver alone utility']].drop_duplicates(subset=['id driver'])
df_p = df[['id passenger', 'Passenger alone utility']].drop_duplicates(subset=['id passenger'])
new_df = pd.DataFrame({'id alone': df_d['id driver'].tolist() + df_p['id passenger'].tolist(), 'utility alone': df_d['Driver alone utility'].tolist() + df_p['Passenger alone utility'].tolist()})
df = new_df.drop_duplicates(subset=['id alone'])
alone = df['id alone'].to_dict()

# create the LP problem
prob = pulp.LpProblem('Matching Problem', LpMaximize)

# create decision variables
variables = LpVariable.dicts('Match', [(i, j) for i, j in costs.keys()], lowBound=0, cat='integer')
variablea = LpVariable.dicts('alone', [(k) for k in alone.values()], lowBound=0, cat='integer')

# objective function
prob += lpSum([df1.loc[(df1['id driver'] == i) & (df1['id passenger'] == j), 'max_matching_utility'].values[0] * variables[(i, j)] for (i, j) in costs.keys()] + [df.loc[(df['id alone'] == k), 'utility alone'].values[0]* variablea[(k)]  for k in alone.values()])

# set the constraints
for i in alone.values():
    prob += lpSum([[variables[(k, j)]for k, j in costs.keys() if k == i] + [variables[(k, j)] for k, j in costs.keys() if j == i]]  + variablea[(i)] ) == 1
    
prob.solve()

print("status:", LpStatus[prob.status])
print(f"Total cost: {value(prob.objective)}")

df3 = pd.DataFrame(0, index=range(len(alone.values())), columns=['id driver', 'id passenger', 'max_matching_utility', 'id alone' , 'utility alone'])
p = 0
for i, j in costs.keys():
        if variables[(i, j)].varValue == 1:
            #print(f"{i} is matched with {j} , cost: {df1.loc[(df1['id driver'] == i) & (df1['id passenger'] == j), 'max_matching_utility'].values[0]}")
            df3.loc[p,['id driver', 'id passenger', 'max_matching_utility',]] = i,j,df1.loc[(df1['id driver'] == i) & (df1['id passenger'] == j), 'max_matching_utility'].values[0]
            p += 1
p = 0
for i in alone.values():            
    if variablea[(i)].varValue == 1:
        #print(f"{i} is traveling alone (cost: {df.loc[(df['id alone'] == i), 'utility alone'].values[0]})")
        df3.loc[p,['id alone' , 'utility alone']] = i,df.loc[(df['id alone'] == i), 'utility alone'].values[0]
        p += 1

df3.to_csv("matchings_and_alone_01.csv", index=False)

print("% s seconds" % (time.time() - start))