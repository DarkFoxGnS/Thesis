from manim import *
import numpy as np

x_min = -6.5
y_min = -3.5

x_max = 6
y_max = 3.5

#maps from 0 to 1 to the xy_min to xy_max
def scaled_point (x,y,z):
    scale_tuple = (x,y,z)
    offset = (x_min,y_min,0)
    max_size = (x_max*2,y_max,0)
    
    scale_tuple = [offset[i]+max_size[i]*scale_tuple[i] for i in range(3)]
    
    return tuple(scale_tuple)
    
def to_np(tuple_):
    return np.ndarray((3,),buffer=np.array([tuple_[0],tuple_[1],tuple_[2]]))

class modelLoss(Scene):
    def construct(self):
        
        ################################
        #Variables
        x_scale = 0.95
        y_scale = 0.95
        #y_max_data = 0.04
        y_max_data = 0.09
        ################################
        #Loading data
        
        file = open("..\\os_model_8_diff\\model_8.stat","r")
        
        dataset = file.read()
        dataset = dataset[0:-1].split("\n")
        dataset = [x.split(";") for x in dataset]
        dataset_size = len(dataset)
        
        
        
        ################################
        #White background, shant be included in the final render.
        
        #self.camera.background_color = WHITE
        
        ################################
        #Plot the axes
        
        line_x = Line(start=scaled_point(0,0,0), end=scaled_point(1,0,0),color=BLACK)
        arrow_x = Triangle(color=BLACK,fill_opacity=1).scale(0.1).rotate(30*DEGREES).next_to(line_x,to_np((0.1,0,0))).shift(to_np((-0.1,0,0)))
        label_x = Text(text="Epoch",color=BLACK).scale(0.5).next_to(line_x,to_np((0.1,-0.1,0))).shift(to_np((0,-0.1,0.)))
        line_y = Line(start=scaled_point(0,0,0), end=scaled_point(0,1.01,0),color=BLACK)
        label_y = Text(text="Loss",color=BLACK).scale(0.5).rotate(90*DEGREES).next_to(line_y,to_np((-0.6,0,0)))
        arrow_y = Triangle(color=BLACK,fill_opacity=1).scale(0.1).next_to(line_y,to_np((0,0.1,0))).shift(to_np((0,-0.1,0)))
        self.add(line_x,line_y,arrow_x,arrow_y,label_x,label_y)
        
        ################################
        #Plot labels.
        
        x_label_0 = Text(text = "0",color=BLACK).scale(0.4).shift(to_np(scaled_point(0,-0.05,0)))
        x_label_100 = Text(text = f"{int(dataset_size/2)}",color=BLACK).scale(0.4).shift(to_np(scaled_point(0.5*x_scale,-0.05,0)))
        x_label_200 = Text(text = f"{dataset_size}",color=BLACK).scale(0.4).shift(to_np(scaled_point(1*x_scale,-0.05,0)))
        x_line_0 = Line(start = scaled_point(0,-0.02,0), end = scaled_point(0,0.02,0),color = BLACK,stroke_width = 1)
        self.add(x_label_0,x_label_100,x_label_200,x_line_0)
        
        y_label_0 = Text(text = "0",color=BLACK).scale(0.4).shift(to_np(scaled_point(-0.015,0,0)))
        y_label_4 = Text(text = f"{y_max_data}",color=BLACK).scale(0.4).shift(to_np(scaled_point(-0.025,1*y_scale,0)))
        
        y_line_0 = Line(start = scaled_point(-0.005,0,0), end = scaled_point(0.005,0,0),color = BLACK,stroke_width = 1)
        y_line_4 = Line(start = scaled_point(-0.005,1*y_scale,0), end = scaled_point(0.005,1*y_scale,0),color = BLACK,stroke_width = 1)
        self.add(y_label_0,y_label_4,y_line_4,y_line_0)
        ################################
        #Plot data.
        
        #Init and plot the 0th element.
        prev_point = dataset[0]
        self.add(Line(start = scaled_point(1/(dataset_size+1), -0.02, 0), end = scaled_point(1/(dataset_size+1), 0.01, 0), color = BLACK, stroke_width = 1))
        
        #Plot other elements.
        
        for idx in range(1,dataset_size):
            cur_data = dataset[idx]
            cur_epoch = idx
            cur_avg_performance = float(cur_data[2])
            cur_eval_performance = float(cur_data[3])
            print(cur_eval_performance)
            cur_x_loc = (cur_epoch*x_scale+1)/(dataset_size+1)
            cur_avg_y_loc = cur_avg_performance/y_max_data
            cur_eval_y_loc = cur_eval_performance/y_max_data
            
            prev_epoch = idx-1
            prev_avg_performance = float(prev_point[2])
            prev_eval_performance = float(prev_point[3])
            prev_x_loc = (prev_epoch*x_scale+1)/(dataset_size+1)
            prev_avg_y_loc = prev_avg_performance/y_max_data
            prev_eval_y_loc = prev_eval_performance/y_max_data
            
            #Add line of regression based on observed start of regression
            if idx == 600:
                self.add(Line(start = scaled_point(cur_x_loc,-0.02,0), end = scaled_point(cur_x_loc,1,0), color = BLACK, stroke_width = 1))
                self.add(Text("Dataset saturation",color = BLACK).scale(0.4).rotate(90*DEGREES).shift(to_np(scaled_point(cur_x_loc-0.01,0.6,0))))
            
            avg_line = Line(start = scaled_point(prev_x_loc,prev_avg_y_loc,0), end = scaled_point(cur_x_loc,cur_avg_y_loc,0),color=BLACK,stroke_width = 2)
            eval_line = Line(start = scaled_point(prev_x_loc,prev_eval_y_loc,0), end = scaled_point(cur_x_loc,cur_eval_y_loc,0),color=RED,stroke_width = 2)
            
            avg_difference = prev_avg_performance - cur_avg_performance
            
            #Observe frequent low changes to find point of regression.
            if abs(avg_difference *10000) < 0.1:
                print(idx,avg_difference)
            
            prev_point = cur_data
            
            tick = Line(start = scaled_point(cur_x_loc,-0.02,0), end = scaled_point(cur_x_loc,0.01,0), color = BLACK, stroke_width = 1)
            
            self.add(eval_line,avg_line,tick)
        
        #######################################
        #Lowest average loss mark.
        values = [[]]*len(dataset)
        for idx in range(len(dataset)):
            x = dataset[idx]
            print(x,idx)
            values[idx] = [float(x[2]),idx]
        lowest_loss = min(values)
        print("Lowest avg. loss",lowest_loss)
        
        self.add(Line(start = scaled_point((int(lowest_loss[1])*x_scale+1)/(dataset_size+1),-0.02,0), end = scaled_point((int(lowest_loss[1])*x_scale+1)/(dataset_size+1),1,0), color = BLACK, stroke_width = 1))
        self.add(Text("Lowest avg. loss",color = BLACK).scale(0.4).rotate(90*DEGREES).shift(to_np(scaled_point((int(lowest_loss[1])*x_scale+1)/(dataset_size+1)+0.01,0.7,0))))
        
        #######################################
        #Lowest per image loss.
        
        values = [[]]*len(dataset)
        for idx in range(len(dataset)):
            x = dataset[idx]
            values[idx] = [float(x[3]),idx]
        lowest_loss = min(values)
        print("Lowest loss",lowest_loss)
        
        self.add(Line(start = scaled_point((int(lowest_loss[1])*x_scale+1)/(dataset_size+1),-0.02,0), end = scaled_point((int(lowest_loss[1])*x_scale+1)/(dataset_size+1),1,0), color = BLACK, stroke_width = 1))
        self.add(Text("Lowest loss",color = BLACK).scale(0.4).rotate(90*DEGREES).shift(to_np(scaled_point((int(lowest_loss[1])*x_scale+1)/(dataset_size+1)-0.01,0.7,0))))