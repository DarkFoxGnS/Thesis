import os,argparse

if __name__ == "__main__":
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

def assemble_file(path):
    """
    Assembles the file from .part<id> files.
    @params:
        path (string): The path of the first .part file
    @example:
        assemble_file('.\\model_8.nn.part1') will result in an assembled file model_8.nn.
    """
    file_name = ".".join(path.split(".")[0:-1])
    print(f"Assembling the file {file_name}")
    out_file = open(f"{file_name}_ass","wb")
    file_id = 1
    
    while True:
        try:
            in_file_name = f"{file_name}.part{file_id}"
            print(f"\tReading {in_file_name}")
            in_file = open(in_file_name,"rb")
            data = in_file.read()
            out_file.write(data)
            in_file.close()
        except:
            break
    
        file_id+=1
    out_file.close()

def split_file(path):
    """
    Splits a file into parts matching the <file_size_limit> defined above.
    @params:
        path (string): The path to the file to be split.
    @example:
        split_file('.\\model_8.nn') will result in a set of file ending with .part<id>, like model_8.nn.part1.
    """
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
    """
    Recursively finds all files that are larger than the <file_size_limit>.
    @params:
        in_path (string): The main directory where to search for the files.
    """
    files = os.listdir(in_path)
    for file in files:
        if file in file_black_list:
            continue
        path = in_path+"\\"+file
        file_stat = os.stat(path)
        if file_stat.st_mode == 16895:
            findFiles(path)
        else:
            if file.split(".")[-1] in extension_black_list:
                continue

            if args.s and file_stat.st_size > file_size_limit:
                split_file(path)

            if args.a and file.split(".")[-1] == "part1":
                assemble_file(path)

if __name__ == "__main__":
    findFiles(".")
