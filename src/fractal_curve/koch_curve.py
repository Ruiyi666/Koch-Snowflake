#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: fractal_curve/koch_curve.py
Author: Ruiyi Qian
Date: 2023/05/01
Description: This module contains the KochCurve class, it is a subclass of
    FractalCurve, and it overrides the create_children, update, and delete
"""

import math
from typing import Optional, Tuple, Union

from .base_curve import FractalCurve, Vector, BoundingBox, Canvas, Geometry

stroke = 2              # This is the stroke width of all the curves
margin = 0              # This is the margin between the snowflake and the canvas
resolution = 3          # This is the resolution of the curves, any length less than this will be ignored
update_call_count = 0   # This is the number of times the update function is called, just for debugging

class KochCurve(FractalCurve):
    """This class represents a koch curve. It is a subclass of FractalCurve,
    and it overrides the create_children, update, and delete functions.
    It requires the following parameters:
    
    canvas: The canvas on which the curve is drawn
    line: A tuple of two vectors, the start and end point of the curve
    order: The order of the curve, it can be an integer or a string. 
        If it is an integer, it is the order of the curve. 
        If it is not an integer, it means the order is infinite.
    """
    def __init__(
            self, 
            canvas: "Canvas", 
            line: Tuple[Vector, Vector],
            order: Union[int, str],
        ) -> None:
        super().__init__(order=order, canvas=canvas)
        p0 = line[0]
        p3 = line[1]
        self.object_id = canvas.create_line(p0.x, p0.y, p3.x, p3.y, width=stroke)
        
        self.first_id = self.object_id  # This is the id of the first component of the curve
        self.last_id = self.object_id   # This is the id of the last component of the curve
        self.element_count = 1          # This can be deleted, it is just for debugging
        
        self.last_within = False        # This is a flag to indicate if the component is within the bounding box at the last update
        self.last_outof = False         # This is a flag to indicate if the component is out of the bounding box at the last update
                                        # Both flags are used to determine if the component can be ignored in the next update
    
    def create_children(self):
        """This function creates the children of the current curve. There is no 
        recursion here, the children are created in the update function.
        """
        assert self.object_id is not None, "self.object_id is None"
        assert len(self.children) == 0, "len(self.children) != 0"
        canvas = self.canvas
        
        if not isinstance(self.order, int) or self.order > 0:
            """We only create children if the order is not infinite or greater than 0"""
            
            coords = canvas.coords(self.object_id)
            
            p0 = Vector(coords[0], coords[1])
            p3 = Vector(coords[2], coords[3])
            p1 = Vector((2 * p0.x + p3.x) / 3, (2 * p0.y + p3.y) / 3)
            p2 = Vector((p0.x + 2 * p3.x) / 3, (p0.y + 2 * p3.y) / 3)
            p_new = Vector((p1.x + p2.x) / 2 - (p2.y - p1.y) * 3 ** 0.5 / 2,
                        (p1.y + p2.y) / 2 + (p2.x - p1.x) * 3 ** 0.5 / 2)   
            
            self.canvas.delete(self.object_id)
            self.object_id = None
            
            self.children.extend([
                KochCurve(canvas, (p0, p1),     self.order - 1 if isinstance(self.order, int) else self.order),
                KochCurve(canvas, (p1, p_new),  self.order - 1 if isinstance(self.order, int) else self.order),
                KochCurve(canvas, (p_new, p2),  self.order - 1 if isinstance(self.order, int) else self.order),
                KochCurve(canvas, (p2, p3),     self.order - 1 if isinstance(self.order, int) else self.order),
            ])
    
    def delete(self):
        """When you want to delete the curve and all its children, you call this
        """
        if self.object_id is not None:
            self.canvas.delete(self.object_id)
            self.object_id = None
        for child in self.children:
            child.delete()
        del self.children[:]

    def delete_children(self):
        """When you want to delete the children and sub-children of the curve, you call this
        """
        if self.object_id is not None:
            return
        
        assert len(self.children) == 4, "len(self.children) != 4"
        
        for child in self.children:
            child.delete_children()
        
        # The following code is quite important. It is used to update the first_id and last_id
        # when children's children are deleted. we can then maintain the end points of the curve.
        self.first_id = self.children[0].first_id
        self.last_id = self.children[-1].last_id
        
        coords = self.canvas.coords(self.first_id)
        p0 = Vector(coords[0], coords[1])
        coords = self.canvas.coords(self.last_id)
        p3 = Vector(coords[2], coords[3])
        
        for child in self.children:
            self.canvas.delete(child.object_id)
        del self.children[:]
        self.children = []
        
        self.object_id = self.canvas.create_line(p0.x, p0.y, p3.x, p3.y, width=stroke)
        self.first_id = self.object_id
        self.last_id = self.object_id
        assert self.object_id is not None, "self.object_id is None"
    
        """
        I mean canvas in python tkinter, For a given screen coord x, y, 
        I can get canvas coord by canvasx, canvasy, how about know canvas coord x, y, 
        and get the screen coord, how can I know the screen_x, screen_y is out of screen? 
        """
        
    def within_screen(self, min_x, max_x, min_y, max_y):
        """This function checks if the bounding box of the curve is within the screen
        """
        global margin
        
        screen_width = self.canvas.winfo_width()
        screen_height = self.canvas.winfo_height()
        
        return max_x < screen_width - margin and min_x > margin and max_y < screen_height - margin and min_y > margin
        
    def outof_screen(self, min_x, max_x, min_y, max_y):
        """This function checks if the bounding box of the curve is out of the screen
        """
        global margin
        
        screen_width = self.canvas.winfo_width()
        screen_height = self.canvas.winfo_height()
        
        return min_x > screen_width - margin or max_x < margin or min_y > screen_height - margin or max_y < margin
    
    def too_small(self, min_x, max_x, min_y, max_y):
        """This function checks if the bounding box of the curve is too small to be drawn
        """
        dx = max_x - min_x
        dy = max_y - min_y
        
        return (dx ** 2 + dy ** 2) / resolution ** 2 < 1
    
    def get_coords(self):
        """This function returns the endpoints of the curve
        """
        coords = self.canvas.coords(self.first_id)
        p0 = Vector(coords[0], coords[1])
        coords = self.canvas.coords(self.last_id)
        p3 = Vector(coords[2], coords[3])
        p1 = Vector((2 * p0.x + p3.x) / 3, (2 * p0.y + p3.y) / 3)
        p2 = Vector((p0.x + 2 * p3.x) / 3, (p0.y + 2 * p3.y) / 3)
        p_new = Vector(
            (p1.x + p2.x) / 2 - (p2.y - p1.y) * 3 ** 0.5 / 2,
            (p1.y + p2.y) / 2 + (p2.x - p1.x) * 3 ** 0.5 / 2)
        
        xs = [p0.x, p3.x, p_new.x]
        ys = [p0.y, p3.y, p_new.y]
        
        return xs, ys
    
    def visiable(self, xs, ys):
        """Invisible means the bounding box of the curve is out of the screen or too small to be drawn
        """
        min_x = min(xs[:2])
        max_x = max(xs[:2])
        min_y = min(ys[:2])
        max_y = max(ys[:2])
        
        if self.too_small(min_x, max_x, min_y, max_y):
            return False
        
        min_x = min(min_x, xs[2])
        max_x = max(max_x, xs[2])
        min_y = min(min_y, ys[2])
        max_y = max(max_y, ys[2])
        
        if self.outof_screen(min_x, max_x, min_y, max_y):
            return False

        return True

    def update(self, scale_factor=None, order=None, *args):
        """When something changes, you call this function to update the curve

        Args:
            scale_factor (float, optional): if there is no scale_factor, we know
            it is only a translation, so we don't need to update the whole curve,
            those curves will not cross the screen will not be updated.
            
            order (int, optional): Reset the order of the curve. Normally, you
            need to call this function when you change the order of the curve.
            And None means no change.
        """
        global update_call_count
        update_call_count += 1
        # visiable mean it should have 4 children
        self.element_count = 1
        xs, ys = self.get_coords()
        
        cur_within = self.within_screen(min(xs), max(xs), min(ys), max(ys))
        cur_outof = self.outof_screen(min(xs), max(xs), min(ys), max(ys))
        
        # Skip update if the current state is the same as the last state
        if (self.last_within and cur_within) or (self.last_outof and cur_outof):
            
            if scale_factor is None and order is None:
                self.last_within = cur_within
                self.last_outof = cur_outof
                return
            
        self.last_within = cur_within
        self.last_outof = cur_outof
        
        if order is not None:
            self.order = order

        if self.visiable(xs, ys) and (not isinstance(self.order, int) or self.order > 0):
            if self.first_id == self.last_id:
                self.create_children()
            
            for child in self.children:
                child.update(scale_factor, order - 1 if isinstance(order, int) else order, *args)
                self.element_count += child.element_count
            
            self.first_id = self.children[0].first_id
            self.last_id = self.children[3].last_id
        else:
            if self.first_id != self.last_id:
                self.delete_children()

        return 
    
    def get_call_count(self):
        global update_call_count
        return update_call_count

    def clear_call_count(self):
        global update_call_count
        update_call_count = 0