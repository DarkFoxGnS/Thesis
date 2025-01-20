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
        y_max_avg_data = 0.0004
        y_max_eval_data = 0.07
        
        ################################
        #Loading data
        
        file = open("w_model_14_hy\\model_14.stat","r")
        
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
        x_label_025 = Text(text = f"{int(dataset_size/4*1)}",color=BLACK).scale(0.4).shift(to_np(scaled_point(0.25*x_scale,-0.05,0)))
        x_label_05 = Text(text = f"{int(dataset_size/2)}",color=BLACK).scale(0.4).shift(to_np(scaled_point(0.5*x_scale,-0.05,0)))
        x_label_075 = Text(text = f"{int(dataset_size/4*3)}",color=BLACK).scale(0.4).shift(to_np(scaled_point(0.75*x_scale,-0.05,0)))
        x_label_1 = Text(text = f"{dataset_size}",color=BLACK).scale(0.4).shift(to_np(scaled_point(1*x_scale,-0.05,0)))
        x_line_0 = Line(start = scaled_point(0,-0.02,0), end = scaled_point(0,0.02,0),color = BLACK,stroke_width = 1)
        self.add(x_label_0,x_label_025,x_label_05,x_label_075,x_label_1,x_line_0)
        
        y_label_0 = Text(text = "0",color=BLACK).scale(0.4).shift(to_np(scaled_point(-0.015,0,0)))
        y_label_4_avg = Text(text = f"{y_max_avg_data}",color=BLACK).scale(0.4).rotate(90*DEGREES).shift(to_np(scaled_point(-0.04,1*y_scale,0)))
        y_label_4_eval = Text(text = f"{y_max_eval_data}",color=RED).scale(0.4).rotate(90*DEGREES).shift(to_np(scaled_point(-0.02,1*y_scale,0)))
        
        y_line_0 = Line(start = scaled_point(-0.005,0,0), end = scaled_point(0.005,0,0),color = BLACK,stroke_width = 1)
        y_line_4 = Line(start = scaled_point(-0.005,1*y_scale,0), end = scaled_point(0.005,1*y_scale,0),color = BLACK,stroke_width = 1)
        self.add(y_label_0,y_label_4_avg,y_label_4_eval,y_line_4,y_line_0)
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
            #print(cur_eval_performance)
            cur_x_loc = (cur_epoch*x_scale+1)/(dataset_size+1)
            cur_avg_y_loc = cur_avg_performance/y_max_avg_data
            cur_eval_y_loc = cur_eval_performance/y_max_eval_data
            
            prev_epoch = idx-1
            prev_avg_performance = float(prev_point[2])
            prev_eval_performance = float(prev_point[3])
            prev_x_loc = (prev_epoch*x_scale+1)/(dataset_size+1)
            prev_avg_y_loc = prev_avg_performance/y_max_avg_data
            prev_eval_y_loc = prev_eval_performance/y_max_eval_data
            
            avg_line = Line(start = scaled_point(prev_x_loc,prev_avg_y_loc,0), end = scaled_point(cur_x_loc,cur_avg_y_loc,0),color=BLACK,stroke_width = 2)
            eval_line = Line(start = scaled_point(prev_x_loc,prev_eval_y_loc,0), end = scaled_point(cur_x_loc,cur_eval_y_loc,0),color=RED,stroke_width = 2)
            
            avg_difference = prev_avg_performance - cur_avg_performance
            
            prev_point = cur_data
            
            if (idx+1) % (dataset_size/4) == 0:
                tick = Line(start = scaled_point(cur_x_loc,-0.02,0), end = scaled_point(cur_x_loc,0.01,0), color = BLACK, stroke_width = 1)
                self.add(tick)
            
            self.add(eval_line,avg_line)
        
        #######################################
        #Lowest average loss mark.
        values = [[]]*len(dataset)
        for idx in range(len(dataset)):
            x = dataset[idx]
            #print(x,idx)
            values[idx] = [float(x[2]),idx+1]
        lowest_loss = min(values)
        print("Lowest avg. loss",lowest_loss)
        
        self.add(Line(start = scaled_point((int(lowest_loss[1])*x_scale)/(dataset_size+1),-0.02,0), end = scaled_point((int(lowest_loss[1])*x_scale)/(dataset_size+1),1,0), color = BLACK, stroke_width = 1))
        self.add(Text("Lowest avg. loss",color = BLACK).scale(0.4).rotate(90*DEGREES).shift(to_np(scaled_point((int(lowest_loss[1])*x_scale)/(dataset_size+1)+0.01,0.7,0))))
        
        #######################################
        #Lowest per image loss.
        
        values = [[]]*len(dataset)
        for idx in range(len(dataset)):
            x = dataset[idx]
            values[idx] = [float(x[3]),idx+1]
        lowest_loss = min(values)
        print("Lowest loss",lowest_loss)
        
        self.add(Line(start = scaled_point((int(lowest_loss[1])*x_scale)/(dataset_size+1),-0.02,0), end = scaled_point((int(lowest_loss[1])*x_scale)/(dataset_size+1),1,0), color = BLACK, stroke_width = 1))
        self.add(Text("Lowest loss",color = BLACK).scale(0.4).rotate(90*DEGREES).shift(to_np(scaled_point((int(lowest_loss[1])*x_scale  )/(dataset_size+1)-0.01,0.7,0))))
