import opensimplex
import argparse

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
    labelBuffer = ""
    memoryBuffer = b""
    
    labelfile = open(f"label.label","w")
    outfile = open(f"training.data","wb")
    for seed in range(seed_start,seed_start+seed_range):
        opensimplex.seed(seed)
        labelBuffer += f"{seed};"
        
        for x in range(size):
            for y in range(size):
                data = (opensimplex.noise2(x/10,y/10)+1)/2
                memoryBuffer+=data.tobytes()
        
        outfile.write(memoryBuffer)
        memoryBuffer = b""
        print(f"{seed}/{seed_range} seed={seed}")
    outfile.close()
    labelBuffer = labelBuffer[0:-1]
    labelfile.write(labelBuffer)
    labelfile.close()
    
    
imageGenerator(seed_start,seed_range)