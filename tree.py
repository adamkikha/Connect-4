from graphviz import Digraph



class Tree:
    def __init__(self, states):
        self.graph = Digraph()
        self.png_name = 'states_tree'
        self.extension = 'png'
        self.create_tree(states)
        self.save_tree()

    def create_tree(self,states):
        states_len = len(states)
        # print(states_len)
        for i in range(states_len):
            
            for j in range(len(states[i][1])):
                # print(states[i][1][j])
                self.graph.edge(str(states[i][0]),str(states[i][1][j]))
            if i+1 < states_len:
                # print(i)
                self.graph.edge(str(states[i][0]),str(states[i+1][0]))

    def save_tree(self):
        self.graph.format = self.extension
        tree = self.graph.unflatten(stagger=3)
        tree.render(self.png_name)
