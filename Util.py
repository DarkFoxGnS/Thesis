
"""
The module is meant to be imported into the python REPL enviroment as a Utility framework.
"""
def generateOpenSimplex(seed):
    """
    Generates an Open Simplex image at seed.
    @params:
        seed (int): Seed of the image
    """
    from PIL import Image
    import opensimplex
    
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

def generateWorley(seed):
    """
    Generates a Worley image at seed.
    @params:
        seed (int): Seed of the image
    """
    from PIL import Image
    import pythonworley
    
    gridsize = 4
    shape = (gridsize,gridsize)
    dens = 16
    size = gridsize*dens
    
    image = Image.new("RGB",(64,64))
    pixels = image.load()
    
    w, c = pythonworley.worley(shape, dens=dens, seed=seed)        
    w = w[0]

    for x in range(size):
            for y in range(size):
                data = w[x][y]
                data = int(data*255)
                pixels[x,y] = (data,data,data)
                
    image.save("original.png","PNG")
    
class StatFile():
    """
    This class is used to easily observe the '.stat' statistic file generated by the model after training.
    """
    data = []
    def __init__(self,file):
        """
        Creates the object.
        @params:
            file (string): The path to the .stat file to be opened.
        @returns:
            StatFile object.
        """
        data_file = open(file,"r")
        self.data = data_file.read()
        self.data = self.data.split("\n")
        data_file.close()
    
    def getAvg(self,id):
        """
        Returns the average value at the given id.
        @params.
            id (Integer): The id of the value with 1 being the first.
        @returns:
            value (Float): The average value at the given id.
        """
        return float(self.data[id-1].split(";")[2])
        
    def getPerImage(self,id):
        """
        Returns the per image value at the given id.
        @params.
            id (Integer): The id of the value with 1 being the first.
        @returns:
            value (Float): The peper image value at the given id.
        """
        return float(self.data[id-1].split(";")[3])
        
