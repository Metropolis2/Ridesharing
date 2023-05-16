**# METROPOLIS-Ridesharing**

This repository contains script files for ridesharing in a simulaton of Metropolis for the any network.

**How to Start**

**Step 1:**
* Run the metropolis software using agents input file and get the output files
* Make sure that all input output files and software everything are in the same folder

**Step 2:**
* Run 1.Identify_matches.py 
* It will first merge input and output files on the basis of unique agent id and create a merged file
* After that it will find the possible matches on the criteris that matching utility in the case of free flow case should be higher then the utility of agents traveling alone (Driver and passenger pair)
  
**Step 3:**
* Run 2.Detour_scenarios.py 
* First it will find all the unique driver passenger OD pairs
* It will create all four detour scenarios using driver and passenger OD pairs
  
**Step 4:**
* Run 3.Preday_input.py 
* Using all the detour scenarios it will create an json input file for the preday run

**Step 5:**
* Run the Metropolis preday model using compute_choices.exe
* use startcode_preday.txt to run the preday input file

**Step 6:**
* Run 4.After_preday.py
* it will read driver expected utility from the preday output file for all four detour scenarios
* Also it will compute the passenger travel and schedule delay cost for all detour scenarios
  
**Step 7:**
 * Run 5.Unique_to_all_agents.py
 * It will change all the unique driver and passenger OD pairs to again all possible matching scenarios

**Step 8:**
* Run 6.Optimization_input.py
* It will take only driver and passenger id's and their travel alone and matching utilities to create a input file for linear optimization
  
**Step 9:**
* Run 7.Linear_optimization.py
* It will find the optimal matching pairs of driver and passengers and traveling alone agents by maximising the utilities.
  
**Step 10:**
* Run 8.New_metropolis_input.py
* It will create a new input file for metropolis by removing all the matched passengers from the total agents
