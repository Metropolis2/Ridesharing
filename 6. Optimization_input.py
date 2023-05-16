import pandas as pd
import numpy as np

df1 = pd.read_csv("unique to full output_01.csv")

x = 12

df1['matching utility1'] = df1['Driver expected utility1'] - df1['P_T_cost1'] + df1['epsilon D'] + df1['epsilon P'] + x
df1['matching utility2'] = df1['Driver expected utility2'] - df1['P_T_cost2'] + df1['epsilon D'] + df1['epsilon P'] + x
df1['matching utility3'] = df1['Driver expected utility3'] - df1['P_T_cost3'] + df1['epsilon D'] + df1['epsilon P'] + x
df1['matching utility4'] = df1['Driver expected utility4'] - df1['P_T_cost4'] + df1['epsilon D'] + df1['epsilon P'] + x

df1['travel alone utility'] = df1['Driver alone utility'] + df1['Passenger alone utility']

df1['max_matching_utility'] = df1.apply(lambda row: max(row['matching utility1'], row['matching utility2'], row['matching utility3'], row['matching utility4']), axis=1)

df = df1.loc[:,['id driver', 'id passenger', 'matching utility1', 'matching utility2', 'matching utility3', 'matching utility4', 'max_matching_utility', 'travel alone utility', 'Driver alone utility', 'Passenger alone utility']]

df = df.assign(matching=np.where(df['travel alone utility'] < df['max_matching_utility'], 1, 0))
print((df['matching']).value_counts())

df = df[df['matching'] ==1]
df.to_csv("optimization input_01.csv", index=False)
