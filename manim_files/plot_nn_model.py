from manim import *
import numpy as np
import math

x_min = -6.5
y_min = -3.5

x_max = 6.35
y_max = 3.5

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
        
        #self.camera.background_color = WHITE
        
        layer_size = [16,64,256,1024,4096]
        layer_label = ["Input","Layer1","Layer2","Layer3","Output"]
        displacement = displace((0,0.6,0))
        
        circle_displacement_array = [[]]*5
        for j in range(5):
            width = 8+2*j
            for i in range(1,width):
                
                if i == width/2-1 or i == width/2+1:
                    self.add(Circle(color = BLACK, fill_opacity=1).scale(0.03).shift(displace(scaled_point(j/4,i/width,0.))).shift(displacement).shift(displace((0,0.12,0))))
                    self.add(Circle(color = BLACK, fill_opacity=1).scale(0.03).shift(displace(scaled_point(j/4,i/width,0.))).shift(displacement))
                    self.add(Circle(color = BLACK, fill_opacity=1).scale(0.03).shift(displace(scaled_point(j/4,i/width,0.))).shift(displacement).shift(displace((0,-0.12,0))))
                
                if i == width/2:
                    text = Text(text = f"{layer_size[j]-(width-4)}",color = BLACK).scale(0.5).shift(displace(scaled_point(j/4,0.57,0)))
                    self.add(text)
                
                if i in range(math.floor(width/2-1),math.ceil(width/2+2)):
                    continue
                circle_displacement = displace(scaled_point(j/4,i/width,0.))
                circle_displacement_array[j] = circle_displacement_array[j] + [circle_displacement]
                circle = Circle(color = BLACK, fill_opacity=1).scale(0.2).shift(circle_displacement).shift(displacement)
                self.add(circle)
        
        for i in range(len(circle_displacement_array)-1):
            for point_A in circle_displacement_array[i]:
                for point_B in circle_displacement_array[i+1]:                    
                    line = Line(start=point_A,end=point_B,color=BLACK,stroke_width=3).shift(displacement)
                    self.add(line)
        
        for i in range(5):
            label = Text(text=layer_label[i],color=BLACK).scale(0.5).shift(displace(scaled_point(i/4,0.05,0)))
            size_text = Text(text=f"{layer_size[i]} node",color=BLACK).scale(0.5).shift(displace(scaled_point(i/4,0,0)))
            self.add(label,size_text)
        
    