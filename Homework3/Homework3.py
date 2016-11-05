from __future__ import print_function
import random
import math

learnRate = 0.001

def trainPerceptron(inVals, alpha, epoch, out, printError = False):
    w0 = random.uniform(-0.2, 0.2)
    w1 = random.uniform(-0.2, 0.2)
    w2 = random.uniform(-0.2, 0.2)
    i = 0
    error = 1
    x0 = 1
    data = ""

    while error >= 0.0001 and i < epoch:
        error = 0

        for instance in inVals:
            x1 = instance[0][0]
            x2 = instance[0][1]
            activationInput = w0 + (x1 * w1) + (x2 * w2)
            actualOutput = (1 / (1 + math.exp(-activationInput)))
            
            error = error + pow(instance[1] - actualOutput, 2)          
            left = alpha * (instance[1] - actualOutput)
            right = actualOutput * (1 - actualOutput)
            w0 = w0 + (left * right)
            w1 = w1 + (left * right * x1)
            w2 = w2 + (left * right * x2)
                                
        error = error / (len(inVals))
        i = i + 1

        if printError:
            data = data + str(i) + ", " + str(error) + "\n"
            writeOutData(data, out)

    return [w0, w1, w2]

def activation(activationInput):
    output = (1 / (1 + math.exp(-activationInput)))

    if output < 0.5:
        return 0
    else:
        return 1

def writeOutData(string, fileName):
    file = open(fileName, 'w')
    file.write(string)
    file.close()
    
def readInData(file):
    trainingSet = []
    inputs = []
    inputfile = open(file)

    for line in inputfile:
        io = line.split('\t')
        inputs.append(float(io[0]))
        inputs.append(float(io[1]))
        output = float(io[2].split('\n')[0])
        trainingInstance = (inputs, output)
        trainingSet.append(trainingInstance)
        inputs = []

    inputfile.close()
    return trainingSet

def testPerceptron(Set, epoch):
    numErrors = 0
    trainingSet = Set[0:int(len(Set) * 0.8)]
    testSet = Set[int(len(Set) * 0.8):len(Set)]
    weights = []

    for i in range(0, 10):
        if i == 0:
            weights = trainPerceptron(trainingSet, learnRate, epoch, "DataOut.txt", True)
        else:
            weights = trainPerceptron(trainingSet, learnRate,  epoch, "")

        for instance in testSet:
            actualOutput = runInstanceThrough(instance, weights)
                
            if actualOutput != instance[1]:
                numErrors = numErrors + 1
                
        random.shuffle(Set)
        trainingSet = Set[0:int((len(Set) * 0.8))]
        testSet = Set[int(len(Set) * 0.8):len(Set)]
    return (numErrors / (10 * len(Set))) * 100

def runInstanceThrough(instance, weights):
    first = weights[0]
    second = instance[0][0] * weights[1]
    last = instance[0][1] * weights[2]
    activationInput = first + second + last
    return activation(activationInput)

def part1(file):
    epoch = 1000
    print("Format = (epoch, % accuracy)")

    error = testPerceptron(readInData(file), epoch)
    print("%d, %d%%" % (epoch, 100 - error))

def testLogicGate(inVals, weights):
    numErrors = 0
    
    for instance in inVals:
        actualOutput = runInstanceThrough(instance, weights)
            
        if actualOutput != instance[1]:
                numErrors = numErrors + 1
                
    return ((numErrors / len(inVals)) * 100)
    
def part2():
    NAND = [([0,0], 1), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
    AND = [([0,0], 0), ([0, 1], 0), ([1, 0], 0), ([1, 1], 1)]
    OR = [([0,0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 1)]
    NOR = [([0,0], 1), ([0, 1], 0), ([1, 0], 0), ([1, 1], 0)]
    XOR = [([0,0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
    print("Format = (epoch, % accuracy)")
    epoch = 20000

    NAND_weights = trainPerceptron(NAND, learnRate, epoch, "NAND.txt", True)
    AND_weights = trainPerceptron(AND, learnRate, epoch, "AND.txt", True)
    OR_weights = trainPerceptron(OR, learnRate, epoch, "OR.txt", True)
    NOR_weights = trainPerceptron(NOR, learnRate, epoch, "NOR.txt", True)
    XOR_weights = trainPerceptron(XOR, learnRate, epoch, "XOR.txt", True)

    print("NAND")
    print("%d, %d%%" % (epoch, testLogicGate(NAND, NAND_weights)))
    print("AND")
    print("%d, %d%%" % (epoch, testLogicGate(AND, AND_weights)))
    print("OR")
    print("%d, %d%%" % (epoch, testLogicGate(OR, OR_weights)))
    print("NOR")
    print("%d, %d%%" % (epoch, testLogicGate(NOR, NOR_weights)))
    print("XOR")
    print("%d, %d%%" % (epoch, testLogicGate(XOR, XOR_weights)))

def main(learningRate = 0.001):
    learnRate = learningRate
    print("Part1:")
    part1("Data.txt")
    print("Part2:")
    part2()
