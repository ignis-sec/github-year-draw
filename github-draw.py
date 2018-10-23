from subprocess import call
import datetime 	
from PIL import Image
import numpy as np
import sys

def last_sunday(d): #get last sunday
	if d.weekday() == 6:
		return d
	else: 
		return d-datetime.timedelta(d.weekday()+1)

d = datetime.datetime.today()
last_Sunday = last_sunday(d) 
gitlog_start = last_Sunday - datetime.timedelta(364) #find the starting point of github yearly activity



im = Image.open(str(sys.argv[1])) #convert monochrome bpm to bool array
p = np.array(im)
p = p.transpose()
i=0

with open("temp.txt", "a") as myfile:
	for x in range(0, 52):
		for y in range(0,7):
			for n in range(0,15): #commit 15 times, we want a dark color
				if p[x][y]==False: ##only on black pixels
					myfile.write("1") #need changes for github commit
					myfile.flush()
					call('git commit -a -m "Commit"' + str(i) + ' --date="'+ str(gitlog_start+datetime.timedelta(x*7+y)) +'"') #commit command
					i=i+1
