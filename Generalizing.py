import json
from pprint import pprint
import itertools

nDepths = dict() #figure out a way to get rid of global variables

#take everything out of a tuple
#change to distance between parent and lowest node in the tree

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

def nodeDistance(data, node1, node2, gen):

    nodeDepths(data, depth(data))
    
    node1D, node2D, parentD = nDepths[node1], nDepths[node2], nDepths[gen]

    if node1D <= node2D:
        dist = parentD - node1D
    else:
        dist = parentD - node2D

    return dist

def calculations(file):
    
    with open(file) as f:
        data = json.load(f)

    calcs, treeDepth = [], depth(data)
    nodeDepths(data, treeDepth)
    
    for comb in combinations(data):
        genVal = generalize(data, comb[0], comb[1])
        nodeDist = nodeDistance(data, comb[0], comb[1], genVal)
        calcs.append((comb[0], comb[1], genVal, nodeDist, treeDepth, treeDepth))

    return calcs


def main():

    outfile = open("output.txt", "w")

    for node1, node2, gen, dist, parentDepth, depth in calculations("postal_codes.json"):
        
        sepBy = ","
        out = str(node1)+sepBy+str(node2)+sepBy+str(gen)+sepBy+str(dist)+sepBy+str(parentDepth)+sepBy+str(depth)+"\n"
        outfile.write(out)
        
    outfile.close()

if __name__ == "__main__":
    main()


