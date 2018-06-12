import json
from pprint import pprint

nodes = dict()

def depth(data):
        
    if 'children' in data:
        #return 1 + max([0] + list(map(depth, data['children'])))
        return 1 + max([-1] + list(map(depth, data['children'])))
    else:
        return 1

def nodeDepths(data, currDepth):

    for val in data:
        currVal = data[val]
        if val == "value":
            nodes[currVal] = currDepth
        elif val == "children":
            if currVal == []:
                pass;
            for child in currVal:
                nodeDepths(child, currDepth - 1)

def getAllChildren(data, node, allChildren):

    nodeDepths(data, depth(data))
    maxLevel = nodes[node]

    for val in data:
        currVal, kids = data["value"], data["children"]
        currLevel = nodes[currVal]

        #still too high in the tree
        if currLevel > maxLevel or (currLevel == maxLevel and currVal == node):
            for kid in kids:
                getAllChildren(kid, node, allChildren)

        #if the current node is one of the desired nodes children      
        elif currLevel < maxLevel:
            if currVal not in allChildren:
                allChildren.append(currVal)
            if kids != []:
                for kid in kids:
                    getAllChildren(kid, node, allChildren)

def generalize(data, node1, node2):

    return True
    

with open("language.json") as f:
    data = json.load(f)

allChildren = []
getAllChildren(data, "europe", allChildren)
print(allChildren)

