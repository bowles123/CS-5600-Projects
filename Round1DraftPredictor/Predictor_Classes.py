##Predictor/
##Predictor/__init__.py
##Predictory/Predictory_Classes.py

##Open-refine
##Something similar to the traveling salesman problem, optimization.

class Team:
    def __int__(self, city, name, pickNum, needs, pick = None):
        self.city = city
        self.name = name
        self.pickNum = pickNum
        self.needs = needs
        self.pick = pick

class Prospect:
    def __int__(self, firstName, lastName, position, score = 0):
        self.firstName = firstName
        self.lastName = lastName
        self.position = position
        self.score = score

class Predictor:
    def __init(self, prospects, teams):
        self.prospects = prospect
        self.teams = teams

    def predict():
        best_prospect = prospect[0]
        
        for team in teams:
            for prospect in prospects:
                if prospect.score >= 75 and (prospect in team.needs):
                    team.pick = prospect
                    prospects.remove(prospect)
                    break
                elif prospect.score < 75 and team.pick == None:
                    team.pick = best_prospect
                    prospects.remove(best_prospect)
                    break
                elif prospect.score > best_prospect.score:
                    best_prospect = prospect
                    break

    def display_predictions():
        for team in teams:
            if team.pick == None:
                print("%s %s: None." % team.city, team.name)
            else:
                print("%s %s: %s %s, %s" % team.city, team.name,
                      team.pick.firstName, team.pick.lastName, team.pick.position)
