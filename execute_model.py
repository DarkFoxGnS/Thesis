import argparse

parser = argparse.ArgumentParser()
parser.add_argument("model")
parser.add_argument("seed",type=int)
args = parser.parse_args()

import torch
def save_image(image_tensor):
    from PIL import Image
    out_image = Image.new("RGB",(64,64))
    pixels = out_image.load()
    image_tensor = image_tensor.to("cpu")
    for x in range(64):
        for y in range(64):
            data = int(image_tensor.data[x][y]*255)
            pixels[x,y] = (data,data,data)

    out_image.save(f"media\\model_image_tests\\{args.model.split("\\")[0]}_{args.seed}.png","PNG")
    print("Image written to:",f"media\\model_image_tests\\{args.model.split("\\")[0]}_{args.seed}.png")

def load_model(model):
    model.load_state_dict(torch.load(args.model,weights_only=False))
    print("Using",model)

def AI_nn(seed_tensor):
    import AI_nn
    model = AI_nn.NeuralNetworkModel()
    load_model(model)
    output = model(seed_tensor)
    output = output.view(64,64)
    save_image(output)

def AI_ced(seed_tensor):
    import AI_ced
    model = AI_ced.ConditionalEncoderDecoderModel()
    load_model(model)
    
    image_tensor = torch.nn.Sigmoid()(torch.randn(64,64)).view(-1,64,64)
    for i in range(100):
        output = model(image_tensor,seed_tensor)
        image = output.data.view(-1,64,64)

    output = output.view(64,64)
    save_image(output)


def AI_hy(seed_tensor):
    import AI_hy
    model = AI_hy.HybridModel()
    load_model(model)
    
    output = model(seed_tensor)

    output = output.view(64,64)
    save_image(output)
def main():
    execute_model = {
            "nn":AI_nn,
            "ced":AI_ced,
            "hy":AI_hy
            }
    
    model_type = args.model.split(".")[1]
    seed_tensor = torch.Tensor([float(x) for x in format(args.seed,"016b")]).view(-1,16)
    execute_model[model_type](seed_tensor)
        

if __name__ == "__main__":
    main()
