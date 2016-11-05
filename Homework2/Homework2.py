import math

class Node:

    def __init__(self, children, attribute):
        self.children = children
        self.attribute = attribute

def entropy(num, possible):
    opposite = possible - num
    left = -((num/possible) * math.log((num/possible), 2))
    right = -(opposite/possible) * math.log((opposite/possible), 2)
    return left + right

def getTrainingSet(file, attributeString):
    trainingSet = {}
    att = []
    inputfile = open(file)
    
    for line in inputfile:
        io = line.split(',')
        attributes = line[0].split()

        for attribute in attributes:
            attribute = attributeString.index(attribute)
            att.add(attribute)
        trainingSet[att] = line[1]
        
    inputfile.close()           
    return trainingSet

def buildTree(trainingSet, numValues):
    numAttributes = len((trainingSet.keys())[0])
    
    if all(value == -1 for value in trainingSet.values()):
        return Node([], -3)
    elif all(value == 1 for value in trainingSet.values()):
        return Node([], -2)
    else:
        bestIG = -1
        for att in range(0, numAttributes):
            partition = {}
            sumEntropy = 0
            for instance in trainingSet:
                attValue = instance.getKey()[att]
                partition[attValue] = instance              
                sumEntropy = sumEntropy + entropy(att.values(), numValues[att])
            averageEntropy = sumEntropy / numValues[att]
            informationGain = entropy(att.values(), numValues) - averageEntropy

            if informationGain > bestIG:
                attribute = att
        subPartition = {}
        for instance in attribute:
            attValue = instance.getKey()[attribute]
            subPartition[attValue] = instance
        childen=[]
        for attVal in attribute.values():
            children.append(buildTree(subPartition,len(attribute.values())))
        newNode = Node(children, attVal)
        return newNode  

def evaluateTree(Set, numValues):
    trainingSet = dict(Set.items()[len(Set) * 0.8])
    testSet = dict(Set.items()[len(Set) * 0.2])
    tree = buildTree(trainingSet)

    for each instance int testSet:
        output = tree[instance]
        
        
