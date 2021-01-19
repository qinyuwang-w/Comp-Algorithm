#!/usr/bin/python
# CSE6140 HW2
# This is an example of how your experiments should look like.
# Feel free to use and modify the code below, or write your own experimental code, as long as it produces the desired output.
# datafile: Nx3, u,v,weight
# Kruskal's algorithm:

import time
import sys
class Run_Experiment:
    def parse_edges(self, filename):
        # Write this function to parse edges from graph file to create your graph object
        with open(filename) as graphfile:
            edge_list = []
            count = 0
            for line in graphfile:
                edge = line.split()
                if count == 0:  
                    N,E = int(edge[0]),int(edge[1]) # first line: N=number of vertices, E=number of edges
                    #print(N,E)
                else:
                    v1 = int(edge[0])
                    v2 = int(edge[1])
                    w = int(edge[2])     # vertice1, vertice2, weight
                    edge_list.append((v1,v2,w)) 
                count = count + 1
            #print(edge_list)
        return N,E,edge_list
    
    def computeMST(self,N,edge_list):       
        edge_list.sort(key=lambda tup: tup[2])  # sort in terms of ascending weight of edges
        # foreach node, the initial root is itself,D-D, A-A, C-C
        # initial rank is 0
        root = dict((i,i) for i in range(N))  # for further identifying its component, whether they share the same root
        rank = dict((i,0) for i in range(N))    # number of nodes in the tree, ini=0
        # print(root)
        # print(rank)

        def find(vertice):   ##### recursively find its 'ultimate' root
            while root[vertice] != vertice:
                vertice = root[vertice]
            return vertice
        
        def union(root1, root2):    # merge two components in terms of root's rank
            # attach smaller rank root to higher rank root
            if rank[root1] > rank[root2]:
                root[root2] = root1

            # if rank the same, attach one to anotherand increment rank by one    
            elif rank[root1] == rank[root2]:
                root[root2] = root1
                rank[root1] =  rank[root1] + 1
                
            # same as first case    
            else:    
                root[root1] = root2
                
        mst = []
        mst_wt = 0
        mst_edge = 0
        
        j = 0
        while(mst_edge < N-1):# Kruskal's: not forming cycle (at most N-1 edges)     
            vertice1, vertice2, weight = edge_list[j]
            root1 = find(vertice1)  # find the ultimate root and 
            root2 = find(vertice2)
            
            if root1!= root2:  # if from different component AND not cycle
                # print("union")
                union(root1, root2)    # merge    
                mst.append((vertice1, vertice2, weight))
                mst_edge = mst_edge + 1
                mst_wt = mst_wt + weight
            j = j + 1   
        return mst_wt,mst   # careful with the order of return variables
   		
    def recomputeMST(self,u, v, weight,N,mst):
        edge_list = mst.copy()
        edge_list.append((u,v,weight))    
        new_mst_wt,new_mst = self.computeMST(N,edge_list)   
        return new_mst_wt,new_mst
    
    def main(self):

        num_args = len(sys.argv)

        if num_args < 4:
            print ("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        #Construct graph
        
        N,E,edge_list = self.parse_edges(graph_file)

        start_MST = time.time() #time in seconds
        MSTweight,mst = self.computeMST(N,edge_list) #call MST function to return total weight of MST
        total_time = (time.time() - start_MST) * 1000 #to convert to milliseconds

        #Write initial MST weight and time to file
        output = open(output_file, 'w')
        output.write(str(MSTweight) + " " + str(total_time)+'\n')

        #Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:
                #parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)

                u,v,weight = edge_data[0], edge_data[1], edge_data[2]

                #call recomputeMST function
                start_recompute = time.time()
                new_weight,new_mst = self.recomputeMST(u, v, weight,N,mst)
                total_recompute = (time.time() - start_recompute) * 1000 # to convert to milliseconds

                # for the next iteration
                mst=new_mst.copy()
                
                #write new weight and time to output file
                output.write(str(new_weight) + " " + str(total_recompute)+'\n')
                
        output.close()

if __name__ == '__main__':
    # run the experiments
    runexp = Run_Experiment()
    runexp.main()