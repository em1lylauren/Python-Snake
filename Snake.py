import sys

import pygame as py
import time as t
import random as rand

# Window size
WINDOWXSIZE = 800
WINDOWYSIZE = 800

clock = py.time.Clock()

# Colours
black = py.Color(0, 0, 0)
green = py.Color(71, 204, 73)

# Initialization
py.init()
screen = py.display.set_mode((WINDOWXSIZE, WINDOWYSIZE))
py.display.set_caption("Snake")

icon = py.image.load("apple.png")
py.display.set_icon(icon)

# Initial snake position
snakeHead = [100, 100]
snakeBody = [snakeHead,
             [100, 90],
             [100, 80],
             [100, 70]]
snakeDirection = "RIGHT"
snakeSpeed = 15


# Updates the rest of the snake position
def updateSnakeBody():
    i = len(snakeBody)-1

    while i > 1:
        snakeBody[i] = snakeBody[i-1]
        i -= 1

    snakeBody[1] = oldHead


# Game loop
while True:

    # Controls
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

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

    # Update snake position
    oldHead = [snakeHead[0], snakeHead[1]]
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

    screen.fill(black)

    # Draw snake
    for piece in snakeBody:
        py.draw.rect(screen, green, py.Rect(piece[0], piece[1], 10, 10))

    # Redraw screen
    py.display.update()

    # Update clock
    clock.tick(snakeSpeed)

