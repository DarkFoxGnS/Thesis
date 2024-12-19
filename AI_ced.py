#Only execute when the file is executed directly
if __name__ == "__main__":
 
    ##################################
    #Default parameters
    map_size = 64
    learning_curve = 0.001
    batch_size = 16
    epoch_count = 200
    maximum_noise_steps = 100
    
    model_name = "model"
    working_dirctory = "."
    device = "cuda"
    ##################################


    #handle arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-model",type=str,help="Name of the model, this will be used to locate the .data, the .label and the .pth inside the directory.")
    parser.add_argument("-dir",type=str,help="Location of the model, will use name of the model as the directory by default.")
    parser.add_argument("-batch",type=int,help="Bach size, defaults to 64.")
    parser.add_argument("-epoch",type=int,help="Epoch size, defaults to 10.")
    parser.add_argument("-device",type=str,help="Which device to use, \"cpu\" for CPU based usage, cuda for \"GPU based usage\"")
    parser.add_argument("-lr",type=float,help="The learning curve of the model or training. Default 0.001")

    args = parser.parse_args()
    
    #Overwrite default values if parameter was passed in.
    if args.model:
        model_name = args.model
    if args.dir:
        working_dirctory = args.dir
    if args.batch:
        batch_size = args.batch
    if args.epoch:
        epoch_count = args.epoch
    if args.device:
        device = args.device
    if args.lr:
        learning_curve = args.lr

    #Manage imports
    import time
    import numpy as np
    from PIL import Image
    import random
    import math
    import os
    
    #Create time to measure execution time
    start_timer = time.time()
import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
class DiffuseModel(nn.Module):
    """
    This is a subclass of the Torch.nn.Module.
    Takes the 16bit value of the seed as input, and produces a 64x64 image in a single array.
    """
    def __init__ (self):
        """
        Called on the construction of the model. Creates all the layers of the model.
        """
        super().__init__()
        self.compress =nn.Sequential( #Define compression layers.
            nn.Conv2d(1,16,3,1,1),
            nn.Conv2d(16,32,3,2,1),
            nn.ReLU(),
            nn.Conv2d(32,48,3,1,1),
            nn.Conv2d(48,64,3,2,1),
            nn.ReLU(),
            nn.Conv2d(64,96,3,1,1),
            nn.Conv2d(96,128,3,2,1),
            nn.ReLU(),
        )
        
        self.seed_matrix = nn.Linear(16,128*8*8) #Transform the seed to the expanded seed.
        self.seed_combiner = nn.Conv2d(256,128,1) #Force the combined seed and bottleneck of x together.
                
        self.decompress = nn.Sequential( #Transform the bottleneck back to the image.
            nn.ConvTranspose2d(128,96,3,1,1),
            nn.ConvTranspose2d(96,64,4,2,1),
            nn.ReLU(),
            nn.ConvTranspose2d(64,48,3,1,1),
            nn.ConvTranspose2d(48,32,4,2,1),
            nn.ReLU(),
            nn.ConvTranspose2d(32,16,3,1,1),
            nn.ConvTranspose2d(16,1,4,2,1),
            nn.Sigmoid(),
        )
    
    def forward(self, x,seed):
        """
        This is called during the execution of the model.
        @params
            x (Tensor): The seed in the form of 16 bits as floats in a 1D Tensor.
        @returns
            logits (Tensor): The image generated by the model in a 1D Tensor.
        """
        
        x = self.compress(x) #Compress the image to [-1,256,8,8]
        seed = self.seed_matrix(seed).view(-1,128,8,8) #Expand the seed to [-1,256,8,8]
        
        temp = torch.cat([x.view(-1,128,8,8),seed],dim=1) #Combine the seed and the x on the first dimension resulting in [-1,512,8,8]
        x = self.seed_combiner(temp) #Transform [-1,256,8,8] seed and x combination into [-1,256,8,8]
        
        x = self.decompress(x) #Decompress the image to generate the final image.
        return x
        
