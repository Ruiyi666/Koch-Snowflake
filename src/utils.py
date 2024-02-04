#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: utils.py
Author: Ruiyi Qian
Date: 2023/05/01
Description: Utility functions for the Koch Snowflake fractal curve.
"""

def to_order(order_str):
    if order_str == "inf":
        return "inf"
    try:
        order = int(order_str)
        if order <= 0:
            return None
        else:
            return order
    except ValueError:
        return None
    
def increase_order(order):
    return order - 1 if isinstance(order, int) and order > 1 else "inf"

def decrease_order(order):
    return order + 1 if isinstance(order, int) else 1