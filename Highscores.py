from Globals import *


# Adds a new score to the list (max of 10 can be in the list, smallest is replaced)
def addScore(newScore):
    if newScore['score'] > scores[-1]['score']:
        scores[-1] = newScore
        sortScores()


# Sorts the list of scores based on value
def sortScores():
    global scores
    scores = sorted(scores, key=lambda d: d['score'], reverse=True)


# Creates and returns an object formatted to correctly fit into the highscores file
def createScoreDictObject(name, score):
    return {'name': name, 'score': score}


# Writes the new list of scores to the highscores.json file
def writeToScoresFile():
    global scores

    with open('highscores.json', 'w') as scoresFile:
        json.dump(scores, scoresFile)
        scoresFile.close()


# Checks if the current player score is high enough to place in the top 10 high scores.
def checkIfScoreIsOnLeaderboard(score):
    if score > scores[-1]['score']:
        return True
    else:
        return False