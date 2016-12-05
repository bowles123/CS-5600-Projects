import pybrain

positionMap = {
    'QB': '1000000000', 'RB': '0100000000', 'WR': '0010000000', 'TE': '0001000000',
    'OT': '0000100000', 'OG': '0000100000', 'DL': '0000010000', 'LB': '0000001000',
    'DB': '0000000100', 'P': '0000000010', 'K': '0000000001', 'OL': '0000100000',
    'DE': '0000010000', 'DT': '0000010000', 'CB': '0000000100', 'S': '0000000100',
    'ILB': '0000001000', 'OLB': '0000001000', 'MLB': '0000001000', 'FS': '0000000100',
    'C': '0000100000', 'SS': '0000000100', 'G': '0000100000', 'T': '0000100000',
    'NT': '0000010000', 'RT': '0000100000', 'LT': '0000100000', 'RG': '0000100000',
    'LG': '0000100000'}

orderMap = {
    '1': '11111111111111111111111111111111', '2': '11111111111111111111111111111110',
    '3': '11111111111111111111111111111101', '4': '11111111111111111111111111111011',
    '5': '11111111111111111111111111110111', '6': '11111111111111111111111111101111',
    '7': '11111111111111111111111111011111', '8': '11111111111111111111111110111111',
    '8': '11111111111111111111111101111111', '10': '11111111111111111111111011111111',
    '11': '11111111111111111111110111111111', '12': '11111111111111111111101111111111',
    '13': '11111111111111111111011111111111', '14': '11111111111111111110111111111111',
    '15': '11111111111111111101111111111111', '16': '11111111111111111011111111111111',
    '17': '11111111111111110111111111111111', '18': '11111111111111101111111111111111',
    '19': '11111111111111011111111111111111', '20': '11111111111110111111111111111111',
    '21': '11111111111101111111111111111111', '22': '11111111111011111111111111111111',
    '23': '11111111110111111111111111111111', '24': '11111111101111111111111111111111',
    '25': '11111111011111111111111111111111', '26': '11111110111111111111111111111111',
    '27': '11111101111111111111111111111111', '28': '11111011111111111111111111111111',
    '29': '11110111111111111111111111111111', '30': '11101111111111111111111111111111',
    '31': '11011111111111111111111111111111', '32': '10111111111111111111111111111111'}

class Prospect:
    
    def __init__(self, name, position, stats, combine, score = 0.0):
        self.name = name
        self.position = position
        self.stats = stats
        self.combine = combine
        self.score = score

    def equals(self, prospect):
        if prospect == None:
            return False

        if prospect.name == self.name && prospect.position == self.position:
            return True
        return False

    def printProspect(self):
        print("%s - %s [%f]" % (self.name, self.position, self.score))

class Team:
    def __init__(self, name, pickNum, needs, pick = None):
        self.name = name
        self.pickNum = pickNum
        self.needs = needs
        self.pick = pick

    def printTeam(self):
        print("%d. %s, Needs: %s" % (self.pickNum, self.name, self.printNeeds()))

    def printNeeds(self):
        string = "["
        i = 0
        
        for need in self.needs:
            if i == len(self.needs) - 1:
                string = string + (need + "]")
            else:
                string = string + (need + ", ")
            i = i + 1
        return string

class LearningPredictor:
    def __init__(testSet, trainSet):
        self.testSet = []
        self.trainingSet = []
        self.getData(testSet, trainSet)

    def getData(testFile, trainingTestFile):
        self.testSet = getTestSet(testFile , "2016")
        self.trainingSet = getTrainingSet(["2015", "2014", "2013"])

    def train():
        

    def predict():
        

def getTrainingSet(years):
    train = []
    
    for year in years:
        train.append(getDataSet("trainingSet" + year + ".txt", year))
    return train
    
def getDataSet(fileName, year):
    data = []
    fullTeams = []
    fullProspects = []

    with open(fileName) as inFile:
        data = inFile.readlines()
    data.remove(data[0])

    string = ''.join(data)
    data = string.split('\n\nTeams (' + year + '):\n\t')
    teams = data[1].split('\n\t')
    prospects = data[0].split('\n\t')
    prospects[0] = prospects[0][1:]

    for team in teams:
        teamData = team.split('. ')
        teamData[2] = teamData[2][1:-1]
        teamData[2] = teamData[2].split(', ')
        i = 0
        
        for need in teamData[2]:
            teamData[2][i] = positionMap.get(need)
            i = i + 1
        
        fullTeams.append(Team(teamData[1], orderMap.get(teamData[0]), teamData[2]))

    for prospect in prospects:
        prospectData = prospect.split('. ')
        prospectData[3] = prospectData[3][1:-1]
        prospectData[4] = prospectData[4][1:-1]
        fullProspects.append(Prospect(prospectData[1],
                                      positionMap.get(prospectData[2]),
                                      prospectData[3].split(', '),
                                      prospectData[4].split(', ')))

    return {year: (fullTeams, fullProspects)}
    
