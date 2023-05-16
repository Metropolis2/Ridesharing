import pandas as pd
import numpy as np

df2 = pd.read_csv("Possible matchings_01.csv", index_col = None) 

df1 = pd.read_csv("Final Match Matrix_01.csv")

df1 = df1.drop(columns=['epsilon D', 'epsilon P'])#'Alpha', 'origin driver', 'destination driver', 'origin passenger', 'destination passenger', 'Beta', 'Gamma', 't_star_high', 't_star_low', 'u',#, 'Driver alone cost', 'Passenger alone cost'

merged_df = pd.merge( df2, df1, on=['id driver','id passenger'], how='outer')


df_grouped = merged_df.groupby([ 'origin driver', 'destination driver', 'origin passenger', 'destination passenger']).apply(lambda x: x.fillna(method='ffill').fillna(method='bfill'))
    
    
df_grouped.to_csv("unique to full output_01.csv", index=False)


