filename = "./_annotations.txt"
lines = []
with open(filename, 'r') as filehandle:
    for line in filehandle:
        lines.append(line)

for i in range(0,len(lines)):
	data = lines[i]
	contents = data.split()
	filename = "./input/ground-truth/"+contents[0]+".txt"
	f = open(filename,"w+")
	for j in range(1, len(contents)):
		d1 = contents[j]
		d2 = d1.split(",")
		left = d2[0]
		top = d2[1]
		right = d2[2]
		bottom = d2[3]
		class_name = d2[4]
		if class_name == "0":
			print("in")
			class_name = "concussion"
		
			result = class_name+" "+left+" "+top+" "+right+" "+bottom
			f.write(result+"\n")