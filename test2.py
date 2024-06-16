import unittest
import os
from text2gragh_after_Flake8_and_Pylint_lsh import DirectedGraph, random_walk_and_save

class TestRandomWalkAndSave(unittest.TestCase):

    OUTPUT_DIR = "output"

    @classmethod
    def setUpClass(cls):
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)

    def test_path1(self):
        graph = DirectedGraph()
        graph.add_edge("A", "A")
        visited_nodes, visited_edges, string_temp = random_walk_and_save(graph, self.OUTPUT_DIR)
        
        self.assertEqual(visited_nodes, ["A"])
        self.assertEqual(visited_edges, [])
        self.assertEqual(string_temp, "Random walk saved to output/random_walk.txt")

    def test_path2(self):
        graph = DirectedGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "A")
        visited_nodes, visited_edges, string_temp = random_walk_and_save(graph, self.OUTPUT_DIR)
        
        self.assertIn(visited_nodes, [["A", "B"], ["B", "A"]])
        self.assertIn(visited_edges, [[("A", "B")], [("B", "A")]])
        self.assertEqual(string_temp, "Random walk saved to output/random_walk.txt")

    def test_path3(self):
        graph = DirectedGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        visited_nodes, visited_edges, string_temp = random_walk_and_save(graph, self.OUTPUT_DIR)
        
        self.assertEqual(visited_nodes, ["A", "B", "C"])
        self.assertEqual(visited_edges, [("A", "B"), ("B", "C")])
        self.assertEqual(string_temp, "Random walk saved to output/random_walk.txt")

    def test_path4(self):
        graph = DirectedGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")
        visited_nodes, visited_edges, string_temp = random_walk_and_save(graph, self.OUTPUT_DIR)
        
        self.assertIn("A", visited_nodes)
        self.assertGreaterEqual(len(visited_edges), 2)
        self.assertEqual(string_temp, "Random walk saved to output/random_walk.txt")

if __name__ == "__main__":
    unittest.main()