class NoiseDataset(Dataset):
    """
    This is a custom dataset, a subclass of torch.utils.data.Dataset, and is used to load in custom dataset.
    """
    def __init__(self, seed_file_path, binary_file_path):
        """
        @params
            seed_file_path (String): Path to the text file containing comma-separated seeds.
            binary_file_path (String): Path to the single binary file containing sequential noise maps.
        """
        # Read seeds from the text file
        with open(seed_file_path, 'r') as f:
            self.seeds = [int(seed.strip()) for seed in f.read().split(';')]

        #Store the binary file path for faster retreival time of data.
        self.binary_file_path = binary_file_path

        self.num_samples = len(self.seeds) # calculate the number of samples.
        self.floats_per_map = map_size * map_size  # calculate the number of floats per map.
        self.bytes_per_map = self.floats_per_map * 8 #Calculate the total ammount of bytes per map.

    def __len__(self):
        """
        It returns the number of samples in the dataset.
        @returns
            samples (Integer): The number of samples in the dataset.
        """
        #Total number of samples
        return self.num_samples

    def __getitem__(self, idx):
        """
        
        @params
            idx (Integer): The ID of the map and seed to be loaded.
        @returns
            seed_tensor (Tensor): The seed of the map at idx.
            noise_map_tensor (Tensor): The map at idx.
        """
        #Get the seed
        seed = self.seeds[idx]
        binary_str = format(seed, '016b')
        binary_list = [float(bit) for bit in binary_str]
        
        
        #Load the noise map from the binary file using the offset.
        noise_map = self._load_noise_map(idx)

        #Convert to PyTorch tensors
        seed_tensor = torch.tensor(binary_list, dtype=torch.float32).view(1,16)
        noise_map_tensor = torch.tensor(noise_map, dtype=torch.float32).view(1,64,64) #Convert to [1,64,64] to work with Conv2d and ConvTranspose2d.
        
        return seed_tensor, noise_map_tensor

    def _load_noise_map(self, idx):
        """
        Load the map from the storage.
        @params
            idx (integer): The id of the map.
        @returns
            data (float 32 Array): The map in an array as float 32.
        """
        #Calculate the byte offset for the current noise map.
        offset = idx * self.bytes_per_map

        #Read 4096 floats (8 bytes each) starting from the calculated offset.
        with open(self.binary_file_path, 'rb') as f:
            f.seek(offset)
            data = np.fromfile(f, dtype=np.float64, count=self.floats_per_map)
            
        return data.astype(np.float32)  #Convert to single precision float for PyTorch.

def noiser(images,max_steps,noise_step):
    """
    Applies random noise to the input images.
    @params
        images (Tensor): Images to be noised.
        max_steps (Integer): Maximum noising steps.
        noise_step (Integer): The current step of the noising process.
    """
    
    hardTanh = nn.Hardtanh(0,1) #Function to force between 0 to 1, with linear output for inbetween values.
    tanhFunc = nn.Tanh() #Function to force between -1 to 1.
    noise = torch.randn_like(images) * (noise_step/max_steps) #Create a noise dataset.
    noise = tanhFunc(noise) #Force it to be between -1 to 1.
    
    noised_images = images+noise #Disfigurate the images based on noise.
    noised_images = hardTanh(noised_images) #Force the noised_images between 0 to 1
    
    return noised_images

def training(model, data, loss_function, optimizer):
    """
    Trains trains the AI on the given data set.
    @params
        model (Module): This model will be trained.
        data (DataLoader): This dataloader holds the data to be trained.
        loss_function (LossFunction): This functions will be used to evaluate the performance of the model.
        optimizer (Optimizer): The optimizer, which will train the model.
    @returns
        batch_loss (Float): The average of losses observer during training.
    """
    model.train() #Set the model to training mode.
    epoch_loss = 0#It will hold the combined losses.
    executed_batches = 0.#It will hold the executed batch counts, allows for partially full batches.
    for batch,(seed, map) in enumerate(data):
        
        executed_batches+=len(seed)/batch_size #the lenght of seeds are the size of the current batch, and divided by batch size allows for not full batches to be calculated.
        batch_loss = 0
        
        for i in range(1,maximum_noise_steps):
            noised_map = noiser(map,maximum_noise_steps,i)
            #Send the seed and the map to the selected device (if needed).
            noised_map = noised_map.to(device)
            seed = seed.to(device)
            map = map.to(device)
            
            #Evaluate the model.
            output = model(noised_map,seed)
            
            #Use the optimizer and the loss function to train the model.
            optimizer.zero_grad()
            loss = loss_function(output,map)
            loss.backward()
            optimizer.step()
            
            #Add to combined loss
            batch_loss += loss.item()
        
        current_loss = batch_loss/maximum_noise_steps
        #Log to console.
        print(f"Batch {batch} reported with loss {current_loss}")
        epoch_loss += current_loss
    return epoch_loss/executed_batches #Gives an average in the entire epoch

