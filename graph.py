import math   

class Graph:
    def __init__(self):
        self.size = 0
        self.vertList = {}

    def add_vertex(self, label):
        self.size += 1
        """Adds vertex to the graph, which is represented as a dictionary"""
        if type(label) != str:
            raise ValueError
        new_vertex = Vertex(label)
        self.vertList[label] = new_vertex
        return self

    def add_edge(self, src, dest, weight=0):
        """Creates node if does not exist and connects it to another
        node which will also be created if does not exist"""
        if type(src) is not str and type(dest) is not str:
            raise ValueError
        try:
            int(weight)
        except ValueError:
            raise ValueError
        if src not in self.vertList:
            self.add_vertex(src)
        if dest not in self.vertList:
            self.add_vertex(dest)
        self.vertList[src].nbr_list[self.get_vertex(dest)] = weight
        return self

    def get_vertex(self, label):
        """Returns the vertex object attached to parameter"""
        if label in self.vertList:
            return self.vertList[label]

    def get_weight(self, src, dest):
        """Returns weight between the two edges if path exists"""
        if src in self.vertList and dest in self.vertList:
            dest = self.get_vertex(dest)
            try:
                result = self.vertList[src].nbr_list[dest]
            except KeyError:
                return math.inf
            return result
        raise ValueError
    
    def __str__(self):
        strang = 'digraph G {\n'
        for item in self.vertList.values():
            for nbr in item.get_edges():
                weight = item.get_edges()[nbr]
                strang += f'   {item.label} -> {nbr.label}' \
                          f' [label="{weight:.1f}",weight="{weight:.1f}"];\n'
        strang += '}\n'
        return strang
    
    def shortest_travel_path(self, curVertex, curNum, cur_dist, large_path, home_vert):
        curVertex.color = "gray"


        if curNum == self.size - 1:
            large_path.append(cur_dist + curVertex.get_edges()[home_vert])
            curVertex.color = "white"
            return
        
        for node in curVertex.get_edges():
            if (node != home_vert) and node.color == 'white':
                distance = curVertex.get_edges()[node]
                self.shortest_travel_path(node, curNum + 1, cur_dist + distance, large_path, home_vert)
        
        curVertex.color = "white"
                    
    
class Vertex:
    def __init__(self, label, parent=None, color='white'):
        self.nbr_list = {}
        self.label = label
        self.parent = parent
        self.color = color

    def add_neighbor(self, dest, weight):
        self.nbr_list[dest] = weight

    def reset(self):
        self.parent = None
        self.color = 'white'

    def get_edges(self):
        return self.nbr_list

    def __str__(self):
        return self.label

    def __lt__(self, other):
        return self.distance < other.distance

    def __gt__(self, other):
        return self.distance > other.distance
    
    def print_vertex_data(self):
        return f'{self.label} is connected to {[item.label for item in self.nbr_list]}'