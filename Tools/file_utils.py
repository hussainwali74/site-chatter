def writeToFile(file_path, data):
    "write data to file line by line"
    with open(file_path,'w') as ff:
        for c in data:
            ff.write(c+'\n')
