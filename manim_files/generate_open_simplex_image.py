from PIL import Image
import opensimplex
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-seed",type=int,help="Seed of the image to be made.")
args = parser.parse_args()

if not args.seed:
    print("A seed must be passed in using the -seed argument!")
    exit()

seed = args.seed

opensimplex.seed(seed)

image = Image.new("RGB",(64,64))
pixels = image.load()

for i in range(64):
    for j in range(64):
        data = opensimplex.noise2(i/10,j/10)
        data = data+1
        data = data/2
        data = int(data*255)
        pixels[i,j] = (data,data,data)
        
image.save("original.png","PNG")