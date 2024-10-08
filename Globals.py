import json
import random as rand

# Window size
WINDOWXSIZE = 800
WINDOWYSIZE = 800

# Bgm music boolean
needMusic = True

# Sends the player back to the main menu (from the high score screen) if true
backToStartMenu = False

# Initial snake attributes
snakeHead = [100, 100]
snakeBody = [snakeHead,
             [100, 90],
             [100, 80],
             [100, 70]]
snakeDirection = "RIGHT"
snakeSpeed = 15
fps = 60 # For smooth menu transitions

# Current player score
score = 0

# Leaderboard scores
file = open("highscores.json", "r+")
scores = json.load(file)
file.close()

# Fruit attributes
fruits = {
    'banana': (0, 2, 27, 27),
    'orange': (38, 5, 27, 27),
    'apple': (68, 4, 27, 27),
    'watermelon': (99, 10, 27, 27),
    'pineapple': (130, 3, 27, 27),
    'cherry': (5, 38, 27, 27)
}
fruitSpawn = True
