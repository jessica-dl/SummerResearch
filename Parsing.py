import json
from pprint import pprint

nodes = dict()

def depth(data):
        
    if 'children' in data:
        #https://stackoverflow.com/questions/29005959/depth-of-a-json-tree
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

def getParent(data, node):

    nodeDepths(data, depth(data))
    nodeLevel = nodes[node]
    
    for val in nodes:
        if nodes[val] == (nodeLevel + 1):
            allChildren = []
            getAllChildren(data, val, allChildren)
            if node in allChildren:
                return val
        else: pass;
    return node  

with open("sample.json") as f:
    data = json.load(f)

print(getParent(data, "*"))

##allChildren = []
##getAllChildren(data, "europe", allChildren)
##print(allChildren)