def generateImage(model,seed,epoch):
    """
    Generates an image and saves it to hard drive.
    @params
        model (Module): The model to be used to generate an image.
        seed (Integer): The seed use to generate the image.
        epoch (Integer): The current epoch during the testing.
    """
    print(f"Generating seed: {seed}")
    model.eval()
    #Create image.
    image = Image.new("RGB",(64,64))
    pixels = image.load()
    
    #Convert seed.
    seed_str = format(seed,"016b")
    seed_array = [float(x) for x in seed_str]
    seed_tensor = torch.tensor(seed_array).view(1,-1)
    seed_tensor = seed_tensor.to(device)
    
    #Create Dummy image.
    sigmoidFunc = nn.Sigmoid()
    imageTensor = sigmoidFunc(torch.randn(1,1,64,64))
    imageTensor = imageTensor.to(device)
    
    #Generate image via model.
    for i in range(maximum_noise_steps):
        output = model(imageTensor,seed_tensor)
        imageTensor = output.data
    
    imageTensor = imageTensor.view(64,64)
    #Convert generated data into image.
    for i in range(64):
        for j in range(64):
            data = imageTensor[i][j]
            data = int(255*data)
            pixels[i,j] = (data,data,data)
    
    #Create images directory if not existing.
    try:
        os.mkdir(f"{working_dirctory}\\images\\majorSteps")
    except Exception:
        pass
    
    #Save image.
    image.save(f"{working_dirctory}\\images\\majorSteps\\{model_name}_{seed}_generated_{epoch}.png","PNG")

def testWithImage(model,data,seed_,loss_function):
    """
    Testing method to producte image.
    @params
        model (Module): The model to be tested.
        data (DataSet): The dataset to be used for original image.
        seed_ (Integer): The seed to be tested.
        loss_function (LossFunction): The loss function to be used to observer the loss of the AI.
    @returns
        loss (Float): The evaluated loss.
    """
    
    print(f"Testing {seed_}")
    #Create Image objects for the original and the generated images, and create pixel array from it.
    generated_image = Image.new(mode="RGB",size = (64,64))
    generated_pixels = generated_image.load()
    
    original_image = Image.new(mode="RGB",size = (64,64))
    original_pixels = original_image.load()
    
    #Set model into evaluation mode.
    model.eval()
    
    #Get the original image at the seed.
    (seed,trained_data)=data[seed_]
    print(f"Testing seed {seed_} ({seed})")
    
    #Move the Seed and the Data to the device if needed.
    seed = seed.view(1,-1).to(device)
    trained_data = trained_data.to(device)
    
    #Create Dummy image.
    sigmoidFunc = nn.Sigmoid()
    imageTensor = sigmoidFunc(torch.randn(1,1,64,64))
    imageTensor = imageTensor.to(device)
    
    #Execute the model.
    for i in range(maximum_noise_steps):
        output = model(imageTensor,seed)
        imageTensor = output.data
        
    trained_data = trained_data.view(64,64)
    imageTensor = imageTensor.view(64,64)
    #Observe loss.
    loss = loss_function(imageTensor,trained_data)
    #Reshape the Tensors into 64 by 64 view.
    outimage = imageTensor.view(64, 64)
    trained_data = trained_data.view(64, 64)
    
    #Write the images based on the generated and the original data.
    for x in range(64):
        for y in range(64):
            outdata = int(outimage[x][y]*255)
            original_data = int(trained_data[x][y]*255)
            
            generated_pixels[x,y] = (outdata,outdata,outdata)
            original_pixels[x,y] = (original_data,original_data,original_data)
            
    #Log the console and save the generated images.
    currentTime = time.time()
    try:
        os.mkdir(f"{working_dirctory}\\images")#Create images directory if not existing.
    except Exception:
        pass
    generated_image.save(f"{working_dirctory}\\images\\{int(start_timer)}_{int(currentTime)}_{model_name}_{seed_}_generated.png","PNG")
    original_image.save(f"{working_dirctory}\\images\\{int(start_timer)}_{int(currentTime)}_{model_name}_{seed_}_original.png","PNG")
    
    return loss.item()
        
