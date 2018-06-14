import json
from pprint import pprint
import itertools

nDepths = dict() #figure out a way to get rid of global variables

#take everything out of a tuple
#change to distance between parent and lowest node in the tree

def depth(data):
    #function found here: https://stackoverflow.com/questions/29005959/depth-of-a-json-tree
        
    if 'children' in data:
        return 1 + max([-1] + list(map(depth, data['children'])))
    else:
        return 1


def nodeDepths(data, currDepth):

    for val in data:
        
        currVal = data[val]
        if val == "value":
            nDepths[currVal] = currDepth #appends the node and its depth to dictionary nDepths
            
        elif val == "children":
            if currVal != []:
                
                for child in currVal:
                    nodeDepths(child, currDepth - 1) #continues to go through the tree
                    
            else: pass;


def getAllChildren(data, node, allChildren):

    nodeDepths(data, depth(data))
    maxLevel = nDepths[node]

    for val in data:
        currVal, kids = data["value"], data["children"]
        currLevel = nDepths[currVal]

        #if still higher in the tree than the desired node or at the node 
        if currLevel > maxLevel or (currLevel == maxLevel and currVal == node):
            for kid in kids:
                getAllChildren(kid, node, allChildren) #go through current children to look for children of the node

        #if the current node is one of the desired nodes children      
        elif currLevel < maxLevel:
            if currVal not in allChildren:
                allChildren.append(currVal) #if the node hasn't been seen before, add it to the list of children
            if kids != []:
                for kid in kids:
                    getAllChildren(kid, node, allChildren) #if the current node has children, look through them
        else: pass;


def getParent(data, node):

    nodeDepths(data, depth(data))
    nodeLevel = nDepths[node]
    
    for val in nDepths:
        
        if nDepths[val] == (nodeLevel + 1): #look at nodes one level higher than the specified node
            allChildren = []
            getAllChildren(data, val, allChildren) #if the higher node contains the specified node in its children
                                                   #then it's the specified node's parent
            if node in allChildren:
                return val
        else: pass;
        
    return node  


def generalize(data, node1, node2):

    if node1 == node2: #if the two nodes are the same, there is no need to generalize
        return node1
    
    else:

        nodeDepths(data, depth(data))
        if nDepths[node1] >= nDepths[node2]: #we want to look at the nodes in terms of where they are in the tree
            higher, lower = node1, node #higher means closer to the root
        else: 
            higher, lower = node2, node1
        
        allChildren, currNode = [], lower
        while (higher not in allChildren) and (higher != currNode): #if the higher node is in the children, then
                                                                    #the generalized value has been found
            #find the parent value of the current node and find the children of parent                                          
            parent = getParent(data, currNode)
            pChildren = getAllChildren(data, parent, allChildren) 

            """we know that if the higher node is not in the current nodes children, then we have to go up a
               level and see if that generalizes node1 and node2"""
            if higher not in allChildren:
                currNode = parent
        
    return parent


def combinations(data):
    """function found here:
    https://stackoverflow.com/questions/45964423/generate-all-possible-combinations-of-elements-in-a-list """

    nodeDepths(data, depth(data))
    combs = []
    
    for comb in (itertools.product(nDepths, nDepths)): #use itertools to generate the combinations of nodes
        if (comb[0], comb[1]) and (comb[1], comb[0]) not in combs: #this ensures that there are no repeated combinations
            combs.append(comb)
        
    return combs
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
    
    with open(file) as f:
        data = json.load(f)

    calcs, treeDepth = [], depth(data)
    nodeDepths(data, treeDepth)
    
    for node1, node2 in combinations(data):
        genVal = generalize(data, node1, node2) #find the generalization for each combination of nodes
        #nodeDist = nodeDistance(data, node1, node2, genVal)
        calcs.append((node1, node2, genVal, nDepths[genVal], treeDepth, treeDepth))

    return calcs


def main():

    outfile = open("output.txt", "w")

    for node1, node2, gen, dist, parentDepth, depth in calculations("postal_codes.json"):
        
        sepBy = "," #if its decided to separate the values by something else, this makes it easy to change
        out = str(node1)+sepBy+str(node2)+sepBy+str(gen)+sepBy+str(dist)+sepBy+str(parentDepth)+sepBy+str(depth)+"\n"
        outfile.write(out) #append all the values to the file
        
    outfile.close()

if __name__ == "__main__":
    main()


