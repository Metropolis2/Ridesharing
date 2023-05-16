# METROPOLIS-Ridesharing

This repository contains script files for ridesharing in a simulaton of Metropolis for the any network.

How to Start

Step 1:
  Run the metropolis software using agents input file and get the output files.
  Make sure that all input output files and software everything are in the same folder

Step 2:
  Run the first code 1.Identify matches_multicore.py 
  It will first merge input and output files on the basis of unique agent id and create a merged file
  After that it will find the possible matches on the criteris that matching utility in the case of free flow case should be higher then the utility of agents traveling alone (Driver and passenger pair)
  
Step 3:
  Run the second code 2.Cost computation.py 
  First it will find all the unique driver passenger OD pairs
  It will create all four detour scenarios using driver and passenger OD pairs.
  
Step 4:
  Run the second code 3.Preday_input.py 
  Using all the detour scenarios it will create an json input file for the preday run

Step 5:
  Run the Metropolis preday model using compute_choices.exe
  use startcode_preday.txt to run the preday input file

Step 6:
  
