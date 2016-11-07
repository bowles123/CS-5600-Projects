def fourty(time):
    if time == 0:
        return time
    return (time / 4.24) * 100

def bench(reps):
    return reps * 3

def vertical(inches):
    return inches * 2.2

def broad(inches):
    return inches / 1.5

def cone(time):
    if time == 6.4:
        return 100
    return (time / 6.4) * 100

def twentyShuttle(time):
    if time == 3.81:
        return 100
    return (time / 3.81) * 100

def sixtyShuttle(time):
    if time == 10.72:
        return 100
    return (time / 10.72) * 100

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

def calcQBStatsScore(rating, pys, ptds, interceptions, attempts):
    ratingScore = rating - 55
    pysScore = pys / 38
    ptdsScore = ptds * 2.75
    intScore = abs((interceptions / attempts) * 100 - 100)
    return (ratingScore + pysScore + ptdsScore + intScore) / 4

def calcRBStatsScore(avgy, yards, carries, tds):
    avgyScore = avgy * 15
    yardsScore = yards / 14
    carriesScore = carries / 2.5
    tdsScore = tds * 6
    return (avgyScore + yardsScore + carriesScore + tdsScore) / 4

def calcWRStatsScore(avgy, yards, receptions, tds):
    avgyScore = avgy * 6
    yardsScore = yards / 12
    receptionsScore = receptions + 25
    tdsScore = tds * 7
    return (avgyScore + yardsScore + receptionsScore + tdsScore) / 4

def calcTEStatsScore(avgy, yards, receptions, tds):
    avgyScore = avgy * 6
    yardsScore = yards / 7.5
    receptionsScore = receptions * 2.5
    tdsScore = tds * 14
    return (avgyScore + yardsScore + receptionsScore + tdsScore) / 4

def calcDLStatsScore(sacks, tackles, position = "DT"):
    if position == "DE":
        sacksScore = sacks * 8
    else:
        sacksScore = sacks * 10

    tacklesScore = tackles * 2
    return (sacksScore + tacklesScore) / 2

def calcDBStatsScore(interceptions, tackles):
    interceptionsScore = interceptions * 20
    tacklesScore = tackles * 2.5
    return (interceptionsScore + tacklesScore) / 2

def calcLBStatsScore(tackles, sacks, position = "LB"):
    if position == "OLB":
        sacksScore = sacks * 8
        tacklesScore = tackles * 2
    else:
        sacksScore = sacks * 12      
        tacklesScore = tackles / 1.25
        
    return (tacklesScore + sacksScore) / 2
