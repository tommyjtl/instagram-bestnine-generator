from PIL import Image
#Open image using Image module

min_size = 0
all_size = []

for i in range(1,9,1):
	im = Image.open("tommyjtl/"+str(i)+".jpg")
	all_size.append(im.size)
	print(im.size)

sort_out = sorted(all_size, key=lambda x: int(x[1]), reverse=True)

print(sort_out)
min_size = sort_out[-1][1]
print(min_size)

#Show actual Image
#im.show()