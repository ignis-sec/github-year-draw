from subprocess import call
import datetime 	
from PIL import Image
import numpy as np
import sys
import cv2
import math
if len(sys.argv)==1:
	print("Please run this script with a console command, passing a path to a monochrome bmp image.")
	exit()

def last_sunday(d): #get last sunday
	if d.weekday() == 6:
		return d
	else: 
		return d-datetime.timedelta(d.weekday()+1)

d = datetime.datetime.today()
last_Sunday = last_sunday(d) 
gitlog_start = last_Sunday - datetime.timedelta(364) #find the starting point of github yearly activity



p = cv2.imread(sys.argv[1],0)
#cv2.imshow('image',p)
p=p.transpose()
i=0
print(p)
with open("temp.txt", "a") as myfile:
	for x in range(0, 52):
		for y in range(0,7):
			if p[x][y]!=255:
				for n in range(0,math.floor((255-p[x][y])/10)): #commit according to color
					#print(n)
					myfile.write("1") #need changes for github commit
					myfile.flush()
					call('git commit -a -m "Commit"' + str(i) + ' --date="'+ str(gitlog_start+datetime.timedelta(x*7+y)) +'"') #commit command
					i=i+1
