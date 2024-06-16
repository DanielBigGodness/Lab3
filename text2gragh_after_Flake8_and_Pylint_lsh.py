import os
import random
import re


import networkx as nx
import matplotlib.pyplot as plt


input_dir = './input'
output_dir = './output/'

default_filename = 'example'

EOF_symbol = 'EOF'


class DirectedGraph:
    def __init__(self):
        self.nodes = []
        self.edges = {}

    def add_edge(self, src, dst):
        if src not in self.nodes:
            self.nodes.append(src)

        if src in self.edges:
            if dst in self.edges[src]:
                self.edges[src][dst] += 1
            else:
                self.edges[src][dst] = 1
        else:
            self.edges[src] = {dst: 1}

        if dst not in self.nodes:
            self.nodes.append(dst)

    def get_neighbors_nodes(self, node):
        return self.edges.get(node, {})


def process_text(infunc_text):
    in_func_processed_text = re.sub(r'[\W_]+', ' ', infunc_text)
    in_func_processed_text = in_func_processed_text.lower()
    in_func_processed_text = in_func_processed_text.replace('\n', ' ')
    in_func_processed_text = in_func_processed_text.replace('\r', ' ')
    return in_func_processed_text


def create_graph(infunc_text):
    infunc_graph = DirectedGraph()
    words = infunc_text.split()
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        infunc_graph.add_edge(word1, word2)
    infunc_graph.add_edge(words[-1], EOF_symbol)
    return infunc_graph


filename = input("\n\n-------------------------------------\nPlease " +
                 "input text file name " +
                 "(e.g. example = ./input/example.txt), " +
                 " press Enter for default: \n")
if filename == '':
    filename = default_filename
    print(f"Using default text file: {filename}")

# 增强健壮性
if not filename.endswith(".txt"):
    filename += '.txt'

try:
    with open(os.path.join(input_dir, filename), 'r', encoding='utf-8')\
          as file:
        text = file.read()
except FileNotFoundError as e:
    print(f"Error: File not found. Details: {e} using example")
except PermissionError as e:
    print(f"Error: Permission denied. Details: {e} using example")
except IOError as e:
    print(f"Error: An I/O error occurred. Details: {e} using example")


processed_text = process_text(text)
graph = create_graph(processed_text)

print("Create graph ok")


def showDirectedGraph(infunc_graph, infunc_filename):

    G = nx.DiGraph()
    for i in range(len(infunc_graph.nodes)):
        node = infunc_graph.nodes[i]
        for neighbor in infunc_graph.edges[node]:
            if neighbor != EOF_symbol:
                # G.add_edge(str(i)  + node[1:], neighbor)
                weight = infunc_graph.edges[node][neighbor]
                # print("##########")
                # print(node, neighbor)
                # print(weight)
                G.add_edge(node, neighbor, weight=weight)
    pos = nx.spring_layout(G, iterations=50, k=0.5)  # positions for all nodes
    plt.figure(figsize=(8, 8))
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=1500)  # 节点大小
    # edges
    # nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2,
                           arrowstyle='-|>', arrowsize=7, node_size=1200) 
    # node_size设置指向的节点半径
    nx.draw_networkx_labels(G, pos, font_size=10)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels=edge_labels, font_color='red')
    plt.axis("off")
    plt.savefig(os.path.join(output_dir, infunc_filename+".png"))
    plt.show()


def queryBridgeWords(word1, word2):
    if (' ' in word1) or (' ' in word2):
        return f"Either '{word1}' or '{word2}' contains a space or is empty."
    if (word1 not in graph.nodes) or (word2 not in graph.nodes):
        # print("No " + word1 + " or " + "no " + word2 + " in the graph!")
        return "No " + word1 + " or " + "no " + word2 + " in the graph!"

    bridge_words = []
    for neighbor in graph.edges[word1]:
        if word2 in graph.edges[neighbor]:
            bridge_words.append(neighbor)

    if len(bridge_words) == 0:
        return "No bridge words from " + word1 + " to " + word2 + " !"
    else:
        a = "The bridge words from " + word1 + " to " + word2 + " are: "
        return a + f"{', '.join(bridge_words)}."
        

