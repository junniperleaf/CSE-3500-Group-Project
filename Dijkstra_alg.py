import random
import networkx as nx
import matplotlib.pyplot as plt

def generate_weighted_graph(num_verticies, num_edges, directed= False, weight_range=(1,10)):
    '''error handling'''
    if num_verticies <1:
        raise ValueError("There must be more than 1 node")

    if num_edges<num_verticies-1:
        raise ValueError("There should be enough edges to connect all nodes")

    if directed:
        max_edges= num_verticies *(num_verticies-1)
        G= nx.DiGraph()
    else:
        max_edges= num_verticies *(num_verticies-1)//2
        G=nx.Graph()
    
    if num_edges>max_edges:
        raise ValueError("Too many edges")

    '''Creating graph'''
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
  visualize= nx.spring_layout(Graph, seed=42)
  nx.draw(Graph, visualize, with_labels=True, node_color='pink', edge_color='gray', node_size=700, arrows=Graph.is_directed())
  edge_labels=nx.get_edge_attributes(Graph, 'weight')
  nx.draw_networkx_edge_labels(Graph, visualize, edge_labels= edge_labels)
  plt.show()
  

if __name__== '__main__':
    user_option= input("Hello and welcome to the Dijkstra visualizer! " \
    "Would you like to use a random graph of a premade one?: RANDOM || PREMADE\n").upper()

    while (user_option!= "RANDOM" and user_option!= "PREMADE"):
        print("That was not a valid option! Please choose again!\n")
        user_option= input("RANDOM || PREMADE\n").upper()
    
    if (user_option== 'PREMADE'):
        premade_choice= input("Great! Which premade option would you like to run?:" \
        "PREMADE 1 || PREMADE 2 || PREMADE 3\n").upper()

        while(premade_choice!= 'PREMADE 1' and premade_choice!= 'PREMADE 2' and premade_choice!= 'PREMADE 3'):
            print("That was not a valid option! Please choose again!\n")
            premade_choice= input("PREMADE 1 || PREMADE 2 || PREMADE 3\n").upper()

        if (premade_choice== 'PREMADE 1'):
            num_verticies=6
            graph=generate_weighted_graph(num_verticies,5, False, (1,10))

        elif(premade_choice== 'PREMADE 2'):
            num_verticies=8
            graph=generate_weighted_graph(num_verticies, 7, False, (1,20))

        elif (premade_choice== 'PREMADE 3'):
            num_verticies=12
            graph=generate_weighted_graph(num_verticies, 11, False, (2,15))
    else:
        num_verticies= random.randint(2, 10)

        dir_option= random.randint(0, 1)
        if dir_option== 0:
            directed= False
            max_edges= num_verticies *(num_verticies-1)//2
        else:
            directed= True
            max_edges= num_verticies *(num_verticies-1)
        
        num_edges= random.randint(num_verticies-1,  max_edges)
        max_weight= random.randint(2, 20)
        weight_range= (1, max_weight) 
        graph= generate_weighted_graph(num_verticies, num_edges, directed, weight_range)

    '''Dijkstra'''
    try:
        dijkstra_path = nx.dijkstra_path(graph, 0, num_verticies - 1, weight='weight')
        print(f"Shortest path using Dijkstra: {dijkstra_path}")
        visualizer(graph)
    except nx.NetworkXNoPath:
        print("No path exists!")
        visualizer(graph)
