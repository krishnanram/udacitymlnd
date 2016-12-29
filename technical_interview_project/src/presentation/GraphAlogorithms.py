

class Graph:

  def __init__(self):
    self.nodes = set()
    self.edges = dict(list())
    self.distances = {}

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):

    print "Inside add_edge:",from_node, to_node, distance

    if from_node not in self.edges :
        ll = list()
        ll.append(to_node)
        self.edges[from_node] = ll
    else :
        l = self.edges[from_node]
        print l
        l.append(to_node)

    self.distances[(from_node, to_node)] = distance


##### Methods in main program

def toposort(graph, initial):

  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes:

    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited,path


def bfs(graph, initial):

  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes:

    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited,path


def dfs(graph, initial):

  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes:

    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited,path



def dijsktra(graph, initial):

  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes:

    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited,path


def findSpanningTree(graph, initial):
    print "adas"

if __name__ == '__main__':

    gdict = {
        'A': [('B', 2) , ('C',1)] ,
        'B': [('A', 2), ('C', 5)],
        'C': [('B', 5)]
    }

    g = Graph()

    for vertex,edges in gdict.items() :
        g.add_node(vertex)
        for edge in edges :
            print vertex, edge[0], edge[1]
            g.add_edge(vertex, edge[0], edge[1])

    #print ":"+str(dijsktra(g, 'A'))+":"
    print dijsktra(g, 'A')
    #b=({'A': 0, 'C': 7, 'B': 2}, {'C': 'B', 'B': 'A'})
    #assert(dijsktra(g, 'A') == b )