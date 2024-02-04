#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: fractal_curve/base_curve.py
Author: Ruiyi Qian
Date: 2023/05/01
Description: Base class for fractal curves. This module provides the base class
    for fractal curves.
"""

import math
from tkinter import Canvas
from typing import Optional, Tuple


""" 
Weather do draw a component of the fractal or not, will depend on the
visibility of the component's bounding box, and the resolution of the
screen.

compoenent state: 
    - have children or not  : H, NH
    - draw or not           : D, ND

(1) H, D : 
(2) H, ND 
(3) NH, D
(4) NH, ND
    

split if inside the canvas and current resolution is too low
merge if outside the canvas or current resolution is high enough

"""


BoundingBox = Tuple[float, float, float, float]
    
class Geometry:
    def __init__(self, canvas: Optional[Canvas] = None):
        self.canvas = canvas
        self.children = []
        self.bbox = None
        self.object_id = None
        
    def visiable(self):
        if self.bbox is None:
            return False
        x0, y0, x1, y1 = self.bbox
        x0, y0 = self.canvas.canvasx(x0), self.canvas.canvasy(y0)
        if x0 > self.canvas.winfo_width() or y0 > self.canvas.winfo_height():
            return False
        x1, y1 = self.canvas.canvasx(x1), self.canvas.canvasy(y1)
        if x1 < 0 or y1 < 0:
            return False
        
        dx = x1 - x0
        dy = y1 - y0
        if dx * dx + dy * dy < 40:
            return False
        
        return True
    
    def draw(self):
        for child in self.children:
            child.draw()
    
    def erase(self):
        for child in self.children:
            child.erase()
    
    
class Vector:
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y
         
    def rotate(self, angle):
        x = self.x 
        y = self.y
        self.x = x * math.cos(angle) - y * math.sin(angle)
        self.y = x * math.sin(angle) + y * math.cos(angle)
        return self
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
   
    
class FractalCurve(Geometry):
    def __init__(self, canvas: "Canvas", order: Optional[int]) -> None:
        super().__init__(canvas)
        self.order = order
            
    def create_children(self):
        pass
    
    def delete_children(self):
        pass
            
    

    
