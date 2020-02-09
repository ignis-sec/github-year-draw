from subprocess import call
import datetime 	
from PIL import Image
import numpy as np
import sys
from sty import fg, bg, ef, rs, Style, RgbFg,RgbBg

from html.parser import HTMLParser
import math
import os

fail="[\033[91m+\033[0m]"
succ="[\033[92m+\033[0m]"
warn="[\033[93m+\033[0m]"
info="[\033[94m+\033[0m]"


def last_sunday(d): #get last sunday
	if d.weekday() == 6:
		return d
	else: 
		return d-datetime.timedelta(d.weekday()+1)


def waitConfirm():
	c = input(">>> ")
	if(c=='Y' or c=='y' or c=='Yes' or c=='yes'):
		return True
	return False

#generate a gray from pixel, ignore if image is already grayscale
def monochromize(p):
	try:
		return int((p[0]+p[1]+p[2])//3)
	except:
		return int(p)

def preview():
	print(f"{warn} Preview?")
	if(waitConfirm()):
		for y in range(im.size[1]):
			for x in range(im.size[0]):
				#print(f"{x=}{y=}")
				c = monochromize(pix[y][x])

				#double scale to introduce the flat lose.
				c = scaleIntensity(c,255,intensity)
				c = scaleIntensity(c,intensity,255)
				c = monochromize(pix[y][x])
				c = bg(c,c,c)
				print(c + " ", end='')
			print(bg.rs)

#scale 0-x pixel value to 0-y
def scaleIntensity(c,currentIntensity,_intensity):
	r = int((currentIntensity-c)/currentIntensity*_intensity)
	#Ceil non-0 ones who are 0 by mistake
	if(c!=currentIntensity and r==_intensity):
		r+=1
	return r

oldCommits = np.zeros((53,7))


#used for github profile commit summary parsing
class MyHTMLParser(HTMLParser):

	def __init__(self):
		self.rectCounter=0
		self.maxCommits=0
		super().__init__()
	def handle_starttag(self, tag, attrs):
		if(tag!="rect"):
			return
		c = 0
		for attr in attrs:
			if(attr[0]=="data-count"):
				c=int(attr[1])
				break
		if(c>self.maxCommits):self.maxCommits=c
		oldCommits[self.rectCounter//7][self.rectCounter%7] = c
		self.rectCounter+=1

parser = MyHTMLParser()




if len(sys.argv)==1:
	print("Example Usage:")
	print(f"python3 {os.path.basename(__file__)} <filename> <intensity>?")
	print("Higher intensity will take longer to process, but will look better. Default is 30. Max is 255")
	exit()

intensity=30
if(len(sys.argv)==3):
	intensity=int(sys.argv[2])

print(f"{succ} Intensity set to {intensity}")

print(f"{warn} Do you want to give a github username, so this script can see your past commit overview and adjust on that?")
print(f"{warn} (Requires requests library)")
if(waitConfirm()):
	import requests
	username = input("Username:>>> ")
	r = requests.get("https://github.com/" + username)
	parser.feed(r.text)

	for y in range(7):
		for x in range(52):
			#print(oldCommits[x][y], end=', ')
			c=scaleIntensity(oldCommits[x][y],parser.maxCommits,255)
			c = bg(c,c,c)
			print(c + " ", end='')
		print(bg.rs)
	print(f"{warn} Is this your history?")
	if(not waitConfirm()):
		print(f"{fail} Either wrong username, or something went wrong.")
		exit()

	print(f"{info} your maximum number of commits on a day is {parser.maxCommits}")
	print(f"{warn} Set intensity to {parser.maxCommits}?")
	if(waitConfirm()):
		intensity=parser.maxCommits
		print(f"{succ} Intensity is now at {intensity}")
	


#find the starting point of github yearly activity
d = datetime.datetime.today()
last_Sunday = last_sunday(d) 
gitlog_start = last_Sunday - datetime.timedelta(364) 

print(f"{info} Opening image {sys.argv[1]}")
im = Image.open(sys.argv[1])
pix = 0
print(f"{succ} Image size is {im.size[0]}x{im.size[1]}")
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

print(f"{warn} Continue with this?")
if(not waitConfirm()):
	print(f"{fail} Ok.")
	exit(0)


print(f"{succ} Setting up git repo in git-art")
try:
	os.mkdir("git-art")
except:
	print(f"{warn} Folder exists, but continuing.")
try:
	os.chdir("git-art")
except:
	print(f"{fail} Something went wrong, not gonna risk it")
	exit(1)
os.system("git init")

i=0

with open("temp.txt", "a") as myfile:
	os.system("git add .")
	for x in range(0, 52):
		for y in range(0,7):
			c=int(monochromize(pix[y][x]))
			c=scaleIntensity(c,255,intensity)
			if c!=255:#dont commit on empty days

				#Clear collisions
				c = c - int(oldCommits[x][y])

				if(c<0):
    				#Image will have an artifact, nothing we can do without adjusting the intensity
					#There are more commits on the day than we meant to commit. Cant do minus commits on that day
					print(f"{info} Detected a bad artifact.")
					continue
				print(c, end=', ')
				for n in range(c): 
					#commit according to goal color
					print(scaleIntensity(c,255,intensity), end=', ')

					#need changes for github commit to go through
					myfile.write("1") 
					myfile.flush()
					call('git commit -a -m "Commit"' + str(i) + ' --date="'+ str(gitlog_start+datetime.timedelta(x*7+y)) +'"') 
					i=i+1
			else:
				print('0', end=', ')
				pass		
		print()
