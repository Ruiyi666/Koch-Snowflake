#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: app.py
Author: Ruiyi Qian
Date: 2023/05/01
Description: Main application class for the Koch Snowflake fractal curve.
"""

import operator
import os
from tkinter import *
from tkinter.ttk import *

from .utils import *
from .snowflake import KochSnowflake



class SnowflakeApp():
    """Main application class for the Koch Snowflake fractal curve.
    This class is only responsible for setting up the GUI and the snowflake.
    Those algorithms are implemented in the snowflake.py module, or in the
    fractal_curve module.
    """
    def __init__(
            self,
            width: int = 500,
            height: int = 500,
        ) -> None:
        self.master = Tk()
        master = self.master
        master.geometry(f"{width}x{height}")
        master.title("Koch Snowflake")

        self.snowflake = KochSnowflake(
            master,
            center=(width / 2, height / 2),
            radius=min(width, height) / 3,
            rotation=0,
            order="inf",
            stroke=2,
            resolution=3
        )

        snowflake = self.snowflake
        snowflake.render_on_move = True
        snowflake.pack(side=TOP, fill=BOTH, expand=1)

        # Left side here
        self.controls = Frame(master)
        self.controls.pack(side=BOTTOM, fill=BOTH)
        controls = self.controls
        
        snowflake.canvas.update()
        snowflake.update()

        scoll_resolution = Scale(controls, from_=1, to=10, orient=HORIZONTAL)
        scoll_resolution.set(snowflake.get_resolution())
        
        input_order = Entry(controls, width=10)
        input_order.insert(0, snowflake.order)
        button_reset = Button(controls, text="Reset")
        button_plus = Button(controls, text = "+", width=4)
        button_minus = Button(controls, text = "-", width=4)
        checkbox_render_on_move = Checkbutton(controls, text="Online Render")

        scoll_resolution.bind(
            "<ButtonRelease-1>", lambda event: 
                snowflake.set_resolution(scoll_resolution.get()))
        
        button_reset.bind(
            "<Button-1>", lambda event: snowflake.reset(
                center=(master.winfo_width() / 2, master.winfo_height() / 2),
                radius=min(master.winfo_width(), master.winfo_height()) / 3))
        
        button_plus.bind(
            "<Button-1>", lambda event: (
                snowflake.reset(order=decrease_order(snowflake.order)),
                input_order.delete(0, END),
                input_order.insert(0, snowflake.order)))
        
        button_minus.bind(
            "<Button-1>", lambda event: (
                snowflake.reset(order=increase_order(snowflake.order)),
                input_order.delete(0, END),
                input_order.insert(0, snowflake.order)))
        
        input_order.bind(
            "<Return>", lambda event: (
                snowflake.reset(order=to_order(input_order.get())),
                input_order.delete(0, END),
                input_order.insert(0, snowflake.order))) 
        
        
        checkbox_render_on_move.bind(
            "<Button-1>", 
            lambda event: setattr(snowflake, "render_on_move", not snowflake.render_on_move))

        scoll_resolution.pack(side=LEFT, fill=BOTH)
        button_minus.pack(side=LEFT)
        input_order.pack(side=LEFT, expand=0.5, fill=BOTH)
        button_plus.pack(side=LEFT)
        button_reset.pack(side=LEFT)
        checkbox_render_on_move.pack(side=LEFT)

        checkbox_render_on_move.invoke()
        
        # This is what enables using the mouse:
        snowflake.canvas.bind("<ButtonPress-1>", snowflake.move_start)
        snowflake.canvas.bind("<B1-Motion>", snowflake.on_move)
        snowflake.canvas.bind("<ButtonRelease-1>", snowflake.move_stop)

        # For some it is <Button-2> and for some it's <Button-3>.
        snowflake.canvas.bind("<ButtonPress-2>", snowflake.scale_start)
        snowflake.canvas.bind("<B2-Motion>", snowflake.on_scale)
        snowflake.canvas.bind("<ButtonRelease-2>", snowflake.scale_stop)
        
        snowflake.canvas.bind("<ButtonPress-3>", snowflake.scale_start)
        snowflake.canvas.bind("<B3-Motion>", snowflake.on_scale)
        snowflake.canvas.bind("<ButtonRelease-3>", snowflake.scale_stop)
        
        # resize
        snowflake.canvas.bind('<Configure>', snowflake.update)

    def run(self):
        self.master.mainloop()

def main():
    SnowflakeApp(500, 300).run()
    