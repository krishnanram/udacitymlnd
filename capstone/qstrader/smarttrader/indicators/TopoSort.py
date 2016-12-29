from agents.AgentFactory import AgentFactory
from common.PropertyReader import *
from dateutil import parser
import json
# Simple:
# a --> b
#   --> c --> d
#   --> d

graph = {
    "a": ["b"],
    "b": ["c"],
    "c": ["d"],
    "d": []
}

graph1 = {
    "a": ["b", "c", "d"],
    "b": [],
    "c": ["d"],
    "d": []
}

# 2 components
graph2 = {
    "a": ["b", "c", "d"],
    "b": [],
    "c": ["d"],
    "d": [],
    "e": ["g", "f", "q"],
    "g": [],
    "f": [],
    "q": []
}

# cycle
graph3 = {
    "a": ["b", "c", "d"],
    "b": [],
    "c": ["d", "e"],
    "d": [],
    "e": ["g", "f", "q"],
    "g": ["c"],
    "f": [],
    "q": []
}

from collections import deque

GRAY, BLACK = 0, 1

def topological(graph):
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = GRAY
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == GRAY: raise ValueError("cycle")
            if sk == BLACK: continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = BLACK

    while enter: dfs(enter.pop())
    return order

# check how it works
#print topological(graph)
#print topological(graph2)
#try: topological(graph3)
#except ValueError: print "Cycle!"

if __name__ == '__main__':

    print topological(graph)

    print getAppDir()
    print getConfigDir()

    indicatorPath = getPath('strategies.data.path')
    print indicatorPath

    config = settings.from_file(getqQstraderConfig())
    strategiesDict = dict()
    instancesDict = dict()


    graph = dict()
    indicators = json.load(open(indicatorPath+"indicators.dict"))
    for indicator, value in indicators.iteritems():
        print indicator, value
        dependencies = value['dependencies']
        graph[indicator] = dependencies


    print graph
    order = topological(graph)
    while True:
        try:
            print order.pop()
        except IndexError:
            break