from manim import *
import numpy as np

x_min = -6.5
y_min = -3.5

x_max = 6.5
y_max = 3.5

def scaled_point (x,y,z):
    scale_tuple = (x,y,z)
    offset = (x_min,y_min,0)
    max_size = (x_max*2,y_max,0)
    
    scale_tuple = [offset[i]+max_size[i]*scale_tuple[i] for i in range(3)]
    
    return tuple(scale_tuple)

    

class fileSize(Scene):
    def construct(self):
        
        #self.camera.background_color = WHITE
        
        data_label = [8,10,12,14,16]
        max_data = 65536*32/1024
        file_size = [int((2**x)*32/1024) for x in data_label]
        data = [(2**x)*32/1024 for x in data_label]
        
        for i in range(1,len(data)+1):
            data_point = data[i-1]
            data_point = scaled_point(i/(len(data)+1),data_point/max_data,0)
            data[i-1] = data_point
        
        line_x = Line(start=scaled_point(0,0,0), end=scaled_point(1,0,0),color=BLACK)
        arrow_x = Triangle(color=BLACK,fill_opacity=1).scale(0.1).rotate(30*DEGREES).next_to(line_x,np.ndarray((3,),buffer=np.array([0.1,0,0]))).shift(np.ndarray((3,),buffer=np.array([-0.1,0,0])))
        label_x = Text(text="Seed Size",color=BLACK).scale(0.5).next_to(line_x,np.ndarray((3,),buffer=np.array([0.1,-0.1,0]))).shift(np.ndarray((3,),buffer=np.array([-1.2,-0.1,0.])))
        line_y = Line(start=scaled_point(0,0,0), end=scaled_point(0,1.01,0),color=BLACK)
        label_y = Text(text="Dataset Size",color=BLACK).scale(0.5).rotate(90*DEGREES).next_to(line_y,np.ndarray((3,),buffer=np.array([-0.6,0,0]))).shift(np.ndarray((3,),buffer=np.array([0.,1,0.])))
        arrow_y = Triangle(color=BLACK,fill_opacity=1).scale(0.1).next_to(line_y,np.ndarray((3,),buffer=np.array([0,0.1,0]))).shift(np.ndarray((3,),buffer=np.array([0,-0.1,0])))
        previous_point = scaled_point(0,0,0)
        for idx in range(len(data)):
            current_point = data[idx]
            line = Line(start=previous_point, end=current_point, color = BLACK)
            previous_point = current_point
            
            marker_line_x = Line(start=(current_point[0],y_min-0.1,0),end=(current_point[0],current_point[1],0),stroke_width=1,color=BLACK)
            
            marker_line_y = Line(start=(x_min-0.1,current_point[1],0),end=(x_min,current_point[1],0),stroke_width=1,color=BLACK)
            
            point = Circle(color = BLACK,  fill_opacity=1).scale(0.05).next_to(marker_line_x,np.ndarray((3,), buffer=np.array([0.,1e-10,0]))).shift(np.ndarray((3,), buffer=np.array([0.,-0.05,0])))
            
            name = Text(text=f"{data_label[idx]}-bit",color=BLACK).scale(0.5).next_to(marker_line_x,np.ndarray((3,), buffer=np.array([0.,-0.1,0])))
            value = Text(text=f"{file_size[idx]}MB",color=BLACK).scale(0.5).next_to(marker_line_x,np.ndarray((3,), buffer=np.array([-0.5,0.1,0])))
            
            self.add(line,marker_line_x,marker_line_y,name,value,point)
        self.add(line_x,line_y,label_x,label_y,arrow_x,arrow_y)