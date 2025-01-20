import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("model")
parser.add_argument("seed_start")
parser.add_argument("seed_end")
args = parser.parse_args()

program_start = time.time()

def time_worley(seed_start,seed_end):
    print("\nTiming Worley Noise:")
    section_time = time.time()
    from pythonworley import worley 
    print("\tImport time:",time.time()-section_time,"seconds")
    
    section_time = time.time()
    dataset = []
    for seed in range(seed_start,seed_end):
        w, c = worley((4,4), dens=16, seed=seed)
        w = w[0] 
        for x in range(64):
            for y in range(64):
                data = w[x][y]
                dataset.append(data)
    
    print("\tGenerating",seed_end-seed_start,"images took",time.time()-section_time,"seconds")
    return dataset

def time_open_simplex(seed_start,seed_end):
    print("\nTiming Open Simplex Noise:")
    section_time = time.time()
    import opensimplex
    print("\tImport time:",time.time()-section_time,"seconds")

    section_time = time.time()
    dataset=[]    
    for seed in range(seed_start,seed_end):
        opensimplex.seed(seed)
        for x in range(64):
            for y in range(64):
                data = opensimplex.noise2(x,y)
                dataset.append(data)
    
    
    print("\tGenerating",seed_end-seed_start,"images took",time.time()-section_time,"seconds")
    return dataset

def time_model_nn(seed_start,seed_end):
    print("\nTiming Neural Network Model:")
    section_time = time.time()
    import torch
    import AI_nn
    print("\tImport time:",time.time()-section_time,"seconds")
    model = AI_nn.NeuralNetworkModel()
    section_time = time.time()
    model.load_state_dict(torch.load(args.model,weights_only=True))
    print("\tLoading of the Neural Network Model took:",time.time()-section_time)

    preparation_time = 0
    generation_time = 0
    parsing_time = 0
    dataset=[]
    for seed in range(seed_start,seed_end):
        section_time = time.time()
        
        #Generate image inputs.
        seed = format(seed,"016b")
        seed = [float(x) for x in seed]
        seed = torch.Tensor(seed)
        seed = seed.view(-1,16)
        
        preparation_time += time.time()-section_time
        section_time = time.time()

        #Generate images with the model.
        output = model(seed)

        generation_time += time.time()-section_time
        section_time = time.time()

        #Parse output.
        for value in output.view(4096).data:
            dataset.append(float(value))
    
        parsing_time += time.time()-section_time

    print("\tImage generation of",seed_end-seed_start,"images took",preparation_time+generation_time+parsing_time,"seconds")
    print("\t\tPreparation took",preparation_time,"seconds")
    print("\t\tGeneration took",generation_time,"seconds")
    print("\t\tParsing took",parsing_time,"seconds")

    return dataset

def time_model_ced(seed_start,seed_end):    
    print("\nTiming Conditional Encoder Decoder Model:")
    section_time = time.time()
    import torch
    import AI_ced
    print("\tImport time:",time.time()-section_time,"seconds")
    model = AI_ced.ConditionalEncoderDecoderModel()
    section_time = time.time()
    model.load_state_dict(torch.load(args.model,weights_only=True))
    print("\tLoading of the Conditional Encoder Decoder Model took:",time.time()-section_time)
   
    preparation_time = 0
    generation_time = 0
    parsing_time = 0
    dataset = []
    for seed in range(seed_start,seed_end):
        section_time = time.time()

        #Prepare image inputs.
        image = torch.randn(64,64)
        sigmoid = torch.nn.Sigmoid()
        image = sigmoid(image)
        image = image.view(-1,64,64)        

        seed = format(seed,"016b")
        seed = [float(x) for x in seed]
        seed = torch.Tensor(seed)
        seed = seed.view(-1,16) 
        
        preparation_time += time.time()-section_time
        section_time = time.time()
        
        #Generate image.
        for i in range(100):
            output = model(image,seed)
            image = output.data
        
        generation_time += time.time()-section_time
        section_time = time.time()
        
        output = output.view(64,64).data
        
        #Parse output.
        for x in range(64):
            for y in range(64):
                dataset.append(float(output[x][y]))
        
        parsing_time += time.time()-section_time
        

    print("\tImage generation of",seed_end-seed_start,"images took a total of",preparation_time+generation_time+parsing_time,"seconds")
    print("\t\tPreparation took",preparation_time,"seconds")
    print("\t\tGeneration took",generation_time,"seconds")
    print("\t\tParsing took",parsing_time,"seconds")
    
    return dataset

def time_model_hy(seed_start,seed_end):
    print("\nTiming Hybrid Model:")
    section_time = time.time()
    import torch
    import AI_hy
    print("\tImport time:",time.time()-section_time,"seconds")
    model = AI_hy.HybridModel()
    section_time = time.time()
    model.load_state_dict(torch.load(args.model,weights_only=True))
    print("\tLoading of the Hybrid Model took:",time.time()-section_time)
    
        
    preparation_time = 0
    generation_time = 0
    parsing_time = 0
    dataset=[]
    for seed in range(seed_start,seed_end):
        section_time = time.time()
        
        #Generate image inputs.
        seed = format(seed,"016b")
        seed = [float(x) for x in seed]
        seed = torch.Tensor(seed)
        seed = seed.view(-1,16)
        
        preparation_time += time.time()-section_time
        section_time = time.time()

        #Generate images with the model.
        output = model(seed)

        generation_time += time.time()-section_time
        section_time = time.time()

        #Parse output.
        for value in output.view(4096).data:
            dataset.append(float(value))
    
        parsing_time += time.time()-section_time

    print("\tImage generation of",seed_end-seed_start,"images took",preparation_time+generation_time+parsing_time,"seconds")
    print("\t\tPreparation took",preparation_time,"seconds")
    print("\t\tGeneration took",generation_time,"seconds")
    print("\t\tParsing took",parsing_time,"seconds")

    return dataset

def main():
    #put model timing functions inside a dictionary.
    time_model = {
            "nn":time_model_nn,
            "ced":time_model_ced,
            "hy":time_model_hy
            }
    #put noise timing functions inside a dictionary.
    time_noise = {
            "os":time_open_simplex,
            "w":time_worley
            }

    #parse input parameters.
    model_type = args.model.split(".")[1]
    noise_type = args.model.split("_")[0]
    seed_start = int(args.seed_start)
    seed_end = int(args.seed_end)

    #call the respective functions.
    original_dataset = []
    model_dataset = []

    original_dataset = time_noise[noise_type](seed_start,seed_end)
    model_dataset = time_model[model_type](seed_start,seed_end)
    
    #Compare differences.
    section_time = time.time()
    difference = 0
    for i in range(4096):
        o_data = original_dataset[i]
        m_data = model_dataset[i]
        difference = abs(o_data-m_data)
    
    difference /= 4096

    print("\nComparing of results took",time.time()-section_time,"seconds")
    print("The difference of images is",difference)

if __name__ == "__main__":
    main()
    
