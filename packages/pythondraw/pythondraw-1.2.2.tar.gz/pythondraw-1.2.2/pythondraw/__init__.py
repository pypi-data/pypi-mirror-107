"""

Contect Us:xiaodong@indouyin.cn


copyright © xiaodong@indouyin.cn(小东互联网科技),2021.All Rights Reserved.
No secondary development or reprint is allowed without permission.

未经允许不得二次开发或转载

"""

import turtle

  
def screensize(a,b):
  turtle.screensize(a,b)

def startfill():
  turtle.begin_fill()

def endfill():
  turtle.end_fill()

def up(a):
  turtle.forward(a)

def down(a):
  turtle.left(180)
  turtle.forward(a)

def left(a):
  turtle.left(90)
  turtle.forward(a)

def right(a):
  turtle.right(90)
  turtle.forward(a)

def turn_left(a):
  turtle.left(a)

def turn_right(a):
  turtle.right(a)

def startdraw():
  turtle.screensize(500,500)

def penup():
  turtle.penup()

def pendown():
  turtle.pendown()

def tp(x,y):
  turtle.goto(x,y)

def tpx(x):
  turtle.setx(x)

def tpy(y):
  turtle.sety(y)

def getposition():
  position = turtle.pos()
  return position

def printposition():
  print(turtle.pos())

def shape(shape):
  turtle.shape(shape)

def hidepen():
  turtle.hideturtle()

def copyright():
  print("copyright © xiaodong@indouyin.cn(小东互联网科技),2021.All Rights Reserved.")
  print("No secondary development or reprint is allowed without permission.")
  print("未经允许不得二次开发或转载.")

def info():
  print("Name: pythondraw")
  print("Version: 1.2.2")
  print("Summary: A drawing module more suitable for novices")
  print("Home-page: https://xiaodong.indouyin.cn/python/modules/pythondraw/index.html")
  print("Author: DY_XiaoDong")
  print("Author-email: xiaodong@indouyin.cn")
