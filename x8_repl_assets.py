import os
import shutil

for file in os.listdir('.'):
    split = file.split("_")
    split[0] = split[0].replace('11', '02')
    filename = "_".join(split)
    try:
        shutil.move(file, filename)
        print("Moved ", file, "to ", filename)
    except:
        print("Couldn't move", file, "to", filename)