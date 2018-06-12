import json
from pprint import pprint

nodes, children = dict(), []

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

##def getAllChildren(data, node):
##    print(data["children"][1]["value"])
##    #fix it so it only goes through children of data[node]
##    for val in data:
##        kids, currVal = data["children"], data[val]
##        if val != "children" and currVal != [] and currVal not in children:
##            children.append(currVal)
##        else:
##            for kid in kids:
##                getAllChildren(kid, kid["value"])            
##
##    return children


with open("sample.json") as f:
    data = json.load(f)

nodeDepths(data, depth(data))
print(nodes)
#print(getAllChildren(data, "partial1"))

