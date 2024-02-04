# This file is not important anymore. It is just a backup of the old version of 
# my snowflake. I have kept it here for reference. It use the turtle module, and
# I have replaced it with the canvas module. The canvas module is more flexible.
# Here the fixed means that the snowflake is not scalable. It is just a fixed.

# Reference: https://blog.csdn.net/boysoft2002/article/details/120790162

import math
from tkinter import *
from tkinter.ttk import *
import turtle

class KochSnowflakeTurtle:
    
    def __init__(self, master = None, width = 500, height = 500):
        self.master = master
        self.canvas = Canvas(self.master, width = width, height = height)
        self.canvas.pack()
        self.turtle = turtle.RawTurtle(self.canvas)
        

    def draw_triangle(self, order, size):
        """
        Start with an equilateral triangle. This is order 1.
        """
        self.turtle.clear()
        self.turtle.penup()
        self.turtle.home()
        self.turtle.goto(-size / 2, -math.sqrt(3) * size / 6)
        self.turtle.right(300)
        self.turtle.pendown()
        
        # reset the turtle direction
        # self.turtle.setheading(0)
        if order <= 0:
            return 
        for i in range(3):
            self.draw_line(order - 1, size)
            self.turtle.right(120)


    def draw_line(self, order, size):
        """
        Repeat n - 1 times: Replace the middle third of each side with two sides of an equilateral triangle.
        """
        if order == 0:
            self.turtle.forward(size)
        else:
            self.draw_line(order - 1, size / 3)
            self.turtle.left(60)
            self.draw_line(order - 1, size / 3)
            self.turtle.right(120)
            self.draw_line(order - 1, size / 3)
            self.turtle.left(60)
            self.draw_line(order - 1, size / 3)

    def save(self):
        self.canvas.postscript(file = "snowflake.eps")
        
def main():
    # object of class Tk, responsible for creating
    # a tkinter toplevel window
    master = Tk()
    master.geometry("500x600")
    snowflake = KochSnowflakeTurtle(master, 500, 500)
    snowflake.draw_triangle(3, 300)
    
    master.title("Koch Snowflake")

    input_order = Entry(master)
    button_draw = Button(master, text = "Draw", command = lambda: snowflake.draw_triangle(int(input_order.get()), 300))
    button_save = Button(master, text = "Save", command = lambda: snowflake.save())

    input_order.pack()
    button_draw.pack()
    button_save.pack()
    # Infinite loop breaks only by interrupt
    master.mainloop()

if __name__ == "__main__":    
    main()
    
