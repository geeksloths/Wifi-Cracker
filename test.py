with open('text.txt','r') as file:
    lines = file.readlines() 
    for line in lines:
        string = line.replace(" ", "")
        string= string.replace("\n","")
        print(string)
        print(len(string))