import os,argparse


argparse = argparse.ArgumentParser()
argparse.add_argument("-s",help="Use this flag to split the files",action="store_true")
argparse.add_argument("-a",help="Use this flag to assemble the files",action="store_true")
args = argparse.parse_args()

if not args.s and not args.a:
    print("Supply at least one of the flags")
    exit()

file_size_limit = 1024*1024*50
file_black_list = [".git","media","__pycache__","images"]
extension_black_list = ["png"]

def assemble_file(path,file):
    pass

def split_file(path):
    print("Splitting file at",path)
    original_file = open(path,"rb")
    original_file_size = os.stat(path).st_size

    

    file_id = 1 
    while True:
        file_slice = original_file.read(file_size_limit)
        if not file_slice:
            break
        file_out_name = f"{path}.part{file_id}" 
        print(f"\tSaving {file_out_name} ({((file_id-1)*file_size_limit+len(file_slice))/1024/1024}MB/{original_file_size/1024/1024}MB)")
        file_out = open(file_out_name,"wb")
        file_out.write(file_slice)
        file_out.close()
        file_id+=1

    original_file.close()

    

def findFiles(in_path):
    files = os.listdir(in_path)
    for file in files:
        if file in file_black_list:
            continue
        path = in_path+"\\"+file
        file_stat = os.stat(path)
        if file_stat.st_mode == 16895:
            findFiles(path)
        else:
            file_extension = file.split(".")[1]
            if file_extension in extension_black_list:
                continue
            if args.s and file_stat.st_size > file_size_limit:
                split_file(path)
            if args.a and file_extension == "part1":
                assemble_file(path,file)

findFiles(".")
