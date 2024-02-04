#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: snowflake.py
Author: Ruiyi Qian
Date: 2023/05/01
Description: Koch Snowflake fractal curve widget.
"""

import math

from tkinter import *
from tkinter.ttk import *
from typing import Optional, Union, Tuple
from .fractal_curve import Vector, KochCurve, koch_curve 

class KochSnowflake(Frame):
    """This class is a tkinter widget that renders a Koch Snowflake fractal curve
    in a canvas. It is a subclass of tkinter.Frame. It provides methods for
    updating the snowflake and resetting it.
    
    It requires the following arguments that can describe the snowflake:
    
        center, radius, rotation, order, stroke, resolution
        
    The master argument is the parent widget of the snowflake. 
    It is passed to the tkinter.Frame constructor.
    """
    def __init__(
            self, 
            master, 
            center: Union[Vector, Tuple[float, float]],
            radius: float, 
            rotation: float, 
            order: int=None,
            stroke: int=None,
            resolution: int=None,
        ) -> None:
        super().__init__(master)
        
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)
        self.curves = []
        self.scale_factor = 1
        self.scale_step_factor = 1.1

        self.render_on_move = False
        self.reset(center, radius, rotation, order, stroke, resolution)

    def update(self, *args):
        """This is the core method of the snowflake. It updates the snowflake
        when anything changes. 
        """
        for curve in self.curves:
            curve.clear_call_count()
            curve.update(*args)

    def set_resolution(self, resolution: int):
        koch_curve.resolution = resolution
        self.update(self.scale_factor)

    def get_resolution(self):
        return koch_curve.resolution

    def reset(
            self, 
            center: Union[None, Vector, Tuple[float, float]] = None, 
            radius: Optional[float] = None,
            rotation: Optional[float] = None,
            order: Optional[int] = None,
            stroke: Optional[int] = None,
            resolution: Optional[int] = None,
    ) -> None:
        """Initialize the snowflake with the given arguments. It is possible to
        change only some of the arguments. The arguments that are not given
        will be kept unchanged.
        """
        if  center is None and \
            radius is None and \
            rotation is None and \
            stroke is None and \
            resolution is None:
            # only order changed
            
            if order is None:
                return

            for curve in self.curves:
                curve.update(order=order - 1 if isinstance(order, int) else order),
            self.order = order 
            return

        for curve in self.curves:
            curve.delete()            
        del self.curves[:]

        if isinstance(center, tuple):
            center = Vector(*center)

        self.center = center if center is not None else self.center
        self.radius = radius if radius is not None else self.radius
        self.rotation = rotation if rotation is not None else self.rotation
        self.order = order if order is not None else self.order

        koch_curve.stroke = stroke if stroke is not None else koch_curve.stroke
        koch_curve.resolution = resolution if resolution is not None else koch_curve.resolution

        center = self.center
        radius = self.radius
        rotation = self.rotation
        order = self.order

        vectors = [
            Vector(0, -radius).rotate(rotation),
            Vector(0, -radius).rotate(rotation - 2 * math.pi / 3),
            Vector(0, -radius).rotate(rotation - 4 * math.pi / 3)
        ]
        
        vectors = [Vector(center.x + v.x, center.y + v.y) for v in vectors]
        
        canvas = self.canvas

        self.curves = [
            KochCurve(canvas, (vectors[0], vectors[1]), order - 1 if isinstance(order, int) else order),
            KochCurve(canvas, (vectors[1], vectors[2]), order - 1 if isinstance(order, int) else order),
            KochCurve(canvas, (vectors[2], vectors[0]), order - 1 if isinstance(order, int) else order),
        ]
        self.update()

    # ------------------------------------------------------------------------ #
    # -------------------------- Scale the snowflake ------------------------- #
    # ------------------------------------------------------------------------ #
    # The following methods are for scaling the snowflake.                     #
    # scale_start, on_scale, scale_stop are event handlers for mouse events.   #
    # scale_start is called when the left mouse button is pressed.             #
    # on_scale is called during mouse motion as the left mouse button pressed. #
    # scale_stop is called when the left mouse button is released.             #
    # ------------------------------------------------------------------------ #
    
    def scale_start(self, event):
        global scale_lastx, scale_lasty
        global scale_x, scale_y
        scale_lastx, scale_lasty = event.x, event.y
        scale_x, scale_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.canvas.create_oval(scale_x - 5, scale_y - 5, scale_x + 5, scale_y + 5, fill="red", tags="scale", outline="red")
    
    def on_scale(self, event):
        global scale_lastx, scale_lasty
        global scale_x, scale_y
        dx = event.x - scale_lastx
        dy = event.y - scale_lasty
        scale_lastx, scale_lasty = event.x, event.y
        scale_factor = self.scale_step_factor ** (dx / 10 + dy / 10)
        self.canvas.scale("all", scale_x, scale_y, scale_factor, scale_factor)
        self.scale_factor *= scale_factor
        if self.render_on_move:
            self.update(self.scale_factor)
        self.canvas.delete("scale")
        self.canvas.create_oval(scale_x - 5, scale_y - 5, scale_x + 5, scale_y + 5, fill="red", tags="scale", outline="red")

    def scale_stop(self, event):
        global scale_lastx, scale_lasty
        dx = event.x - scale_lastx
        dy = event.y - scale_lasty
        scale_lastx, scale_lasty = event.x, event.y
        scale_factor = self.scale_step_factor ** (dx / 10 + dy / 10)
        self.canvas.scale("all", scale_x, scale_y, scale_factor, scale_factor)
        self.update(self.scale_factor)
        self.canvas.delete("scale")

    # ------------------------------------------------------------------------ #
    # ------------------------- Move the snowflake --------------------------- #
    # ------------------------------------------------------------------------ #
    # The following methods are for moving the snowflake.                      #
    # move_start, on_move, move_stop are event handlers for mouse events.      #
    # move_start is called when the right mouse button is pressed.             #
    # on_move is called during the mouse movement as the right button pressed. #
    # move_stop is called when the right mouse button is released.             #
    # ------------------------------------------------------------------------ #
    
    def move_start(self, event):
        global drag_lastx, drag_lasty
        drag_lastx, drag_lasty = event.x, event.y
        # self.canvas.scan_mark(event.x, event.y)
        self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="red", tags="move", outline="red")
        
    def on_move(self, event):
        global drag_lastx, drag_lasty
        dx = event.x - drag_lastx
        dy = event.y - drag_lasty
        self.canvas.move("all", dx, dy)
        drag_lastx, drag_lasty = event.x, event.y
        # self.canvas.scan_dragto(event.x, event.y, gain=1)
        if self.render_on_move:
            self.update()
        self.canvas.delete("move")
        self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="red", tags="move", outline="red")
    
    def move_stop(self, event):
        global drag_lastx, drag_lasty
        dx = event.x - drag_lastx
        dy = event.y - drag_lasty
        self.canvas.move("all", dx, dy)
        drag_lastx, drag_lasty = event.x, event.y
        self.update()
        self.canvas.delete("move")
