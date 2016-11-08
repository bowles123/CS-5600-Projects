import re
import json
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

class Prospect:
    
    def __init__(self, firstName, lastName, position, score = 0):
        self.firstName = firstName
        self.lastName = lastName
        self.position = position
        self.score = score

    def printProspect(self):
        print("%s, %s - %s" % (self.lastName, self.firstName, self.position))

class Team:
    def __init__(self, city, name, pickNum, needs, pick = None):
        self.city = city
        self.name = name
        self.pickNum = pickNum
        self.needs = needs
        self.pick = pick

    def printTeam(self):
        print("%d. %s %s Needs: %s" % (self.pickNum, self.city, self.name, self.printNeeds()))

    def printNeeds(self):
        needsString = ""
        i = 0
        
        for need in self.needs:
            i = i + 1

            if (i == len(self.needs)):
                needsString = needsString + need
            else:
                needsString = needsString + (need + ", ")
        return needsString

## Returns list of prospect objects.
## List is sorted in terms of the prospects' scores, descending.
def getProspects():
    http = httplib2.Http()
    status, response = http.request('http://www.nfl.com/news/story/0ap3000000641197/article/daniel-jeremiahs-top-50-prospects-for-2016-nfl-draft')
    soup = BeautifulSoup(response, 'html.parser')
    prospects = []
    data = []

    for span in soup.find_all('span', attrs={'class':'team-name'}):
        data.append(span.text)

    for prospect in data:
        metadata = prospect.split(' - ')
        names = metadata[0].split(' ')
        prospects.append(Prospect(names[0], names[1], metadata[1].split(' ')[0]))
    return prospects

## The index of the stats list corresponds to the index of the prospects list.
def getStatistics():
    prospects = getProspects()
    stats = []

    ##for prospect in prospects:
        ##google search for: "(prospect name, (first, last)) college statistics"
        ##get url from first result in google search
        ##prospect.score = getProspectStatsScore(resultUrl)
        ##pause for 5 seconds before getting the next one

##Stats order
##QB: Cmp, Att, Pct, Yds, Y/A, AY/A, TD, Int, Rate
##WR:
def getProspectStatsScore(prospect):
    http = httplib2.Http()
    status, response = http.request('http://www.sports-reference.com/cfb/players/' + prospect.firstName + '-' + prospect.lastName + '-' + '1.html')
    soup = BeautifulSoup(response, 'html.parser')
    years = 0
    stats = []

    for tr in soup.find('tbody'):
        years = years + 1

## From NFL.com, returns list of combine results for each prospect.
## The index of the results list corresponds to the index of the prospects list.
def getCombineResults():
    prospects = getProspects()
	
    ##for prospect in prospects:
	##google search for: "(prospect name, (first, last)) combine results"
        ##get url from first result in google search
        ##prospect.score = getProspectCombineScore(resultUrl)
        ##pause for 5 seconds before getting the next one

## Returns the score for a player's combine
def getProspectCombineScore(url):
    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response, 'html.parser')
    grade = f = b = v = br = c = t = s = 0.0
    events = 0

    grade = soup.find('span', attrs={'class':'grade'})
    if grade != None:
        grade = float(grade.em.text)

    f = getEventResult('forty-yard-dash', url)
    
    if f != None:
        events = events + 1

    b = getEventResult('bench-press', url)

    if b != None:
        events = events + 1

    v = getEventResult('vertical-jump', url)

    if v != None:
        events = events + 1

    br = getEventResult('broad-jump', url)

    if br != None:
        events = events + 1

    c = getEventResult('three-cone-drill', url)

    if c != None:
        events = events + 1

    t = getEventResult('twenty-yard-shuttle', url)

    if t != None:
        events = events + 1

    s = getEventResult('sixty-yard-shuttle', url)

    if s != None:
        events = events + 1

    return calcCombineScore(grade, f, b, v, br, c, t, s, events)

## Grabs the result of a player's event
def getEventResult(eventName, url):
    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response, 'html.parser')

    result = soup.find('li', attrs={'class':eventName})
    if result != None:
        result = float(result.h5.text.split(' ')[0])
    else:
        result = soup.find('li', attrs={'class':eventName + ' top-performer'})
        if result != None:
            result = float(result.h5.text.split(' ')[0])
    return result

