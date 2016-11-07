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
        print("%d. %s %s [%s]" % (self.pickNum, self.city, self.name, self.printNeeds()))

    def printNeeds(self):
        needsString = ""
        i = 0
        
        for need in self.needs:
            i = i + 1

            if (i == len(needs)):
                needsString = needsString + need
            else:
                needsString = needsString + (need + ", ")

## From NFL.com, returns list of prospect objects.
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

## Probably from API, returns list of stats.
## The index of the stats list corresponds to the index of the prospects list.
def getStatistics():
    stats = []

## From NFL.com, returns list of combine results for each prospect.
## The index of the results list corresponds to the index of the prospects list.
def getCombineResults():
    prospects = getProspects()
    ##wd.get("http://www.nfl.com/combine/participants")
	
    ##for prospect in prospects:
	##wd.find_element_by_id("alpha-" + prospect.lastName).click()
	## Use either selenium to click on the correct name link.
	## Use beautifulsoup to parse the information on the participants profile page.
    
def getProspectResults(first, last, Id):
    http = httplib2.Http()
    status, response = http.request('http://www.nfl.com/combine/profiles/' + first + '-' + last + '?id=' + Id)
    soup = BeautifulSoup(response, 'html.parser')
    results = []   
    results.append(soup.find('span', attrs={'class':'Grade'}).em.text)

    for li in soup.find_all('ul'):
        print(li)

    
    for h5 in soup.find_all('h5'):
        if (h5.text == "Grade"):
            continue
        else:
            results.append(h5.text)
    return results

## From NFL.com, returnss list of teams' needs.
## The index of the needs list corresponds to the index of the teams list

## From NFL.com, returns list of teams sorted by pick number, descending.
def getDraftOrder():
    http = httplib2.Http()
    status, response = http.request('http://www.nfl.com/news/story/0ap3000000551301/article/2016-nfl-draft-order-and-needs-for-every-team')
    soup = BeautifulSoup(response, 'html.parser')
    teams = []
    needs = [[]]

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

def scoreProspect(statsScore, combineScore):
    score = ((statsScore * 3) + (combineScore * 2)) / 7

def predictDraft():
    predictor
