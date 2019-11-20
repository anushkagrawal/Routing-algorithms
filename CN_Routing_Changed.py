
import os

# Initialization of all the variables.
router_matrix = []  # contains the Cost matrix for the Routers

matrix_set = 0  # used to check if the data is set or not

nodes = []
distances = {}

unvisited = {}

previous = {}

visited = {}

interface = {}

# stores the path from source node to destination node
path = []

start = 0
end = 0
numnodes = 0

# Function to print the choices when program starts.

def print_choices():
    

    print("\nCN 317 Link State Routing Simulator\n")

    print("(1) Input Network Topology File")

    print("(2) Build a Connection Table")

    print("(3) Shortest Path to Destination Router")

    print("(4) Exit")


    pass


def check_choices(command):
    if not command.isdigit():

        print("Please enter a number as command from given choices..")

        return -1

    else:

        command = int(command)

        if command > 4 or command < 1:

            print("Please enter a valid command from given choices..")

            return -1

        else:

            return command


# Function to process the given input file.


def process_file(fname):
    global matrix_set

    global router_matrix

    matrix_set = 0

    router_matrix = []

    with open(fname) as f:

        router_matrix = [list(map(int, x.split(" "))) for x in
                         f]  # Data from input file is stored in a two dimensional list(array).

    matrix_set = 1

    print("\nReview original topology matrix:\n")

    for line in router_matrix:

        for item in line:
            print(item, end=" ")

        print(" ")

    print

    set_distances(
        router_matrix)  # Distances are stored in a dictionary - key,value pair - with source router as key and distances in form of a dictionary as value.


# Function to store the distances in dictionary format.


def set_distances(router_matrix):
    global distances

    global nodes

    distances = {}

    nodes = []

    num_nodes = len(router_matrix)

    print("Creating Routing Tables ... ")

    for i in range(num_nodes):

        tempdict = {}

        for j in range(num_nodes):

            if i != j and router_matrix[i][j] != -1:
                tempdict[j + 1] = router_matrix[i][j]

        distances[i + 1] = tempdict

        nodes.append(i + 1)

        print("--------------------")

        for key, value in distances.items():
            print(key, value)

        print("---------------------")


def show_Values(c):
    print(" ")
    print("#################", c)
    print("---Unvisited Dict---")

    for k, v in unvisited.items():
        print(k, v)

    print("----------------------")

    print("----Previous Dict -----")
    for k, v in previous.items():
        print(k, v)

    print("----------------------")

    print("-----Interface Dict -------")
    for k, v in interface.items():
        print(k, v)

    print("----------------------")

    print("----Visited Dict-------")
    for k, v in visited.items():
        print(k, v)

    print("----------------------")
    print(" ")
    print("#################", c)


def dijkstra(start):
    global distances

    global nodes

    global unvisited

    global previous

    global visited

    global interface 

    # set the values to none for initialization.

    unvisited = {node: None for node in nodes}

    previous = {node: None for node in nodes}

    interface = {node: None for node in nodes}

    visited = {node: None for node in nodes}

    current = start

    currentDist = 0

    # setting the Cost to Start node=0
    unvisited[current] = currentDist

    print("Building the Router Table for Router:", start)

    while True:

        # show_Values(0)
        for next, distance in distances[current].items():

            # print("Next value is :",next)
            # if the node is visited already, do nothing
            if next not in unvisited: continue

            newDist = currentDist + distance

            # setting up the parent, for the shortest node/router
            if not unvisited[next] or unvisited[next] > newDist:

                unvisited[next] = newDist

                previous[next] = current

                if not interface[current]:

                    interface[next] = next
                

                else:

                    interface[next] = interface[current]
               
        visited[current] = currentDist

        # removing current node from list of Unvisited Nodes
        del unvisited[current]

        # to Check at least one node is left to explore
        shallWeStop = 1

        for x in unvisited:

            if unvisited[x]:
                shallWeStop = 0

                break

        # stop the iteration if no unvisited nodes
        if not unvisited or shallWeStop:
            break

        # store the all neighbours of the CUrrent node
        elements = [node for node in unvisited.items() if node[1]]

        current, currentDist = sorted(elements, key=lambda x: x[1])[0]



def shortest_path(start, end):
    global path

    path = []

    dest = int(end)

    src = int(start)

    path.append(dest)

    while dest != src:
        path.append(previous[dest])

        dest = previous[dest]

    path.reverse()

command = 0


while command != 4:

    print_choices()
    command = check_choices(input("\nCommand : "))

    # Accept the topology file.

    if command == 1:

        if matrix_set == 1:
            answer = input("\nThe network topology is already uploaded. Do you want to overwrite? (Y/N) :")

        if matrix_set == 0 or answer == 'Y' or answer == 'y':

            filename = input(
                "\nInput original network topology matrix data file[ NxN distance matrix] : ")

            if os.path.isfile(filename):

                process_file(filename)

                start = 0

                end = 0

            else:

                print("\nThe file does not exist. Please try again..")


    elif command == 2:

        if matrix_set == 1:

            for i in range(1, len(nodes) + 1):
                start = i
                dijkstra(start)

                print("---------------------------------")
                print("Routing Table For:", start)
                print("\nDestination\tInterface")

                for key in interface:
                    print(key, "\t\t", interface[key])

                print("---------------------------------")

        else:

            print("\nNo network topology matrix exist. Please upload the data file first.. ")

    elif command == 3:

        if matrix_set == 1:

            start = input("\nSelect Start Router:")
            end = input("\nSelect a destination router : ")

            dijkstra(int(start))
            if end.isdigit() and int(end) > 0 and int(end) <= len(router_matrix):

                if int(start) == 0:

                    print("\nNo source router selected yet. Please select a source router using choice : 2.")

                elif int(start) == int(end):

                    print("\nSource and Destination routers are same. Please select a different destination router.")

                elif not previous[int(end)]:

                    print(
                        "\nThere does not exist any route from Source : {} to Destination : {}. \nPlease select a different destination router. ".format(
                            'start', 'end'))

                else:

                    shortest_path(start, end)

                    print("\nThe shortest path from router %s to router %s : " % (start, end)),

                    for item in path:
                        print(str(item) + '  '),

                    print('')

                    cost = 0

                    if visited[int(end)]:
                        cost = visited[int(end)]

                    print("\nThe total cost is : ", cost)
            else:

                print("\nPlease enter a valid destination router.")

            pass
        else:

            print("\nNo network topology matrix exist. Please upload the data file first.. ")

    else:
        print("\n Simulation END....\n")







