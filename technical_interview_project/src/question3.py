#Question 3
#Given an undirected graph G, find the minimum spanning tree within G.
#  A minimum spanning tree connects all vertices in a graph with the
# smallest possible total weight of edges. Your function should take in and
# return an adjacency list structured like this:

#Vertices are represented as unique strings. The function definition should be question3(G)
class Graph:

    def __init__(self):
        self.nodes = set()
        self.edges = dict(list())
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):

        #print "Inside add_edge:",from_node, to_node, distance

        if from_node not in self.edges :
            ll = list()
            ll.append(to_node)
            self.edges[from_node] = ll
        else :
            l = self.edges[from_node]
            #print l
            l.append(to_node)

        self.distances[(from_node, to_node)] = distance


    def getEdges(self):
        data = []

        nodes = set(self.nodes)
        for from_node in nodes:
            for to_node in self.edges[from_node]:
                #print from_node, to_node, g.distances[(from_node, to_node)]
                weight =  self.distances[(from_node, to_node)]
                if (to_node, from_node, weight) not in data:
                    data.append((from_node, to_node, weight))



        #print data
        return data

    def sorted_by_weight(self, desc=False):
        return sorted(self.getEdges(), key=lambda x: x[2], reverse=desc)

    def spanning_tree(self, minimum=True):
        mst = Graph()
        parent = {}
        rank = {}

        def find_parent(vertex):
            while parent[vertex] != vertex:
                vertex = parent[vertex]

            return vertex

        def union(root1, root2):
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root2] = root1

                if rank[root2] == rank[root1]:
                    rank[root2] += 1

        for vertex in self.nodes :
            parent[vertex] = vertex
            rank[vertex] = 0

        for v1, v2, weight in self.sorted_by_weight(not minimum):
            parent1 = find_parent(v1)
            parent2 = find_parent(v2)

            if parent1 != parent2:

                if v1 not in mst.nodes :
                    mst.add_node(v1)

                mst.add_edge(v1, v2, weight)
                union(parent1, parent2)

            if len(self) == len(mst):
                break

        print mst
        return mst

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, node):
        return self.nodes[node]

    def __iter__(self):
        for edge in self.getEdges():
            yield edge

    def __str__(self):
        return "\n".join('from %s to %s: %d' % edge for edge in self.getEdges())

def printGraph(g) :
    nodes = set(g.nodes)
    for from_node in nodes:
        for to_node in g.edges[from_node]:
            print from_node, to_node, g.distances[(from_node, to_node)]


if __name__ == '__main__':

    gdict = {
        'A': [('B', 2), ('C', 1)],
        'B': [('A', 2), ('C', 5)],
        'C': [('B', 5)]
    }

    g = Graph()

    for vertex, edges in gdict.items():
        g.add_node(vertex)
        for edge in edges:
            #print vertex, edge[0], edge[1]
            g.add_edge(vertex, edge[0], edge[1])

    print "******* Given Graph ************"
    printGraph(g)

    mst = g.spanning_tree(False)
    print "******* Minimum Spanning Tree Graph ************"
    printGraph(mst)
