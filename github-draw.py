from subprocess import call
import datetime 	
from PIL import Image
import numpy as np
import sys

import math
import os

fail="[\033[91m+\033[0m]"
succ="[\033[92m+\033[0m]"
warn="[\033[93m+\033[0m]"
info="[\033[94m+\033[0m]"

if len(sys.argv)==1:
	print("Example Usage:")
	print(f"python3 {os.path.basename(__file__)} <filename> <intensity>?")
	print("Higher intensity will take longer to process, but will look better. Default is 20. Max is 255")
	exit()


def last_sunday(d): #get last sunday
	if d.weekday() == 6:
		return d
	else: 
		return d-datetime.timedelta(d.weekday()+1)

#find the starting point of github yearly activity
d = datetime.datetime.today()
last_Sunday = last_sunday(d) 
gitlog_start = last_Sunday - datetime.timedelta(364) 

print(f"{info} Opening image {sys.argv[1]}")
im = Image.open(sys.argv[1])

print(f"{info} Image size is {im.size[0]}x{im.size[1]}")
i=0
if(im.size[0]!=52 or im.size[1]!=7):
	print(f"{warn} This script requires a 52*7 image to work with. Do you wish to resize? (Y/N)")
	confirm = input(">>>")
	if(confirm=='Y' or confirm=='y'):
		print(f"{info} Resizing image.")
		im = im.resize((52, 7))
		print(f"New image size {im.size[0]}x{im.size[1]}")
	else:
		print(f"{fail} Quitting.")
		exit(1)

exit()
with open("temp.txt", "a") as myfile:
	for x in range(0, 52):
		for y in range(0,7):
			if im[x][y]!=255:
				for n in range(0,math.floor((255-p[x][y])/10)): #commit according to color
					#print(n)
					myfile.write("1") #need changes for github commit
					myfile.flush()
					#call('git commit -a -m "Commit"' + str(i) + ' --date="'+ str(gitlog_start+datetime.timedelta(x*7+y)) +'"') #commit command
					i=i+1
