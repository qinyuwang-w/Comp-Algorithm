#!/usr/bin/python
# CSE6140 HW2
# This is an example of how your experiments should look like.
# Feel free to use and modify the code below, or write your own experimental code, as long as it produces the desired output.
import time
import sys


class RunExperiments:
    def parse_edges(self, filename):
        # Write this function to parse edges from graph file to create your graph object
        pass

    def computeMST(self, G):
        # Write this function to compute total weight of MST
        pass

    def recomputeMST(self, u, v, weight, G):
        # Write this function to recompute total weight of MST with the newly added edge
        pass

    def main(self):

        num_args = len(sys.argv)

        if num_args < 4:
            print("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        # Construct graph
        G = self.parse_edges(graph_file)

        start_MST = time.time()  # time in seconds
        # call MST function to return total weight of MST
        MSTweight = self.computeMST(G)
        total_time = (time.time() - start_MST) * \
            1000  # to convert to milliseconds

        # Write initial MST weight and time to file
        output = open(output_file, 'w')
        output.write(str(MSTweight) + " " + str(total_time) + "\n")

        # Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:
                # parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)

                u, v, weight = edge_data[0], edge_data[1], edge_data[2]

                # call recomputeMST function
                start_recompute = time.time()
                new_weight = self.recomputeMST(u, v, weight, G)
                # to convert to milliseconds
                total_recompute = (time.time() - start_recompute) * 1000

                # write new weight and time to output file
                output.write(str(new_weight) + " " + str(total_recompute) + "\n")


if __name__ == '__main__':
    # run the experiments
    runexp = RunExperiments()
    runexp.main()
