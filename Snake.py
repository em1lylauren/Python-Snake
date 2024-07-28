import json as json
import sys as sys
import time as t
import pygame as py

from Globals import *  # Import variables from other file

clock = py.time.Clock()
gameStart = False  # Determines whether we are in the main game loop or not

# Initialization
py.init()
screen = py.display.set_mode((WINDOWXSIZE, WINDOWYSIZE))
py.display.set_caption("Snake")

icon = py.image.load("sprites/icon.png")  # Window icon
fruitSpriteSheet = py.image.load("sprites/foods.png")  # Spritesheet for fruits
py.display.set_icon(icon)

# Initialize sound mixer
py.mixer.init()

# Sounds and music
buttonHoverSound = py.mixer.Sound("sounds/buttonhover.wav")
startGameSound = py.mixer.Sound("sounds/startgame.ogg")
gameOverSound = py.mixer.Sound("sounds/gameover.wav")
scoreCollectSound = py.mixer.Sound("sounds/coincollect.wav")
bgm = py.mixer.Sound("sounds/menumusic.mp3")

# Colours
black = py.Color(0, 0, 0)
white = py.Color(255, 255, 255)
green = py.Color(71, 204, 73)
blue = py.Color(41, 182, 246)
red = py.Color(211, 47, 47)
yellow = py.Color(255, 235, 59)
purple = py.Color(142, 36, 170)
orange = py.Color(247, 28, 0)

# Fonts
textFont = py.font.Font("fonts/PixelDigivolveFont.ttf", 20)
textFontLarge = py.font.Font("fonts/PixelDigivolveFont.ttf", 50)


class Fruit():  # Will flesh this out later
    def __init__(self, x, y, image):
        self.x = x  # x location on screen
        self.y = y  # y location on screen
        self.image = image  # image of the fruit


# A class for the menu buttons
class Button():
    # Initializes a new button object and adds it to the array of buttons
    def __init__(self, x, y, width, height, text='Button', onClickFunction=None):
        self.x = x  # X location on screen
        self.y = y  # Y location on screen
        self.width = width  # Button width
        self.height = height  # Button height
        self.onClickFunction = onClickFunction  # Function to call when button is clicked

        # Normal, hover, and pressed colours
        self.fillColors = {
            'normal': '#7bb9fc',
            'hover': '#9fccfc',
            'pressed': '#518ac6'
        }

        self.buttonSurface = py.Surface((self.width, self.height))
        self.buttonRect = py.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = textFont.render(text, True, white)

    # Updates the graphics of the button
    def updateButton(self):
        mousePosition = py.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors["normal"])
        if self.buttonRect.collidepoint(mousePosition):
            self.buttonSurface.fill(self.fillColors["hover"])

            if py.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors["pressed"])
                self.onClickFunction()

        self.buttonSurface.blit(self.buttonSurf, [self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
                                                  self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2])

        screen.blit(self.buttonSurface, self.buttonRect)


# Draws a single line of text at the given x and y coordinate on screen.
def drawText(text, size, colour, x, y):
    font = py.font.Font("fonts/PixelDigivolveFont.ttf", size)
    textSurface = font.render(text, True, colour)
    screen.blit(textSurface, (x, y))


# Shows the high score screen (debug, crashes)
def seeHighScores():
    global gameStart, backToStartMenu
    gameStart = False
    backToStartMenu = False

    screen.fill(black)

    # Imports highscores from file
    file = open("highscores.json", "r+")
    scores = json.load(file)
    file.close()

    # Back button
    backButton = Button(5, 5, 100, 50, "Back", backToMenu)
    buttons = [backButton]

    while not backToStartMenu:
        screen.fill(black)

        # Draw 10 high scores on screen
        yPos = 200
        for name in scores:
            drawText(name + " " + str(scores[name]), 30, white, 325, yPos)
            yPos += 40

        for menuEvent in py.event.get():
            if menuEvent.type == py.QUIT:
                quitGame()

        for button in buttons:
            button.updateButton()

        py.display.flip()
        clock.tick(snakeSpeed)


# Sends the player back to the main menu from the high score screen
def backToMenu():
    global backToStartMenu
    backToStartMenu = True
    screen.fill(black)


# Starts the main game loop and resets the game attributes
def startGame():
    global gameStart, snakeHead, snakeBody, snakeSpeed, snakeDirection, score, fruitLocation, fruitSpawn, needMusic
    gameStart = True
    screen.fill(black)

    # Re-initialize the game attributes
    snakeHead = [100, 100]
    snakeBody = [snakeHead,
                 [100, 90],
                 [100, 80],
                 [100, 70]]
    snakeDirection = "RIGHT"

    score = 0
    snakeSpeed = 15

    updateFruitLocation()

    # Play game start sound
    startGameSound.play()
    t.sleep(1.5)
    needMusic = True


# Quits the game
def quitGame():
    py.quit()
    sys.exit()


# Updates the rest of the snake position to follow the head
def updateSnakeBody():
    oldHead = [snakeHead[0], snakeHead[1]]
    i = len(snakeBody) - 1

    while i > 1:
        snakeBody[i] = snakeBody[i - 1]
        i -= 1

    snakeBody[1] = oldHead


