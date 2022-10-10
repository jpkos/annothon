# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 07:28:08 2022

@author: jankos
"""

class BBox:
    def __init__(self, lbl, x, y, w, h, conf = None):
        self.lbl = int(lbl)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.conf = conf
        
    def iou(self, bbox):
        bb1 = self.as_xyxy()
        bb2 = bbox.as_xyxy()
        x_left = max(bb1[0], bb2[0])
        y_top = max(bb1[2], bb2[2])
        x_right = min(bb1[1], bb2[1])
        y_bottom = min(bb1[3], bb2[3])
        intersection_area = (x_right - x_left + 1) * (y_bottom - y_top + 1)
        bb1_area = (bb1[1] - bb1[0] + 1) * (bb1[3] - bb1[2] + 1)
        bb2_area = (bb2[1] - bb2[0] + 1) * (bb2[3] - bb2[2] + 1)
        iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
        return iou
    
    def as_xyxy(self):
        x1 = self.x - self.w/2
        x2 = self.x + self.w/2
        y1 = self.y - self.h/2
        y2 = self.y + self.h/2
        return (x1, x2, y1, y2)
    
    def __repr__(self):
        return f'{self.lbl} {self.x} {self.y} {self.w} {self.h} {self.conf}\n'
    