## Calculates a player's combine score based on each event and their grade
def calcCombineScore(grade, fourty_time, reps, verticalInches, broadInches,
                     cone_time, twenty_time, sixty_time, totalEvents):
    gradeScore = grade * 18
    fourtyScore = fourty(fourty_time)
    benchScore = bench(reps)
    verticalScore = vertical(verticalInches)
    broadScore = broad(broadInches)
    coneScore = cone(cone_time)
    twentyScore = twentyShuttle(twenty_time)
    sixtyScore = sixtyShuttle(sixty_time)
    return (fourtyScore + benchScore + verticalScore + broadScore + coneScore +
            twentyScore + sixtyScore +  gradeScore) / (totalEvents + 1.5)

# Normalizes forty-yard-dash time
def fourty(time):
    if time == None:
        return 0
    return (4.24 / time) * 100

# Normalizes number of bench-presses
def bench(reps):
    if reps == None:
        return 0
    return reps * 3

# Normalizes height for vertical-jump
def vertical(inches):
    if inches == None:
        return 0
    return inches * 2.2

# Normalizes height for broad-jump
def broad(inches):
    if inches == None:
        return 0
    return inches / 1.5

# Normalize three-cone-drill time
def cone(time):
    if time == None:
        return 0
    return (6.4 / time) * 100

# Normalizes twenty-yard-shuttle time
def twentyShuttle(time):
    if time == None:
        return 0
    return (3.81 / time) * 100

# Normalizes sixty-yard-shuttle time
def sixtyShuttle(time):
    if time == None:
        return 0
    return (10.72 / time) * 100

## Returns list of teams sorted by pick number, descending.
def getDraftOrder():
    http = httplib2.Http()
    status, response = http.request('http://www.nfl.com/news/story/0ap3000000551301/article/2016-nfl-draft-order-and-needs-for-every-team')
    soup = BeautifulSoup(response, 'html.parser')
    teams = []

    for b in soup.find_all('b'):
        if b.a != None:
            teams.append(b.a.text)

    status, response = http.request('http://www.nfl.com/news/story/0ap3000000572264/article/2016-nfl-draft-order-and-needs-nos-1120')
    soup = BeautifulSoup(response, 'html.parser')

    for b in soup.find_all('b'):
        if b.a != None:
            teams.append(b.a.text)

    status, response = http.request('http://www.nfl.com/news/story/0ap3000000572265/article/2016-nfl-draft-order-and-needs-playoff-teams')
    soup = BeautifulSoup(response, 'html.parser')

    for b in soup.find_all('b'):
        if b.a != None:
            teams.append(b.a.text)
    return teams

## Returns a list of Team objects with all their given information
def getTeams():
    http = httplib2.Http()
    status, response = http.request('http://www.nfl.com/news/story/0ap3000000551301/article/2016-nfl-draft-order-and-needs-for-every-team')
    soup = BeautifulSoup(response, 'html.parser')
    teams = getDraftOrder()
    fullTeam = []
    fullTeams = []
    needs = []
    shortNeeds = []
    i = 1

    for team in teams:
        topNeed = ''
        otherNeeds = ''
        
        if i == 11:
            status, response = http.request('http://www.nfl.com/news/story/0ap3000000572264/article/2016-nfl-draft-order-and-needs-nos-1120')
            soup = BeautifulSoup(response, 'html.parser')
        if i == 21:
            status, response = http.request('http://www.nfl.com/news/story/0ap3000000572265/article/2016-nfl-draft-order-and-needs-playoff-teams')
            soup = BeautifulSoup(response, 'html.parser')

        for p in soup.find_all('p'):
            if team in p.getText() and team == teams[i - 1]:
                for b in p:
                    if 'Top need:' in b:
                        topNeed = next(b.next_siblings)
                    elif 'Other needs:' in b:
                        otherNeeds = next(b.next_siblings)
                        
        needs.append(topNeed)
        needs.extend(otherNeeds.split(','))

        for need in needs:
            temp = need.upper().split(' ')
            temp = [space for space in temp if space != '']

            if len(temp) == 2:
                if 'BACK' in temp[1] and temp[1] != 'BACK':
                    need = temp[0][0] + temp[1][0] + 'B'
                else:
                    need = temp[0][0] + temp[1][0]

            if len(temp) == 1:
                if 'BACK' in temp[0]:
                    need = temp[0][0] + 'B'
                else:
                    need = temp[0][0]

            if need == 'ER':
                need = 'DE'
            if need == 'PR':
                need = 'DL'

            shortNeeds.append(need)
        
        fullTeam = team.split(' ')
        fullTeams.append(Team(fullTeam[0], fullTeam[1], i, shortNeeds))
        shortNeeds = []
        needs = []
        i = i + 1

    return fullTeams

## Scores the prospect based on stats and combine results
## Stats account for 60% of the score while the combine accounts for 40%
def scoreProspect(statsScore, combineScore):
    score = ((statsScore * 3) + (combineScore * 2)) / 7
