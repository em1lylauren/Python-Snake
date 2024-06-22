import pygame as py
import time as t
import random as rand

# Window size
windowXSize = 600
windowYSize = 800

# Initialization
py.init()
screen = py.display.set_mode((windowXSize, windowYSize))
py.display.set_caption("Snake")

icon = py.image.load("apple.png")
py.display.set_icon(icon)


