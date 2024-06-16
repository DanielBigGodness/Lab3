# test_calculator.py

import unittest
import re

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

    def get_neighbors_nodes(self, node):
        return self.edges.get(node, {})


def process_text(infunc_text):
    # 非字母或数字
    in_func_processed_text = re.sub(r'[\W_]+', ' ', infunc_text)
    
    in_func_processed_text = in_func_processed_text.lower()

    # 将换行和回车符替换为空格
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
        

with open("/Users/mac/Projects/gjh_SE_lab1/input/bridge_test.txt", 'r', encoding='utf-8') as file:
    text = file.read()
processed_text = process_text(text)
graph = create_graph(processed_text)

class Test_bridge(unittest.TestCase):

    def setUp(self):
        self.test_func = queryBridgeWords

    def test_1(self):
        result = "The bridge words from aa to dd are: bb, cc."
        self.assertEqual(self.test_func("aa", "dd"), result)

    def test_2(self):
        result = "The bridge words from bb to aa are: dd."
        self.assertEqual(self.test_func("bb", "aa"), result)

    def test_3(self):
        result = "Either ' ' or 'aa' contains a space or is empty."
        self.assertEqual(self.test_func(" ", "aa"), result)

    def test_4(self):
        result = "Either ' ' or 'Harry Potter' contains a space or is empty."
        self.assertEqual(self.test_func(" ", "Harry Potter"), result)
    
    def test_5(self):
        result = "No abc or no aa in the graph!"
        self.assertEqual(self.test_func("abc", "aa"), result)

    def test_6(self):
        result = "No abc or no bcd in the graph!"
        self.assertEqual(self.test_func("abc", "bcd"), result)

    def test_7(self):
        result = "No bridge words from aa to cc !"
        self.assertEqual(self.test_func("aa", "cc"), result)


if __name__ == '__main__':
    unittest.main()
