#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# README (GROUP 31)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# -------------------------------------------------------------------------------
# DESCRIPTION
# -------------------------------------------------------------------------------
#
# The python script run_mvc.py defines a RuncMVC class that includes 8 functions:
# - parse_graph                 --> parse the input graph file [input: graph file; output: a graph data structure]
# - branch_and_bound            --> generate the optimal MVC solution using the branch and bound method [input: graph, cutoff time; output: best VC value, best MVC solution, and improved solutions]
# - min_weighted_vertex_cover   --> generate and the upper bound of the MVC solution for the input graph (a helper function for branch_and_bound) [input: graph, weight; output: 2-approximate vertex cover]
# - heuristic_approximation     --> generate the near-optimal (OPT <= sol <= 2OPT) MVC solution using the heuristic approximation method [input: graph, cutoff time, random seed; output: best VC value, best MVC solution, and improved solutions]
# - hill_climbing               --> generate the near-optimal MVC solution using the hilling climbing (local search) method [input: graph, cutoff time, random seed; output: best VC value, best MVC solution, and improved solutions]
# - simulated_annealing         --> generate the near-optimal MVC solution using the simulated annealing (local search) method [input: graph, cutoff time, random seed; output: best VC value, best MVC solution, and improved solutions]
# - check_valid_vc              --> check if the input vertex cover is valid (a helper function for hill_climbing and simulated_annealing) [input: vertex cover, removed vertex, graph; output: validity of the vertex cover]
# - main                        --> execute parsing input arguments, parsing graph, calling mvc method function, and writing .sol and .trace file [input: NA; output: NA]
#
# -------------------------------------------------------------------------------
# TO RUN THE CODE
# -------------------------------------------------------------------------------
#
# - step 1 --> create a folder (e.g. "output") to store the two types of output files
# - step 2 --> copy the "DATA" folder that contains the graph files to the created folder ("output")
# - step 3 --> copy the run_mvc.py file to the created folder ("output")
# - step 4 --> navigate the directory to the created folder ("output") in the command line
# - step 5 --> type in the inputs by following the required format to execute the run_mvc.py file (see an example below)
# 
# -------------------------------------------------------------------------------
# COMMAND EXAMPLE
# -------------------------------------------------------------------------------
# 
# python3 run_mvc.py exec -inst "dummy2.graph" -alg LS1 -time 600 -seed 2
#
# - "dummy2.graph" --> input graph file
# - LS1            --> input mvc method (BnB for branch and bound; Approx for heuristic approximation; LS1 for hill climbing; LS2 for simulated annealing)
# - 600            --> input cutoff time in second (s)
# - 2              --> input random seed
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++