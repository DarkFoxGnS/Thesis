# Theis project: From Determinism to Adaptability: Evaluation of Artificial Intelligence Performance in Pseudo-Random Generation
By Tibor Péter Szabó
Thesis for IU University of Applied Sciences

## Table of contents
[Dependencies](#dependencies)  
[OpenSimplex Noise](#opensimplex-noise)  
[Worley Noise](#worley-noise)  

## Dependencies
For the project to fully function, the following packages are required.  
[PIL](https://pypi.org/project/pillow/)  
[pythonworley](https://pypi.org/project/pythonworley/)  
[opensimplex](https://pypi.org/project/opensimplex/)  
[torch](https://pytorch.org/)  

## OpenSimplex Noise
The training data and the labels for the AI that uses OpenSimplex can be generated by executing the [OpenSimpex.py](./OpenSimplex.py)

### Arguments
`-seed <SEED>` to input the start of the seed.  
`-range <RANGE>` for the range of the seed relative to the start.  

### Example
Given the input `OpenSimplex.py -start 100 -range 200` images with seed ranging from 100 to 300 will be generated.

### Output
These files will be generated into the same directory as [OpenSimpex.py](./OpenSimplex.py).  
`OpenSimpex.data` contains the luminescence of the images in a binary format with each value being a 64-bit float written sequentially, where each image consists of 262,144 bits or 32 KB.  
`OpenSimpex.label` contains the respective labels (seeds) of the images written sequentially separated via `;`.

## Worley Noise
The training data and the labels for the AI that uses Worley can be generated by executing the [Worley.py](./Worley.py) 

### Arguments
`-seed <SEED>` to input the start of the seed.  
`-range <RANGE>` for the range of the seed relative to the start.  

### Example
Given the input `Worley.py -start 100 -range 200` images with seed ranging from 100 to 300 will be generated.

### Output
These files will be generated into the same directory as [Worley.py](./Worley.py).  
`Worley.data` contains the luminescence of the images in a binary format with each value being a 64-bit float written sequentially, where each image consists of 262,144 bits or 32 KB.  
`Worley.label` contains the respective labels (seeds) of the images written sequentially separated via `;`.

## AI
AI can be trained by executing

## Models
The models included in the repository are stored in the folders named in the scheme `<TYPE>_model_<SEED_SIZE>` where  
`TYPE` describes the type of the model, it can be either `w` for Worley or `os` for OpenSimpex.  
`SEED_SIZE` describes the ammount of bits used for the seeds.  
For example the folder `w_model_8` contains a model trained on **Worley** noise with the seed range of 2<sup>**8**</sup>=255.
