from manim import *
import numpy as np
import math

x_min = -6.5
y_min = -3.5

x_max = 6.35
y_max = 3

def scaled_point (x,y,z):
    scale_tuple = (x,y,z)
    offset = (x_min,y_min,0)
    max_size = (x_max*2,y_max*2,0)
    
    scale_tuple = [offset[i]+max_size[i]*scale_tuple[i] for i in range(3)]
    
    return tuple(scale_tuple)

def displace(tuple_):
    return np.ndarray((3,),buffer=np.array([tuple_[0],tuple_[1],tuple_[2]]))

class fileSize(Scene):
    def construct(self):
        
        LAYER_SIZES = (
            "1x64x64", #input
            "16x64x64", #1 down out
            "32x32x32", #2 down out
            "48x32x32", #3 down out
            "64x16x16", #4 down out
            "96x16x16", #5 down out
            "128x8x8", #6 down out
            "256x8x8", #seed injection
            "128x8x8", #seed compression
            "96x16x16", #1 up out
            "64x16x16", #2 up out
            "48x32x32", #3 up out
            "32x32x32", #4 up out
            "16x64x64", #5 up out
            "1x64x64" #6 up out
        )
        
        #self.camera.background_color = WHITE
        
        x0_loc,y0_loc,x1_loc,y1_loc = 0,0.2,1,1
        
        x0,y0,null = scaled_point(x0_loc,y0_loc,0)
        x1,y1,null = scaled_point(x1_loc,y1_loc,0)
        
        gridSize = (2*7+1,8)
        
    #Draw Layers
        #Layer Rectangles
        for i in range(gridSize[0]):
            size_x = (x1-x0)/gridSize[0]
            size_y = y1-y0
            
            if i == 7:
                continue
            if i in (6,8):
                if i == 6:
                    size_x*=2
                size_y = size_y/gridSize[1]*2
            
            elif i in (4,5,9,10):
                size_y = size_y/gridSize[1]*4
            elif i in (2,3,11,12):
                size_y = size_y/gridSize[1]*6
                
            
            self.add(Rectangle(color = 0,width = size_x, height = size_y).shift(displace(scaled_point(1/gridSize[0]*i,y0_loc,0))).shift(displace((size_x/2,size_y/2,0))))
        
        #Layer size labels
        i = 0
        for word in LAYER_SIZES:
            if i == 7:
                i+=1
            self.add(Text(text = word, color = BLACK).scale(0.5).rotate(90*DEGREES).shift(displace(scaled_point(1/gridSize[0]*i,0.05,0))))
            i+=1
    
    #Darw Seed
        #Draw Rectangles
        unit_x = (x1-x0)/gridSize[0]
        unit_y = (y1-y0)/gridSize[1]
        #seed concat rectangle
        self.add(Rectangle(color = 0,width = unit_x, height = unit_y*2).shift(displace(scaled_point(1/gridSize[0]*7,y0_loc,0))).shift(displace((unit_x/2,unit_y,0))).shift(displace((0,unit_y*2,0))))
        self.add(Text(text = "128x8x8",color = BLACK).scale(0.3).rotate(90*DEGREES).shift(displace(scaled_point(1/gridSize[0]*7.5,1/gridSize[1]*4,0))))
        self.add(Rectangle(color = 0,width = unit_x*5, height = unit_y).shift(displace(scaled_point(1/gridSize[0]*5,y0_loc,0))).shift(displace((unit_x*5/2,unit_y/2,0))).shift(displace((0,unit_y*5,0))))
        self.add(Text(text = "8,192 long tensor",color = BLACK).scale(0.3).shift(displace(scaled_point(1/gridSize[0]*7.5,1/gridSize[1]*6,0))))
        self.add(Rectangle(color = 0,width = unit_x*3, height = unit_y).shift(displace(scaled_point(1/gridSize[0]*6,y0_loc,0))).shift(displace((unit_x*3/2,unit_y/2,0))).shift(displace((0,unit_y*7,0))))
        self.add(Text(text = "16-bit seed",color = BLACK).scale(0.3).shift(displace(scaled_point(1/gridSize[0]*7.5,1/gridSize[1]*7.5,0))))