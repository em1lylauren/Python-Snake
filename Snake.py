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
             [snakeHead[0], snakeHead[1]-10],
             [snakeHead[0], snakeHead[1]-20],
             [snakeHead[0], snakeHead[1]-30]]
snakeDirection = "RIGHT"
snakeSpeed = 15

# Game loop

while True:

    # Controls
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                snakeDirection = "UP"
            if event.key == py.K_DOWN:
                snakeDirection = "DOWN"
            if event.key == py.K_LEFT:
                snakeDirection = "LEFT"
            if event.key == py.K_RIGHT:
                snakeDirection = "RIGHT"

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

