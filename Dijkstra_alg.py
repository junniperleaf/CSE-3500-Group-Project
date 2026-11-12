import random
import networkx as nx
import matplotlib as plt

def generate_weighted_graph(num_verticies, num_edges, directed= False, weight_range=(1,10)):
    '''error handling'''
    if num_verticies <1:
        raise ValueError("There must be more than 1 node")

    if num_edges<num_verticies-1:
        raise ValueError("There should be enough edges to connect all nodes")

    if num_edges>num_verticies:
        raise ValueError("Too many edges")

    '''Creating graph'''
    if directed:
        max_edges= num_verticies *(num_verticies-1)
        G= nx.DiGraph()
    else:
        max_edges= num_verticies *(num_verticies-1)//2
        G=nx.Graph()

    G.add_nodes_from(range(num_verticies))

    '''Creating spanning tree'''
    nodes= list(G.nodes)
    random.shuffle(nodes)
    possible_edges=[]

    for i in range(num_verticies-1):
        weight= random.randint(*weight_range)
        G.add_edge(nodes[i], nodes[i+1], weight=weight)

    '''Add remaining edges'''
    for u in range(num_verticies):
        for v in range(num_verticies):
            if u!=v and not G.has_edge(u,v):
                possible_edges.append((u,v))

    random.shuffle(possible_edges)

    for u,v in possible_edges[:num_edges- (num_verticies-1)]:
        weight= random.randint(*weight_range)
        G.add_edge(u, v, weight= weight)

    return G


def visualizer(Graph):
  '''Visualize graph with weighting'''
  visualize= nx.spring_layout(Graph)
  nx.draw(Graph, with_labels=True, node_color='pink', edge_color='gray', node_size=100)
  plt.show()
  

if __name__== '__main__':
    user_option= input("Hello and welcome to the Dijkstra visualizer!" \
    "would you like to use a random graph of a premade one?: RANDOM || PREMADE\n")

    if (user_option!= "RANDOM" or user_option!= "PREMADE"):
        print("That was not a valid option! Please choose again!\n")
        user_option= input("Would you like to use a random graph of a premade one?: RANDOM || PREMADE\n")
    elif (user_option== 'PREMADE'):
        premade_choice= input("Great! Which premade option would you like to run?:" \
        "PREMADE 1 || PREMADE 2 || PREMADE 3\n")

        if (premade_choice== 'PREMADE 1'):
            graph=generate_weighted_graph(6, 10, False, (1,10))

        elif(premade_choice== 'PREMADE 2'):
            graph=generate_weighted_graph(5, 8, False, (1,20))

        elif (premade_choice== 'PREMADE 3'):
            graph=generate_weighted_graph(7, 12, False, (2,15))

        else:
            print("That was not a valid option! Please choose again!\n")
            premade_choice= input("Great! Which premade option would you like to run?:" \
                    "PREMADE 1 || PREMADE 2 || PREMADE 3\n")
    else:
        num_verticies= random.randint(1, 10)
        num_edges= random.randint(1, num_verticies)
        while(num_edges>num_verticies):
                    print("Num of edges was more than verticies. Trying again...\n")
                    num_edges= random.randint(1, num_verticies)
                    

        dir_option= random.randint(0, 1)
        if dir_option== 0:
            directed= False
        elif dir_option== 1:
            directed= True

        print(directed)

        max_weight= random.randint(2, 20)
        weight_range= (1, max_weight)
        
        graph= generate_weighted_graph(num_verticies, num_edges, directed, weight_range)
        visualizer(graph)

    '''Dijkstra'''
    dijkstra_path= nx.dijkstra_path(graph, 0, num_verticies-1, weight= 'weight')

