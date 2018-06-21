import json
from pprint import pprint
import itertools
import sys

def depth(data):
    #function found here: https://stackoverflow.com/questions/29005959/depth-of-a-json-tree
        
    if 'children' in data:
        return 1 + max([-1] + list(map(depth, data['children'])))
    else: return 1


def nodeDepths(data, currDepth, nDepths):

    for val in data:
        
        currVal = data[val]
        
        if val == "value":
            nDepths[currVal] = currDepth #appends the node and its depth to dictionary nDepths
            
        elif val == "children" and currVal != []:
            for child in currVal:
                nodeDepths(child, currDepth - 1, nDepths) #continues to go through the tree
                    
        else: pass;


def getAllChildren(data, node, allChildren, nDepths):

    maxLevel = nDepths[node]

    for val in data:
        currVal, kids = data["value"], data["children"]
        currLevel = nDepths[currVal]

        #if still higher in the tree than the desired node or at the node 
        if currLevel > maxLevel or (currLevel == maxLevel and currVal == node):
            for kid in kids:
                getAllChildren(kid, node, allChildren, nDepths) #go through current children to look for children of the node

        #if the current node is one of the desired nodes children      
        elif currLevel < maxLevel:
            if currVal not in allChildren:
                allChildren.append(currVal) #if the node hasn't been seen before, add it to the list of children
            if kids != []:
                for kid in kids:
                    getAllChildren(kid, node, allChildren, nDepths) #if the current node has children, look through them
        else: pass;


def getParent(data, node, nDepths):
 
    nodeLevel = nDepths[node]
    
    for val in nDepths:
        
        if nDepths[val] == (nodeLevel + 1): #look at nodes one level higher than the specified node
            allChildren = []
            getAllChildren(data, val, allChildren, nDepths) #if the higher node contains the specified node in its children
                                                             #then it's the specified node's parent
            if node in allChildren:
                return val
        else: pass;
        
    return node  


def generalize(data, node1, node2, nDepths):

    if node1 == node2: #if the two nodes are the same, there is no need to generalize
        return node1
    
    else:

        if nDepths[node1] >= nDepths[node2]: #we want to look at the nodes in terms of where they are in the tree
            higher, lower = node1, node2 #higher means closer to the root
        else: 
            higher, lower = node2, node1
        
        allChildren, currNode = [], lower
        while (higher not in allChildren) and (higher != currNode): #if the higher node is in the children, then
                                                                    #the generalized value has been found
            #find the parent value of the current node and find the children of parent                                          
            parent = getParent(data, currNode, nDepths)
            pChildren = getAllChildren(data, parent, allChildren, nDepths) 

            """we know that if the higher node is not in the current nodes children, then we have to go up a
               level and see if that generalizes node1 and node2"""
            if higher not in allChildren:
                currNode = parent
        
    return parent


def combinations(data, nDepths):
    """function found here:
    https://stackoverflow.com/questions/45964423/generate-all-possible-combinations-of-elements-in-a-list """

    yield from itertools.product(nDepths, nDepths) #use itertools to generate the combinations of nodes
    
##    for comb in (itertools.product(nDepths, nDepths)): #use itertools to generate the combinations of nodes
##        if (comb[0], comb[1]) and (comb[1], comb[0]) not in combs: #this ensures that there are no repeated combinations
##            combs.append(comb)
##        
##    return combs

#if we need to calculate distance for some reason
##def nodeDistance(data, node1, node2, gen):
##
##    nodeDepths(data, depth(data))
##    
##    node1D, node2D, parentD = nDepths[node1], nDepths[node2], nDepths[gen]
##
##    if node1D <= node2D:
##        dist = parentD - node1D
##    else:
##        dist = parentD - node2D
##
##    return dist

def calculations(file):

    nDepths = dict()
    
    with open(file)as f:
        data = json.load(f)

    calcs, treeDepth = [], depth(data)
    nodeDepths(data, treeDepth, nDepths)
    
    for node1, node2 in combinations(data, nDepths):
        genVal = generalize(data, node1, node2, nDepths) #find the generalization for each combination of nodes
        #nodeDist = nodeDistance(data, node1, node2, genVal)
        calcs.append((node1, node2, genVal, nDepths[genVal], treeDepth, treeDepth))

    return calcs

#run by command: generalizing.py output-file.txt data-file1.json data-file2.json
def main():

    outfile = open(sys.argv[1], "w")
    
    for i in range (2, len(sys.argv)):
        file = str(sys.argv[i])
        outfile.write(file + "\n")
 
        for node1, node2, gen, dist, parentDepth, depth in calculations(file):

            sepBy = "," #if it's decided to separate the values by something else, this makes it easy to change
            out = str(node1)+sepBy+str(node2)+sepBy+str(gen)+sepBy+str(dist)+sepBy+str(parentDepth)+sepBy+str(depth)+"\n"
            outfile.write(out) #append all the values to the file

        outfile.write("\n")
            
    outfile.close()

if __name__ == "__main__":
    main()