# Draws the snake entity onto the screen
def drawSnake():
    # Draw snake
    for piece in snakeBody:
        py.draw.rect(screen, green, py.Rect(piece[0], piece[1], 10, 10))


# Draws the fruit entity onto the screen
def drawFruit():
    # Draw fruit
    fruit = py.Surface((27, 27))
    fruit.blit(fruitSpriteSheet, (0, 0), fruits[fruitType])
    screen.blit(fruit, fruitLocation)


# Updates the player's score display
def drawScore():
    drawText("Score: " + str(score), 20, white, 5, 5)


# Shows the player's final score and ends the game
def gameOver():
    global needMusic
    needMusic = False
    bgm.stop()  # Stop the background music
    gameOverSound.play()

    drawText("Game Over", 30, white, 300, 400)
    py.display.flip()
    t.sleep(3)

    screen.fill(black)
    drawText("Final score: " + str(score), 30, white, 300, 400)
    py.display.flip()
    t.sleep(3)

    # Go back to the main menu
    global gameStart
    gameStart = False


def startMenu():
    global snakeSpeed
    snakeSpeed = 60 # For smoother menu transitions

    startButton = Button(200, 350, 400, 100, "Start", startGame)
    highScoreButton = Button(200, 460, 400, 100, "High Scores", seeHighScores)
    quitButton = Button(200, 570, 400, 100, "Quit", quitGame)

    # Buttons for start menu
    buttons = [startButton, highScoreButton, quitButton]

    # Start menu loop
    while not gameStart:
        screen.fill(black)
        drawText("Snake", 50, green, 320, 250)

        for menuEvent in py.event.get():
            if menuEvent.type == py.QUIT:
                quitGame()

        for button in buttons:
            button.updateButton()

        py.display.flip()
        clock.tick(snakeSpeed)


# Checks for collision between the snake and fruit objects
def checkFruitCollision():
    global score, fruitSpawn

    # Check for collision between snake and fruit
    if (snakeHead[0] in range(fruitLocation[0], fruitLocation[0] + 27)
            and snakeHead[1] in range(fruitLocation[1], fruitLocation[1] + 27)):
        scoreCollectSound.play()  # Play sound
        score += 10
        snakeBody.append([snakeBody[-1][0], snakeBody[-1][1]])
        fruitSpawn = True


# Updates the new location of a fruit object
def updateFruitLocation():
    global fruitSpawn, fruitLocation, fruitType

    # Update fruit location (only one at a time)
    if fruitSpawn:
        fruitLocation = [rand.randint(1, WINDOWYSIZE) // 20 * 20, rand.randint(1, WINDOWYSIZE) // 20 * 20]
        fruitType = rand.choice(list(fruits))
        fruitSpawn = False


# Checks if either of the game over conditions have been reached
def checkGameOverConditions():
    # Checking if snake beyond bounds
    if snakeHead[0] < 0 or snakeHead[1] < 0:
        gameOver()
    elif snakeHead[0] > WINDOWXSIZE - 10 or snakeHead[1] > WINDOWYSIZE - 10:
        gameOver()

    # Checking if snake collides with itself
    for piece in snakeBody[1:]:
        if snakeHead[0] == piece[0] and snakeHead[1] == piece[1]:
            gameOver()


# Game loop
def Game():
    global snakeSpeed, snakeDirection, needMusic

    while True:
        if gameStart:
            snakeSpeed += 0.0001
            print(snakeSpeed)  # Debug

            # Music
            if needMusic:
                bgm.play(-1)
                needMusic = False

            # Controls
            for event in py.event.get():
                if event.type == py.QUIT:
                    quitGame()

                if event.type == py.KEYDOWN:
                    if event.key == py.K_UP or event.key == py.K_w:
                        if snakeDirection != "DOWN":  # Can't move up if moving down
                            snakeDirection = "UP"
                    if event.key == py.K_DOWN or event.key == py.K_s:
                        if snakeDirection != "UP":  # Can't move down if moving up
                            snakeDirection = "DOWN"
                    if event.key == py.K_LEFT or event.key == py.K_a:
                        if snakeDirection != "RIGHT":  # Can't move left if moving right
                            snakeDirection = "LEFT"
                    if event.key == py.K_RIGHT or event.key == py.K_d:
                        if snakeDirection != "LEFT":  # Can't move right if moving left
                            snakeDirection = "RIGHT"

            updateSnakeBody()

            match snakeDirection:
                case "UP":
                    snakeHead[1] -= 10
                case "DOWN":
                    snakeHead[1] += 10
                case "LEFT":
                    snakeHead[0] -= 10
                case "RIGHT":
                    snakeHead[0] += 10

            checkFruitCollision()
            updateFruitLocation()

            screen.fill(black)

            drawSnake()
            drawFruit()
            drawScore()

            checkGameOverConditions()

            # Redraw screen
            py.display.update()

            # Update clock
            clock.tick(snakeSpeed)

        else:
            startMenu()
