import opensimplex
import argparse

"""
This program is used to generate the training data for the AI.
It accepts inputs:
    -start (Integer): The start of the seed.
    -range (Integer): The range of the seeds relatively to the seed start.
"""

if __name__ == '__main__':
    ##############################
    #Default parameters
    size = 64
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
    
def imageGenerator(seed_start,seed_range):
    """
    Generates a files containing OpenSimplex image training data.
    The file 'OpenSimplex.data' will contain the images for training sequentially in binary format, 8 byte per pixel.
    The file 'Opensimplex.label' will contain the labels of the images.
    @params
        seed_start (Integer): The start of the seed range.
        seed_range (Integer): The range of the seed range, relative to the start.
    
    @example
        imageGenerator(100,200) -> Generates images with seed range of 100 to 300.
    
    """
    #buffers for holding generated information
    labelBuffer = ""
    memoryBuffer = b""
    
    #open and create label and data files.
    labelfile = open(f"OpenSimplex.label","w")
    outfile = open(f"OpenSimplex.data","wb")
    
    #iterate through the seeds, set the seed if the generator, save the seed to the label file.
    for seed in range(seed_start,seed_start+seed_range):
        opensimplex.seed(seed)
        labelBuffer += f"{seed};"
        
        #Iterate over the 64 by 64 image range
        for x in range(size):
            for y in range(size):
                
                data = (opensimplex.noise2(x/10,y/10)+1)/2 #Convert the OpenSimplex range of [-1,1] to [0:1] to store.
                memoryBuffer+=data.tobytes() #Only store the luminescence of the image in float64, not RGB value.
        
        #append the image into the data file, and reset the buffer.
        outfile.write(memoryBuffer) 
        memoryBuffer = b""
        print(f"{seed}/{seed_range} seed={seed}")
    #save the data dile and, write and save the label file.
    outfile.close()
    labelBuffer = labelBuffer[0:-1]
    labelfile.write(labelBuffer)
    labelfile.close()
    
#Execution when __main__ is required to generate pydoc.
if __name__ == '__main__':
    imageGenerator(seed_start,seed_range)
