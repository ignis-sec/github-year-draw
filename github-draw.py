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


def waitConfirm():
	c = input(">>> ")
	if(c=='Y' or c=='y'):
		return True
	return False

def monochromize(p):
	try:
		return int((p[0]+p[1]+p[2])//3)
	except:
		return int(p)

def preview():
	print(f"{warn} Preview?")
	if(waitConfirm()):
		from sty import fg, bg, ef, rs, Style, RgbFg,RgbBg

		for y in range(im.size[1]):
			for x in range(im.size[0]):
				#print(f"{x=}{y=}")
				c = monochromize(pix[y][x])

				c = bg(c,c,c)
				print(c + " ", end='')
			print(bg.rs)

#find the starting point of github yearly activity
d = datetime.datetime.today()
last_Sunday = last_sunday(d) 
gitlog_start = last_Sunday - datetime.timedelta(364) 

print(f"{info} Opening image {sys.argv[1]}")
im = Image.open(sys.argv[1])
pix = 0
print(f"{info} Image size is {im.size[0]}x{im.size[1]}")
i=0
if(im.size[0]!=52 or im.size[1]!=7):
	print(f"{warn} This script requires a 52*7 image to work with. Do you wish to resize? (Y/N)")
	if(waitConfirm()):
		print(f"{info} Resizing image.")
		im = im.resize((52, 7))
		pix = np.asarray(im)
		print(f"New image size {im.size[0]}x{im.size[1]}")
		preview()
	else:
		print(f"{fail} Quitting.")
		exit(1)
else:
	pix = np.asarray(im)
	preview()
exit()

i=0
intensity=20
if(len(sys.argv)==3):
	intensity=sys.argv[2]

print(f"{info} Intensity set to {intensity}")
with open("temp.txt", "a") as myfile:
	for x in range(0, 52):
		for y in range(0,7):
			if im[y][x]!=255:#dont commit on empty days
				for n in range(0,math.floor((255-p[x][y])/10)): #commit according to color
					#print(n)
					myfile.write("1") #need changes for github commit to go through
					myfile.flush()
					#call('git commit -a -m "Commit"' + str(i) + ' --date="'+ str(gitlog_start+datetime.timedelta(x*7+y)) +'"') 
					i=i+1
