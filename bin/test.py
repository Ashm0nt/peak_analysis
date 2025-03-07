#Lecture of a file with python
with open ("datos.txt", "r") as file:
    data = file.read()
    print (data)

#Using "for cycle" to read line per line of a file
with open ("datos.txt", "r") as file:
    for line in file:
        print (line)

#To avoid the line break, we use the "strip" method
with open ("datos.txt", "r") as file:
    for line in file:
        print (line.strip())