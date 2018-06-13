import json
from pprint import pprint
import itertools

nDepths = dict()

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
            nDepths[currVal] = currDepth
        elif val == "children":
            if currVal == []:
                pass;
            for child in currVal:
                nodeDepths(child, currDepth - 1)

def getAllChildren(data, node, allChildren):

    nodeDepths(data, depth(data))
    maxLevel = nDepths[node]

    for val in data:
        currVal, kids = data["value"], data["children"]
        currLevel = nDepths[currVal]

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
    nodeLevel = nDepths[node]
    
    for val in nDepths:
        if nDepths[val] == (nodeLevel + 1):
            allChildren = []
            getAllChildren(data, val, allChildren)
            if node in allChildren:
                return val
        else: pass;
    return node  

def generalize(data, node1, node2):

    if node1 == node2:
        return node1
    else:

        nodeDepths(data, depth(data))
        if nDepths[node1] >= nDepths[node2]:
            higher, lower = node1, node2
        else:
            higher, lower = node2, node1
        
        allChildren, currNode = [], lower
        while (higher not in allChildren) and (higher != currNode):
            parent = getParent(data, currNode)
            pChildren = getAllChildren(data, parent, allChildren)
            if higher not in allChildren:
                currNode = parent
        
    return parent

#https://stackoverflow.com/questions/45964423/generate-all-possible-combinations-of-elements-in-a-list
def combinations(data):
    
    nodeDepths(data, depth(data))
    combs = []
    
    for comb in (itertools.product(nDepths, nDepths)):
        if (comb[0], comb[1]) and (comb[1], comb[0]) not in combs:
            combs.append(comb)
        
    return combs

def calculations(file):
    
    with open(file) as f:
        data = json.load(f)

    nodeDepths(data, depth(data))
    calcs = []
    
    for comb in combinations(data):
        genVal = generalize(data, comb[0], comb[1])
        calcs.append((comb, genVal, nDepths[genVal], depth(data), depth(data)))

    return calcs

def main():
    
    print("postal_codes.json")
    for row in calculations("postal_codes.json"):
        print(row)

if __name__ == "__main__":
    main()


