# Import necessary Python libraries
import networkx as nx
import time
import sys
import random
import queue
import math
from copy import deepcopy as dc

# Define the RunMVC class that contains a graph parsing function, four mvc method (BnB|Approx|LS1 (HC)|LS2 (SA)) functions with two helper functions, and a main() function
class RunMVC:
    
    # This function is to parse vertices and edges in graph data structure using python library networkx
    def parse_graph(self, filename):
        # Initialize G with Graph() data structure in networkx 
        G = nx.Graph()

        # Read graph file
        f = open(filename)
        content = f.readlines()
        
        # Read first line in graph file and record vertex count and edge count
        first_line = content[0].split()
        num_ver = int(first_line[0])
        num_edg = int(first_line[1])
        
        # Read adjacency list line by line for each vertex
        for i in range(1, num_ver + 1):
            # Add node i in G
            G.add_node(i)
            
            # Add each edge associated with vertex i
            try:
                eachline = content[i].strip().split()
                edges = [int(nd) for nd in eachline]
                for e in edges:
                    G.add_edge(i, e)
            except ValueError:
                pass
        return G
    
    # This function implements branch and bound (BnB) method to generate optimal MVC solution
    def branch_and_bound(self, G, cutoff_time):
        # Start timing
        start = time.time()

        # Initialize the improved solutions (improved_solution) with an empty list
        improved_solution = []
        # Add the time log and the associated inital best solution (VC value) as a pair in the improved solutions
        improved_solution.append((time.time() - start, len(list(G.nodes))))
        # Initialize the best solution (VC) with the return value (a set) from the helper function of min_weighted_vertex_cover(G, None)
        VC = self.min_weighted_vertex_cover(G, None)
        # Initialize the upper bound as the size of initial solution (VC)
        upperbound = len(VC)
        # Add the time log and the associated inital upper bound constrained best solution if it is improved
        if upperbound < len(list(G.nodes)):
        	improved_solution.append((time.time() - start, len(VC)))
        
        # Sort the vertices by its degree in ascending order and store as pairs of (vertex, vertex's degree) in a list (degree_sorted)
        degree_sorted = sorted(G.degree(),key=lambda x: x[1]) 

        # Initialize a stack data structure (q) with queue.LifoQueue()
        q = queue.LifoQueue()
        # Initialize current vertex cover (I) with an empty list
        I = []
        # Initialize the remaining vertices (V_remaining) with an empty list
        V_remaining = []
        # Add each vertex in the remaining vertices by the ascending order of degree
        for nd in degree_sorted:
            V_remaining.append(nd)
        # Initilaze the remaining graph (G_remaining) with a deep copy of original graph (G)
        G_remaining = dc(G)
        # Put a pair (current vertex cover (I), remaining vertices (V_remaining), remaining graph (G_remaining)) into stack q
        q.put((I,V_remaining, G_remaining))
        
        # Record the time duration (runtime) before the following while loop
        runtime = time.time() - start
        
        # Iteratively pop subproblem out of stack while runtime not exceeding cutoff time threshold
        while(not q.empty() and runtime < cutoff_time): # still worth searching
            # Stack pop pair (current vertex cover, remaining vertices, remaining graph)
            Inc,V_rem,G_rem = q.get()
            
            # Update the lowerbound with the current vertex cover and the remaining graph using the helper fucntion (maximal_matching) in networkx 
            lowerbound = len(Inc) + len(nx.maximal_matching(G_rem)) # set LB = (current VC) + (max_matching of Graph_Remain)
            
            # A new MVC solution is generated when all the edges are covered
            if len(G_rem.edges())==0: #if no more edges left, this branch is over
                # Update the best MVC solution (VC) and corresponding upper bound if the solution is improved
                if len(Inc) < upperbound:
                    # Update the upper bound
                    upperbound = len(Inc)
                    # Record the time log and the associated improved VC value
                    improved_solution.append((time.time() - start, len(Inc)))
                    # Update the the best MVC solution
                    VC = Inc
            # The solution hasn't been generated yet, keep exploring the subproblems
            else:
                # Retrieve the vertex with the highest degree (v) from the remaining vertice list (if not empty)
                if len(V_rem)!=0:   
                    v, v_degree = V_rem.pop()
                
                # Expand the subproblems if the lowerbound is no more than the upper bound (valid)
                if lowerbound <= upperbound:
                    # One subproblem: add all neighbors of v to the current vertex cover
                    V_I = Inc
                    # Add all neighbors of v in the remaining graph into the vertex cover 2 (frontier set, V_I)
                    V_I = V_I + list(G_rem.neighbors(v))
                    # Remove all neighbors of v from the remaining vertice list (V_R)
                    V_R = V_rem
                    V_R = list(filter(lambda a: a[0] not in G_rem.neighbors(v), V_R))  # exclude v.neighbor
                    # Remove all neighbors of v from the remaining graph (G_nextrem)
                    G_nextrem = dc(G_rem)
                    G_nextrem.remove_nodes_from(list(G_rem.neighbors(v))) 
                    # put this subproblem into stack
                    q.put((dc(V_I), dc(V_R), dc(G_nextrem)))
                    
                    # Another subproblem: add v to the current vertex cover
                    # Remove v from the remaining graph (G_rem)
                    G_rem.remove_node(v)
                    # Add v into the vertex cover (frontier set, Inc)
                    Inc.append(v)
                    # put this subproblem into stack
                    q.put((dc(Inc), dc(V_rem), dc(G_rem)))
            
            # Record the corrent run time in the end of each iteration in while loop
            runtime = time.time() - start
        
        # Return best VC value, best MVC solution, and improved solutions
        return len(VC), VC, improved_solution
    
    # This helper function return the 2-approximate vertex cover as the upperbound for the MVC solution
    def min_weighted_vertex_cover(self, G, weight=None):
        # Define a weight function for vertices (default weight is 1)
        weight_func = lambda nd: nd.get(weight, 1)
        
        # Define a cost dictionary with vertex ID as the key and its weight (calculated by weight_func) as the value
        cost = dict((n, weight_func(nd)) for n, nd in G.nodes(data=True))
        
        # Iterate each edge in the edge set of grpah G
        for u,v in G.edges():
            # Calculate the minimum cost among the two end points (u, v) of the current edge
            min_cost = min([cost[u], cost[v]])
            # Update the cost of u and v via normalization
            cost[u] = cost[u] - min_cost
            cost[v] = cost[v] - min_cost

        # Returns an approximate minimum weighted vertex cover (the selected vertices is characterized of normalized cost being 0)
        # The total weight of the set is guaranteed to be at most twice the total weight of the minimum weight vertex cover
        return set(u for u in cost if cost[u] == 0)
    
    # This function implements heuristic approximation (Approx) method to generate near-optimal MVC solution (OPT <= sol <= 2OPT)
    def heuristic_approximation(self, G, cutoff_time, random_seed):
        # Start timing
        start = time.time()

        # Initialize the current MVC solution (vertex_cover) with an empty list
        vertex_cover = []
        # Initialize the improved solutions (improved_solution) with an empty list
        improved_solution = []
        # Initialize the uncovered edges list (uncovered_edges) with all the edges of the graph G
        uncovered_edges = list(G.edges())
        
        # Initialize random seed with the input seed
        random.seed(random_seed)

        # Record the time duration (runtime) before the following while loop
        runtime = time.time() - start

        # Iterate until the uncovered edge list is empty or the runtime exceeding the cutoff time threshold
        while uncovered_edges != [] and runtime < cutoff_time:
            # Randomly select an edge within the uncovered edge list and assign its two end points to u and v, respectively
            u, v = random.choice(uncovered_edges)
            # Add the two end points of the randomly selected edge (u and v) into the vertex cover list
            vertex_cover.append(u)
            vertex_cover.append(v)
            # Remove all the edges that have either u or v as one of the end points from the uncovered edge list
            uncovered_edges = list(filter(lambda a: a[0] != u and a[0] != v and a[1] != u and a[1] != v, uncovered_edges))
            
            # Record the corrent run time in the end of each iteration in while loop
            runtime = time.time() - start
        
        # Record the time log and the associated improved VC value (only one pair since the valid solution is only generated after the while loop)
        improved_solution.append((time.time() - start, len(vertex_cover)))
        
        # Return best VC value, best MVC solution, and improved solutions
        return len(vertex_cover), vertex_cover, improved_solution

    # This function implements hill climbing (LS1, HC) method to generate near-optimal MVC solution
    def hill_climbing(self, G, cutoff_time, random_seed):
        # Start timing
        start = time.time()

        # Initialize the current MVC solution (vertex_cover) with all the vertices of G
        vertex_cover = list(G.nodes)
        # Initialize the improved solutions (improved_solution) with an empty list
        improved_solution = []
        # Add the time log and the associated inital MVC solution as a pair in the improved solutions
        improved_solution.append((time.time() - start, len(vertex_cover)))
        # Initialize best VC value (best_vc_size) with the count of all vertices of G
        best_vc_size = len(G.nodes)

        # Sort the vertices by its degree in ascending order and store as pairs of (vertex, vertex's degree) in a list (degree_sorted)
        degree_sorted = sorted(G.degree(), key=lambda x: x[1])
        
        # Initialize random seed with the input seed
        random.seed(random_seed)

        # Record the time duration (runtime) before the following while loop
        runtime = time.time() - start
        
        # Iterate until the vertice list (sorted by degree) is empty or the runtime exceeding the cutoff time threshold
        while degree_sorted != [] and runtime < cutoff_time:
            # Retrieve the vertices with the smallest degree and store them in a list (least_degree_vertices)
            least_degree_vertices = list(filter(lambda a: a[1] == degree_sorted[0][1], degree_sorted))
            
            # Iterate each vertex in the least degree vertice list while not exceeding the cutoff time
            while least_degree_vertices != [] and runtime < cutoff_time:
                # Randomly select a vertex within the least degree vertice list
                cur_vertex, cur_degree = random.choice(least_degree_vertices)
                # Remove this randomly selected vertex from current vertex cover
                vertex_cover.remove(cur_vertex)
                # Check the validity of the updated vertex cover
                if not self.check_valid_vc(vertex_cover, cur_vertex, G):
                    # Add this vertex back to the current vertex cover if the validity is broken
                    vertex_cover.append(cur_vertex)
                
                # Remove this randomly selected vertex from the least_degree_vertices list and the degree_sorted list
                least_degree_vertices.remove((cur_vertex, cur_degree))
                degree_sorted.remove((cur_vertex, cur_degree))
                
                # Update the best MVC solution (best_vc) and corresponding VC value (best_vc_size) if the solution is improved
                if len(vertex_cover) < best_vc_size:
                    # Record the time log and the associated improved VC value
                    improved_solution.append((time.time() - start, len(vertex_cover)))
                    # Update the best VC value
                    best_vc_size = len(vertex_cover)
                    # Update the best MVC solution
                    best_vc = vertex_cover
                
                # Record the corrent run time in the end of each iteration in inner while loop
                runtime = time.time() - start
            
            # Record the corrent run time in the end of each iteration in outer while loop
            runtime = time.time() - start

        # Return best VC value, best MVC solution, and improved solutions
        return best_vc_size, best_vc, improved_solution

    # This function implements simulated annealing (LS2, SA) method to generate near-optimal MVC solution
    def simulated_annealing(self, G, cutoff_time, random_seed):
        # Start timing
        start = time.time()
        
        # Initialize the current MVC solution (vertex_cover) with all the vertices of G
        vertex_cover = list(G.nodes)
        # Initialize the improved solutions (improved_solution) with an empty list
        improved_solution = []
        # Add the time log and the associated inital MVC solution as a pair in the improved solutions
        improved_solution.append((time.time() - start, len(vertex_cover)))
        # Initialize best VC value (best_vc_size) with the count of all vertices of G
        best_vc_size = len(G.nodes)
        # Get total edge count of G and assign it to edge_num
        edge_num = len(G.edges)
        
        # Initialize temperature (temp) as 100, end temperature (end_temp) as 1e-3, and folding scale ratio (decreasing_ratio) of 0.99999
        temp = 100
        end_temp = 1e-3
        decreasing_ratio = 0.99999
        
        # Initialize random seed with the input seed
        random.seed(random_seed)

        # Record the time duration (runtime) before the following while loop
        runtime = time.time() - start

        # Iterate until the current temperature is no more larger than end temperature or the runtime exceeding the cutoff time threshold
        while temp > end_temp and runtime < cutoff_time:
            # Update the current temperature
            temp = temp * decreasing_ratio
            
            # Randomly pick a vertex (random_vertex) from the vertice set of G
            random_vertex = random.choice(list(G.nodes)) 
            
            # If the randomly selected vertex is in current vertex cover
            if random_vertex in vertex_cover:
                # Remove this randomly selected vertex from current vertex cover
                vertex_cover.remove(random_vertex)
                # Check the validity of the updated vertex cover
                if not self.check_valid_vc(vertex_cover, random_vertex, G):
                    # Add this vertex back to the current vertex cover if the validity is broken
                    vertex_cover.append(random_vertex)
            # If the randomly selected vertex is NOT in current vertex cover
            else:
                # Add this vertex into the current vertex cover
                vertex_cover.append(random_vertex)     
                # Calculate the probability of this vertex to be kept in the current vertex cover
                p = math.exp(-(1 - G.degree(random_vertex) / edge_num) / temp)
                # If the calculated probability is smaller than the randomly generated value betweeon 0 and 1, remove this vertex from the current vertex cover
                if p < random.uniform(0, 1):
                    vertex_cover.remove(random_vertex)
            
            # Update the best MVC solution (best_vc) and corresponding VC value (best_vc_size) if the solution is improved
            if len(vertex_cover) < best_vc_size:
                # Record the time log and the associated improved VC value
                improved_solution.append((time.time() - start, len(vertex_cover)))
                # Update the best VC value
                best_vc_size = len(vertex_cover)
                # Update the best MVC solution
                best_vc = vertex_cover
            
            # Record the corrent run time in the end of each iteration in while loop
            runtime = time.time() - start

        # Return best VC value, best MVC solution, and improved solutions
        return best_vc_size, best_vc, improved_solution           

    # This helper function checks if the input vertex cover (vertex_cover) is valid (covering all the edges of graph G) if removing the input vertex (cur_vertex)
    def check_valid_vc(self, vertex_cover, cur_vertex, G):
        # Retrieve all the neighbors of the cur_vertex
        cur_neighbors = list(G.neighbors(cur_vertex))
        
        # Iterate each neighbor of the neighbors of the cur_vertex
        for neighbor in cur_neighbors:
            # If a neighbor is not in the input vertex cover, return False implying the input vertex cover is not valid
            if neighbor not in vertex_cover:
                return False
        
        # Return True if all the neighbors of the cur_vertex are in the input vertex cover (removing cur_vertex does not affect the covered edged by the vertex cover)
        return True

    # This main() function contains modules of parsing input arguments, parsing graph, calling corresponding mvc method function, and writing .sol and .trace file
    def main(self):
        # Count the total number of input arguments
        num_args = len(sys.argv)
        
        # Throw an error if the total number of input arguments is less than 10
        if num_args < 10:
            print("error: not enough input arguments")
            exit(1)
            
        # Assign the corresponding info to graph_file, mvc_method, cutoff_time, and random_seed from the input arguments
        graph_file = sys.argv[3]
        mvc_method = sys.argv[5]
        cutoff_time = int(sys.argv[7])
        random_seed = int(sys.argv[9])
        
        # Use parse_graph function to parse the targeted graph file and store the graph as G
        G = self.parse_graph("./DATA/" + graph_file)
        
        # Call the corresponding function to generate near-optimal MVC solution according to the input mvc method
        # and throw an error if the input mvc method is not in the method pool
        if mvc_method == "BnB":
            vertex_cover_size, vertex_cover, improved_solution = self.branch_and_bound(G, cutoff_time)
        elif mvc_method == "Approx":
            vertex_cover_size, vertex_cover, improved_solution = self.heuristic_approximation(G, cutoff_time, random_seed)
        elif mvc_method == "LS1":
            vertex_cover_size, vertex_cover, improved_solution = self.hill_climbing(G, cutoff_time, random_seed)
        elif mvc_method == "LS2":
            vertex_cover_size, vertex_cover, improved_solution = self.simulated_annealing(G, cutoff_time, random_seed)
        else:
            print("error: not correct input method")
        
        # Separately define the names of .sol file and .trace file according to the property of the mvc method (if random seed is used)
        if mvc_method == "LS1" or mvc_method == "LS2" or mvc_method == "Approx":
            sol_file_name = graph_file.split('.')[0] + "_" + mvc_method + "_" + str(cutoff_time) + "_" + str(random_seed) + ".sol"
            trace_file_name = graph_file.split('.')[0] + "_" + mvc_method + "_" + str(cutoff_time) + "_" + str(random_seed) + ".trace"
        else:
            sol_file_name = graph_file.split('.')[0] + "_" + mvc_method + "_" + str(cutoff_time) + ".sol"
            trace_file_name = graph_file.split('.')[0] + "_" + mvc_method + "_" + str(cutoff_time) + ".trace"
        
        # Sort the mvc solution in the ascending order of vertex ID
        vertex_cover = sorted(vertex_cover)
        
        # Create and write the .sol file with the required format
        sol_file = open(sol_file_name, 'w')
        sol_file.write(str(vertex_cover_size) + "\n")
        for i in range(vertex_cover_size - 1):
            sol_file.write(str(vertex_cover[i]) + ',')
        sol_file.write(str(vertex_cover[vertex_cover_size - 1]))       
        
        # Create and write the .trace file with the required format
        trace_file = open(trace_file_name, 'w')
        for i in range(len(improved_solution)):
            trace_file.write(str(improved_solution[i][0]) + ', ' + str(improved_solution[i][1]) + "\n")

# Initialize the RunMVC() class and execute the main() function
if __name__ == '__main__':
    runmvc = RunMVC()
    runmvc.main()