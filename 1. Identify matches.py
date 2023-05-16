
import json
import zstandard as zstd
import math
import pandas as pd
import numpy as np
import itertools
from tqdm import tqdm
from multiprocessing import Pool
import time

start = time.time()


def sam(x, a_df, ttime):
    my_list = []
    #walking cost per second
    walk = 0.0041666
    id_D = x[0]
    i = int(x[1])
    j = int(x[2])
    alpha = -(x[4])
    beta = x[5]
    gamma = x[6]
    ta = x[7]
    ta0 = x[8]
    t0 = x[9]
    t1 = x[10]
    mu = x[11]
    u = x[12]
    epsilon_D = x[16]
    C_aD = x[13]  
    for y in a_df:
        k = int(y[1])
        l = int(y[2])
        
        #Four detour scenarios
        cost1_D = (ttime[i,k] + ttime[k,l] + ttime[l,j])
        cost1_P = (alpha)*ttime[k,l] 
        
        cost2_D = (ttime[i,k] + ttime[k,j] )
        cost2_P =  (alpha)*ttime[k,j] + walk*ttime[j,l]
        
        cost3_D = (ttime[i,l]  + ttime[l,j])
        cost3_P =  walk*ttime[k,i] + (alpha)*ttime[i,l]
        
        cost4_D = (ttime[i,j])
        cost4_P = (walk*ttime[k,i] + (alpha)*ttime[i,j] + walk*ttime[j,l])
        
        cost = [[cost1_D, cost1_P], [cost2_D, cost2_P], [cost3_D, cost3_P], [cost4_D, cost4_P]]
                    
        id_P = y[0]
        epsilon_P = y[17]
        C_aP = y[13]
        
        cost_all = []
        for z in cost:
            C_P = -(z[1]) + epsilon_P + 12
            C_D = -(alpha*z[0]) + mu*(math.log(((mu/beta)*(1-math.exp((beta*(-ta+z[0]+t0))/(mu))) - (mu/gamma)*(math.exp(-(((gamma)*(z[0]-ta+t1))/(mu)))-1)))+ np.euler_gamma) + epsilon_D
            zz = [C_D + C_P]
            cost_all.append(zz)
        s_max = max(cost_all)
        max_index = cost_all.index(s_max)
        if C_aD + C_aP <= s_max :
          my_tuple = (id_D, id_P, epsilon_D, epsilon_P)
          my_list.append(my_tuple) 
          #break
    df = pd.DataFrame(my_list)
    #df.columns = ["id driver","origin driver", "destination driver", "id passenger" ,"origin passenger", "destination passenger", "epsilon D", "epsilon P"]
    return df

if __name__ == "__main__":
    #read input file
    i_agents = json.load(open('agents.json'))
    #Agents output read
    def get_agent_results():
        dctx = zstd.ZstdDecompressor()
        with open('agent_results.json.zst', "br") as f:
            reader = dctx.stream_reader(f)
            data = json.load(reader)
        return data
    o_agents = get_agent_results()

    #extract useful data from input file
    input_01 = []
    for x in i_agents:
        id = {"id": x["id"]}    
        O_D = x["modes"][0]["value"]["legs"][0]["class"]["value"]
        alpha = x["modes"][0]["value"]["legs"][0]["travel_utility"]["value"]
        beta_gamma = x["modes"][0]["value"]["destination_schedule_utility"]["value"]
        time_period = x["modes"][0]["value"]["departure_time_model"]["value"]
        my_list = [id, O_D, alpha, beta_gamma, time_period]
        input_01.append(my_list)

    #merge id from input and output for origin destination
    merged_dict = []
    for i in range(len(o_agents)):
        aa = input_01[i][0]
        if aa["id"] == o_agents[i]["id"]:
            my_list1 = [input_01[i][1], o_agents[i], input_01[i][2], input_01[i][3], input_01[i][4]]
            merged_dict.append(my_list1)
            
    json_string = json.dumps(merged_dict)
    # Write the JSON formatted string to a file
    with open('merged_input_output.json', 'w') as file:
        file.write(json_string)

    def cost_computation(merged_dict):
        my_list = []
        for i in range(len(merged_dict)):
            id = merged_dict[i][1]['id']
            origin = merged_dict[i][0]['origin']
            destination = merged_dict[i][0]['destination']
            utility = merged_dict[i][1]["expected_utility"]
            ttime = merged_dict[i][1]["mode_results"]["value"]["legs"][0]["class"]["value"]["global_free_flow_travel_time"]
            alpha = merged_dict[i][2]['b']
            beta = merged_dict[i][3]['beta']
            gamma = merged_dict[i][3]['gamma']
            ta = merged_dict[i][3]['t_star_high']
            ta0 = merged_dict[i][3]['t_star_low']
            t0 = merged_dict[i][4]['period'][0]
            t1 = merged_dict[i][4]['period'][1]
            mu = merged_dict[i][4]['choice_model']['value']['mu']
            u = merged_dict[i][4]['choice_model']['value']['u']
            epsilon_D = np.random.normal(0, 2)
            epsilon_P = np.random.normal(0, 2)
            #C_P = (ttime * alpha) + epsilon_P
            #C_D = -(alpha)*ttime + mu*(math.log(((mu/beta)*(1-math.exp((beta*(-ta+ttime+t0))/(mu))) - (mu/gamma)*(math.exp(-(((gamma)*(ttime-ta+t1))/(mu)))-1)))) + epsilon_D
            my_tuple = (id, origin, destination, ttime,  alpha,  beta,  gamma, ta, ta0,  t0,  t1,  mu, u, utility, epsilon_D, epsilon_P)
            my_list.append(my_tuple)
        
        df = pd.DataFrame(my_list)
        df.columns = ["id","origin", "destination" , "free_flow travel time", "Alpha", "Beta", "Gamma","t_star_high", "t_star_low", "start period", "End period", "mu", 'u', "Travel alone utility", "epsilon D", "epsilon P"]
        return df

    df_a = cost_computation(merged_dict)

    ttime = df_a.pivot_table(index='origin', columns='destination', values='free_flow travel time', aggfunc='mean')
    ttime = ttime.values
    print(ttime[1][2])
    
    #chooce 1% of travelers
    df_a = df_a.sample(frac=0.01)
    a_df = df_a.values

    with Pool() as pool:
      result = list(tqdm(pool.starmap(sam, [(row, a_df, ttime) for row in a_df]), total=len(df_a)))
    processed_df = pd.concat(result, join='outer')
    print("Program finished!")

df_a.to_csv("all_travelers.csv", index = False)
processed_df.columns = ["id driver", "id passenger" , "epsilon D", "epsilon P"]
processed_df.to_csv("Possible matchings_01.csv", index=False)

print("% s seconds" % (time.time() - start))
