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
The training data and the labels for the AI that uses OpenSimplex can be generated by executing the [OpenSimpex.py] (OpenSimpex.py)

### Arguments
`-seed <SEED>` to input the start of the seed.  
`-range <RANGE>` for the range of the seed relative to the start.  

### Output
The program will output the files `OpenSimpex.data` and  `OpenSimpex.label` in the same directory.

## Worley Noise
The training data and the labels for the AI that uses Worley can be generated by executing the [Worley.py] (Worley.py)

### Arguments
`-seed <SEED>` to input the start of the seed.  
`-range <RANGE>` for the range of the seed relative to the start.  

### Output
The program will output the files `Worley.data` and  `Worley.label` in the same directory.

## AI
