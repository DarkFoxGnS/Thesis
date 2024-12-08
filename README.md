# Theis project: From Determinism to Adaptability: Evaluation of Artificial Intelligence Performance in Pseudo-Random Generation
By Tibor Péter Szabó  
Thesis for IU University of Applied Sciences.

## Table of contents
[Dependencies](#dependencies)  
[OpenSimplex Noise](#opensimplex-noise)  
[Worley Noise](#worley-noise)  
[Models](#models)  
[Artificial Intelligence Training](#artificial-intelligence-training)  
[Artificial Intelligence Testing](#artificial-intelligence-testing)  


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
Given the input  
```
OpenSimplex.py -start 100 -range 200  
```
images with seed ranging from **100** to **300** will be generated.
### Output
These files will be generated into the same directory as [OpenSimpex.py](./OpenSimplex.py).  
`OpenSimpex.data` contains the luminescence from 0 (`#000000`) to 1 (`#FFFFFF`) of the images in a binary format with each value being a 64-bit float written sequentially, where each image consists of 262,144 bits or 32 KB.  
`OpenSimpex.label` contains the respective labels (seeds) of the images written sequentially separated via `;`.

## Worley Noise
The training data and the labels for the AI that uses Worley can be generated by executing the [Worley.py](./Worley.py) 
### Arguments
`-seed <SEED>` to input the start of the seed.  
`-range <RANGE>` for the range of the seed relative to the start.  
### Example
Given the input  
```
Worley.py -start 100 -range 200  
```
images with seed ranging from **100** to **300** will be generated.
### Output
These files will be generated into the same directory as [Worley.py](./Worley.py).  
`Worley.data` contains the luminescence from 0 (`#000000`) to 1 (`#FFFFFF`) of the images in a binary format with each value being a 64-bit float written sequentially, where each image consists of 262,144 bits or 32 KB.  
`Worley.label` contains the respective labels (seeds) of the images written sequentially separated via `;`.

## Models
The models included in the repository are stored in the folders named in the scheme `<NOISE>_model_<SEED_SIZE>_<TYPE>` where  
`NOISE` describes the type of the noise which was used to train the model, it can be either `w` for Worley or `os` for OpenSimpex.  
`SEED_SIZE` describes the ammount of bits used for the seeds.  
`TYPE` describes the type of model, it can be either `nn` for Neural Network or `gan` for Generative Adversarial Network.  
For example the folder `w_model_8_nn` contains a **Neural Network** model trained on **Worley** noise with the **8**-bit seed range of 0 to 2<sup>8</sup>=255.  
  
Inside the directory of the model, the following can be found:  
`images` contains the images generated during the training to keep evidence of evolution.  
`model_<SEED_SIZE>.data` contains the images used to train the model, due to size limitations, may be trimmed to `.parts`.  
`model_<SEED_SIZE>.label` contains the labels used to train the model.  
`model_<SEED_SIZE>.model` the actual model containing the shape and the weights of the model.  
`model_<SEED_SIZE>.stat`  contains the statistics measured during the training of the model.
`model_<SEED_SIZE>.settings` contains the parameters of the training.  

### OpenSimplex models
[Neural Network Model with  8-bit seed](./os_model_8_nn/)  
[Neural Network Model with 10-bit seed](./os_model_10_nn/)  
[Neural Network Model with 12-bit seed](./os_model_12_nn/)  
[Neural Network Model with 14-bit seed](./os_model_14_nn/)  
[Neural Network Model with 16-bit seed](./os_model_16_nn/)  
<break></break>

[Generative Adversarial Network Model with  8-bit seed](./os_model_8_gan/)  
[Generative Adversarial Network Model with 10-bit seed](./os_model_10_gan/)  
[Generative Adversarial Network Model with 12-bit seed](./os_model_12_gan/)  
[Generative Adversarial Network Model with 14-bit seed](./os_model_14_gan/)  
[Generative Adversarial Network Model with 16-bit seed](./os_model_16_gan/)

### Worley models
[Neural Network Model with  8-bit seed](./w_model_8_nn/)  
[Neural Network Model with 10-bit seed](./w_model_10_nn/)  
[Neural Network Model with 12-bit seed](./w_model_12_nn/)  
[Neural Network Model with 14-bit seed](./w_model_14_nn/)  
[Neural Network Model with 16-bit seed](./w_model_16_nn/)  
<break></break>

[Generative Adversarial Network Model with  8-bit seed](./w_model_8_gan/)  
[Generative Adversarial Network Model with 10-bit seed](./w_model_10_gan/)  
[Generative Adversarial Network Model with 12-bit seed](./w_model_12_gan/)  
[Generative Adversarial Network Model with 14-bit seed](./w_model_14_gan/)  
[Generative Adversarial Network Model with 16-bit seed](./w_model_16_gan/)

## Artificial Intelligence Training
The training of the Artificial Intelligence model can be done using the [AI_nn.py](./AI_nn.py) and [AI_gan.py](./AI_gan.py).
### Arguments
`-model`: The name of the model, it relates to the name of the .label and the .data file. Default is `model`.  
`-dir`: The name of the working directory where the model, label and data file to be located. Default is `.`.  
`-epoch`: The ammount of times the data set is trained on. Default is `200`.  
`-batch`: The ammount of data that is passed into the model at the same time. Default is `16`.  
`-lr`: The learning rate of the model. Default is `0.001`.  
`-device`: The device used to train the model on. Default is `cuda`.
### Example
The code  
```
AI_nn.py -dir os_model_8_nn -model model_8 -epoch 200 -batch 16 -lr 0.001 -device cuda  
```
starts the training of a model on the data **os_model_8_nn**/**model_8**.data and on the label **os_model_8_nn**/**model_8**.label with a epoch of **200**, a batch size of **16** and a learning rate of **0.001** on the **cuda** device (NVIDIA Graphics Processing Unit).
### Output
`<DIRECTORY>/images/<START_TIME>_<CURRENT_TIME>_<MODEL_NAME>_<SEED>_<original|generated>.png` contains the images generated during the training to keep evidence of evolution.  
`<DIRECTORY>/<MODEL_NAME>.model` the actual model containing the shape and the weights of the model.  
`<DIRECTORY>/<MODEL_NAME>.stat`  contains the statistics measured during the training of the model.  
`<DIRECTORY>/<MODEL_NAME>.settings` contains the parameters of the training.  
where
`<DIRECTORY>` is the active working directory, passed in via `-dir`.  
`<MODEL_NAME>` is the name of the model, passed in via `-model`.  
`<START_TIME>` is the seconds from epoch when the training was started.  
`<CURRENT_TIME>` is the seconds from epoch when generating the image.  
`<SEED>` is the seed used to generate the images.  
`<original|generated>` it can be either `original` when it's taken from the original sample or `generated` when it's generated by the model. They are always created in pair.  

## Artificial Intelligence Testing
TO DO