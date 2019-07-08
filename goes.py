import os
import urllib
import urllib2
import datetime
import time
import filecmp
from bs4 import BeautifulSoup

def getlink(website, searchstr):
	# Open up page and retrieve the part with the link
	try:
		html_page = urllib2.urlopen(website)
	except urllib2.URLError:
		print "Error opening " + website
		return 0, 0
	else:
		soup =  BeautifulSoup(html_page, "lxml")
		img = str(soup.select_one("a[href*=" + searchstr + "]"))
		count = 0
		# go through string and only keep link
		for c in img:
			if count < len(img) - 3 and img[count] == "h" and img[count+1] == "t":
				linkbeg = count
			if count > 3 and img[count] == "g" and img[count-1] == "p" and img[count-2] == "j":
				linkend = count + 1
			if count < len(img) - 3 and img[count] == " " and img[count-1] == "-" and img[count-2] == " " and img[count-3] == "r":
				namebeg = count + 1
			if count > 3 and img[count] == "C" and img[count-1] == "T" and img[count-2] == "U":
				nameend = count + 1
			count = count + 1
		link = img[linkbeg:linkend]
		name = img[namebeg:nameend]
		return link, name



# get first image
website_CONUS = "https://www.star.nesdis.noaa.gov/GOES/GOES16_CONUS.php"
searchstring_CONUS = "GOES16-ABI-CONUS-GEOCOLOR-5000x3000"
link_CONUS, name_CONUS = getlink(website_CONUS, searchstring_CONUS)
prev_img_CONUS = "CONUS/" + name_CONUS + ".jpg"
urllib.urlretrieve(link_CONUS, prev_img_CONUS)
print "New CONUS image: " + name_CONUS

website_FD = "https://www.star.nesdis.noaa.gov/GOES/GOES16_FullDisk.php"
searchstring_FD = "GOES16-ABI-FD-GEOCOLOR-5424x5424"
link_FD, name_FD = getlink(website_FD, searchstring_FD)
prev_img_FD = "FD/" + name_FD + ".jpg"
urllib.urlretrieve(link_FD, prev_img_FD)
print "New FD image: " + name_FD

time.sleep(120)

# loop to get images every 2 minutes
while 1:
	link_CONUS, name_CONUS = getlink(website_CONUS, searchstring_CONUS)
	link_FD, name_FD = getlink(website_FD, searchstring_FD)
	if (link_CONUS == 0 and name_CONUS == 0) or (link_FD == 0 and name_FD == 0):
		time.sleep(120)
		continue

	curr_img_CONUS = "CONUS/" + name_CONUS + ".jpg"
	curr_img_FD = "FD/" + name_FD + ".jpg"

	if curr_img_CONUS != prev_img_CONUS:
		urllib.urlretrieve(link_CONUS, curr_img_CONUS)
		print "New CONUS image: " + name_CONUS
		prev_img_CONUS = curr_img_CONUS

	if curr_img_FD != prev_img_FD:
		urllib.urlretrieve(link_FD, curr_img_FD)
		print "New FD image: " + name_FD
		prev_img_FD = curr_img_FD

	time.sleep(120)