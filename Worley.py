if __name__ == "__main__":
    from PIL import Image
    from pythonworley import worley
    import argparse
    ##############################
    #Parameters
    gridsize = 4
    shape = (gridsize,gridsize) #This is the ammount of grids on the image.
    dens = 16 #Density is the ammount of pixels per grids.
    size = gridsize*dens  #The size of the image is given the shape*density = 4*16=64 resulting in a 64x64 image.
    seed_start = 0
    seed_range = 2**8
    ##############################
   
    parser = argparse.ArgumentParser()
    parser.add_argument("-start",type=int,help="Start of the seed. Default is 0")
    parser.add_argument("-range",type=int,help="Range of the seed. Default is 255")
    args = parser.parse_args()

    if args.start:
        seed_start = args.start
    if args.range:
        seed_range = args.range
        

def imageGenerator(seedStart,seedRange):
    """
    Generates a files containing Worley image training data.
    The file 'Worley.data' will contain the images for training sequentially in binary format, 8 byte per pixel.
    The file 'Worley.label' will contain the labels of the images.
    @params
        seed_start (Integer): The start of the seed range.
        seed_range (Integer): The range of the seed range, relative to the start.
    
    @example
        imageGenerator(100,200) -> Generates images with seed range of 100 to 300.
    
    """
    labelfile = open(f"Worley.label","w")
    outfile = open(f"Worley.data","wb")
    dataBuffer = b''
    labelBuffer = ""
    
    for seed in range(seedStart,seedStart+seedRange):
        #Generate noise and the centers as biproduct.
        w, c = worley(shape, dens=dens, seed=seed)        
        w = w[0]#Create the commonly known woley noise by selecting the 0th array where the 0th point is the closest.
        labelBuffer+=f"{seed};"
        for x in range(size):
            for y in range(size):
                data = w[x][y]
                dataBuffer += data.tobytes()
        
        #append the image into the data file, and reset the buffer.
        outfile.write(dataBuffer) 
        dataBuffer = b''
        print(f"{seed}/{seedRange} seed={seed}")
    #save the data dile and, write and save the label file.
    outfile.close()
    labelBuffer = labelBuffer[0:-1]
    labelfile.write(labelBuffer)
    labelfile.close()
    
if __name__ == "__main__":
    imageGenerator(seed_start,seed_range)