def main():
    """
    Main function.
    """
    #Create a section_timer that is used to measure the performance during training, and testing.
    section_timer = start_timer
    
    #Get the data and label files.
    datafile = f"{working_dirctory}\\{model_name}.data"
    labelfile = f"{working_dirctory}\\{model_name}.label"
        
    
    print(f"Starting AI training {model_name}")
    print(f"Creating model...")
    
    #Use the model if it exists, else create new.
    try:
        print(f"Attempting to load model {model_name}")
        model = torch.load(f'{working_dirctory}\\{model_name}.model', weights_only=False)
        print(f"Model loaded")
    except Exception as e:
        print(e)
        model = DiffuseModel()
    
    #Move model to the selected device.
    model.to(device)
    #Log the model to the console.
    print(model)
    print(f"Done in {time.time()-section_timer} seconds\n")
    section_timer = time.time()
    
    #Load the Dataset and Datamodel.
    print(f"Loading dataset with bach size of {batch_size}")
    dataset = NoiseDataset(labelfile,datafile)
    dataloader = DataLoader(dataset, batch_size=batch_size)
    
    print(f"Done in {time.time()-section_timer} seconds\n")
    section_timer = time.time()
    
    loss_func = nn.MSELoss()#Define the loss function.
    
    optimizer = torch.optim.Adam(model.parameters(), learning_curve)#Create the optimizer.
    
    #Create variables to keep track of training time and the overall measured lowest loss.
    training_time = 0
    over_all_lowest_loss = math.inf
    
    #Execute training based on the given epoch count.
    for epoch in range(epoch_count):
        #############################################
        #Training.
        print(f"Starting epoch {epoch}")
        avg_loss = training(model,dataloader,loss_func,optimizer) #Train the model
        
        print(f"Done in {time.time()-section_timer} seconds\n")
        training_time += time.time()-section_timer
        section_timer = time.time()
        
        #############################################
        #Saving.
        
        print(f"Saving model {model_name}")
        torch.save(model, f'{working_dirctory}\\{model_name}.model') #Save model after each training cycle to protect against power outage.
        print(f"Done in {time.time()-section_timer} seconds\n")
        section_timer = time.time()
    
        #############################################
        #Testing.
        loss = testWithImage(model,dataset,random.randint(0,2**int(model_name.split("_")[1])-1),loss_func) #Create images after every cycle of training for visual statistics.
        over_all_lowest_loss = min(over_all_lowest_loss,loss)
        
        #############################################
        #Log values to console.
        
        print(f"\nAverage training loss: {avg_loss}")
        print(f"Evaluated loss: {loss}")
        
        #############################################
        #Save statistics.
        print(f"Saving starts of {model_name}")
        statFile = open(f"{working_dirctory}\\{model_name}.stat","a")
        statFile.write(f"{model_name};{start_timer};{avg_loss};{loss}\n")
        statFile.close()
        print(f"Done in {time.time()-section_timer} seconds\n")
        section_timer = time.time()
        
        #############################################
        #Generate image to mark keypoints
        if (epoch+1) % int(epoch_count/4) == 0:
            generateImage(model,int(len(dataset)/2),epoch+1)
    
    #Save model after training.
    print(f"Saving model {model_name}")
    torch.save(model, f'{working_dirctory}\\{model_name}.model')
    print(f"Done in {time.time()-section_timer} seconds\n")
    section_timer = time.time()
    
    #Save the parameters used during training.
    settingsFile = open(f"{working_dirctory}\\{model_name}.settings","w")
    settingsFile.write(f"Epoch count = {epoch_count}\n")
    settingsFile.write(f"Batch size = {batch_size}\n")
    settingsFile.write(f"Learning curve = {learning_curve}\n")
    settingsFile.write(f"Average training time = {training_time/epoch_count}\n")
    settingsFile.write(f"Lowest observed loss = {over_all_lowest_loss}\n")
    settingsFile.close()
        
    
    print(f"Finished in {time.time()-start_timer} seconds\n")
    
#Execute main function.
if __name__ == "__main__":
    main()