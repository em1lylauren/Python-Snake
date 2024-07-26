import random as rand

# Window size
WINDOWXSIZE = 800
WINDOWYSIZE = 800

# Bgm music boolean
needMusic = True

# Initial snake attributes
snakeHead = [100, 100]
snakeBody = [snakeHead,
             [100, 90],
             [100, 80],
             [100, 70]]
snakeDirection = "RIGHT"
snakeSpeed = 15

# Score
score = 0

# Initial fruit attributes
fruitLocation = [rand.randint(10, WINDOWYSIZE) // 10 * 10, rand.randint(10, WINDOWYSIZE) // 10 * 10]
fruits = {
    'banana': (0, 2, 27, 27),
    'orange': (38, 5, 27, 27),
    'apple': (68, 4, 27, 27),
    'watermelon': (99, 10, 27, 27),
    'pineapple': (130, 3, 27, 27),
    'cherry': (5, 38, 27, 27)
}
fruitSpawn = False

# Buttons for start menu
buttons = []
