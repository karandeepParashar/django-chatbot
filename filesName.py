import glob
files = glob.glob("Images-DB/*")
for file in files:
    print(file)
    file = glob.glob("Images-DB/"+file+"/*")
    for f in file:
        print(f)