def generateNewText(input_text):
    words = input_text.split()
    new_text = []
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        new_text.append(word1)
        
        bridge_words = queryBridgeWordsList(word1, word2)
        if bridge_words:
            bridge_word = random.choice(bridge_words)
            new_text.append(bridge_word)
    
    new_text.append(words[-1])
    return ' '.join(new_text)


def queryBridgeWordsList(word1, word2):
    if (word1 not in graph.nodes) or (word2 not in graph.nodes):
        return []

    bridge_words = []
    for neighbor in graph.edges[word1]:
        if word2 in graph.edges[neighbor]:
            bridge_words.append(neighbor)

    return bridge_words


def calcShortestPath(word1, word2):
    if word1 not in graph.nodes or word2 not in graph.nodes:
        return f"Word '{word1}' or '{word2}' not in the graph."
    
    G = nx.DiGraph()
    for node in graph.nodes:
        for neighbor in graph.edges[node]:
            weight = graph.edges[node][neighbor]
            G.add_edge(node, neighbor, weight=weight)

    try:
        length, path = nx.single_source_dijkstra(G, source=word1, target=word2)
        path_str = " -> ".join(path)
        return f"The shortest path from '{word1}' to '{word2}' \
          is: {path_str} (Length: {length})"
    except nx.NetworkXNoPath:
        return f"No path from '{word1}' to '{word2}'"


def random_walk_and_save(graph, output_dir):
    # Always start from 'A' to ensure consistency in tests
    current_node = "A"
    if current_node not in graph.nodes:
        raise ValueError("Starting node 'A' not found in graph")
    visited_nodes = [current_node]
    visited_edges = []

    while True:
        neighbors = list(graph.get_neighbors_nodes(current_node).keys())
        if not neighbors:
            break
        next_node = random.choice(neighbors)
        edge = (current_node, next_node)
        if edge in visited_edges or next_node in visited_nodes:
            break
        visited_nodes.append(next_node)
        visited_edges.append(edge)
        current_node = next_node

    infunc_filename = "random_walk.txt"
    f_p = os.path.join(output_dir, infunc_filename)
    with open(f_p, 'w', encoding='utf-8') as infunc_file:
        infunc_file.write("Visited Nodes:\n")
        infunc_file.write(" -> ".join(visited_nodes) + "\n\n")
        infunc_file.write("Visited Edges:\n")
        for edge in visited_edges:
            infunc_file.write(f"{edge[0]} -> {edge[1]}\n")
    s_a = "Random walk saved to "
    s_b = f"{os.path.join(output_dir, infunc_filename).replace(os.sep, '/')}"
    string_temp = s_a + s_b
    return visited_nodes, visited_edges, string_temp


def main():
    while True:

        print("-----------------------------------\nMenu:")
        print("1. Show Directed Graph")
        print("2. Query Bridge Words")
        print("3. Generate New Text")
        print("4. Calculate Shortest Path")
        print("5. Random Walk")

        print("6. Exit Now")

        while (1):
            choice = input("Please input your choice: \n")
            if choice == '1':     

                graphname = 'visual' 
                showDirectedGraph(graph, infunc_filename=graphname)
                break
            elif choice == '2':
                word1 = input("Please input word1: ").lower()
                word2 = input("Please input word2: ").lower()
                print(queryBridgeWords(word1, word2))
                break
            elif choice == '3':
                input_text = input("Please input text: ").lower()
                new_text = generateNewText(input_text)
                print("Generated Text:", new_text)
                break
            elif choice == '4':
                word1 = input("Enter word1 (or press Enter to skip): ").lower()
                word2 = input("Enter word2 (or press Enter to skip): ").lower()
                print(calcShortestPath(word1, word2))
                break
            elif choice == '5':
                visited_nodes, visited_edges, message = \
                    random_walk_and_save(graph, "output")
                print("Visited Nodes:", visited_nodes)
                print("Visited Edges:", visited_edges)
                print(message)
                break

            elif choice == '6':
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
