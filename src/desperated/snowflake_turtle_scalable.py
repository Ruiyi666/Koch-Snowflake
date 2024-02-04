# This file is not important anymore. It is just a backup of the old version of 
# my snowflake. I have kept it here for reference. It use the turtle module, and
# I have replaced it with the canvas module. The canvas module is more flexible.
# Here the scalable means that the snowflake is can be scaled, if you scroll with
# the mouse wheel.

# Reference: 
#   - https://blog.csdn.net/boysoft2002/article/details/120790162
#   - https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan

import math

from tkinter import *
from tkinter.ttk import *
import turtle

class KochSnowflakeTurtle(Frame):
    
    def __init__(self, master = None, width = 500, height = 500):
        super().__init__(master)
        self.master = master
        self.canvas = Canvas(self, width = width, height = height, background="bisque")
        self.xsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,500,500))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.turtle = turtle.RawTurtle(self.canvas)

        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>",self.zoomer)
        

        self.drawing = False
    
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
        self.drawing = True
        # reset the turtle direction
        # self.turtle.setheading(0)
        if order <= 0:
            return 
        for i in range(3):
            self.draw_line(order - 1, size)
            self.turtle.right(120)
        self.drawing = False

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
    
    #move
    def move_start(self, event):
        print(event.x, event.y, self.turtle.xcor(), self.turtle.ycor(), self.canvas.bbox("all"))
        self.canvas.scan_mark(event.x, event.y)
        print(event.x, event.y, self.turtle.xcor(), self.turtle.ycor(), self.canvas.bbox("all"))
        
    def move_move(self, event):
        print(event.x, event.y, self.turtle.xcor(), self.turtle.ycor(), self.canvas.bbox("all"))
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        print(event.x, event.y, self.turtle.xcor(), self.turtle.ycor(), self.canvas.bbox("all"))

    #windows zoom
    def zoomer(self,event):
        if self.drawing:
            return
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self,event):
        if self.drawing:
            return    
        true_x = self.canvas.canvasx(event.x)
        true_y = self.canvas.canvasy(event.y)
        print(event.x, event.y, self.turtle.xcor(), self.turtle.ycor(), self.canvas.bbox("all"))
        self.canvas.scale("all", true_x, true_y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        print(event.x, event.y, self.turtle.xcor(), self.turtle.ycor(), self.canvas.bbox("all"))
        
    def zoomerM(self,event):
        if self.drawing:
            return
        true_x = self.canvas.canvasx(event.x)
        true_y = self.canvas.canvasy(event.y)
        self.canvas.scale("all", true_x, true_y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    
def main():
    # object of class Tk, responsible for creating
    # a tkinter toplevel window
    master = Tk()
    master.geometry("500x600")
    snowflake = KochSnowflakeTurtle(master, 500, 500)

    master.title("Koch Snowflake")

    input_order = Entry(master)
    button_draw = Button(master, text = "Draw", command = lambda: snowflake.draw_triangle(int(input_order.get()), 300))
    button_save = Button(master, text = "Save", command = lambda: snowflake.save())

    snowflake.pack(fill="both", expand=True)
    input_order.pack()
    button_draw.pack()
    button_save.pack()
    # Infinite loop breaks only by interrupt
    master.mainloop()

if __name__ == "__main__":    
    main()
    
