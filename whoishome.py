import os, subprocess, time, sys, bluetooth

running = 1

devnull = open('/dev/null', 'wb')

T_Wil = "192.168.20.101"




i=0

lstip = [T_Wil]

lstname = ["T_Wil"]

bt = ["F0:6B:CA:AC:EB:06"]

print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())

print "<br />\n" #new line for php web

print "<br />\n" #new line for php web

def printme(pingip):

# Check WIFI IP if IN

	if pingip == 0:

		print lstname[i], ": in"

	print "<br />\n" #new line for php web

# Check BlueTooth if NO IP is found

	if pingip == 1:

		result = bluetooth.lookup_name(bt[i], timeout=4)

		if (result != None): # If Bluetooth is found, IN

			print lstname[i], ": in"

			print "<br />\n" #new line for php web

	else: # If Bluetooth is NOT found, OUT

		print lstname[i], ": out"

	print "<br />\n" #new line for php web

	#time.sleep(2)

	return;

while i < len(lstip):

	pingip = subprocess.call(['ping', '-w', '1', '--', lstip[i]],

	stdout = devnull)

	printme(pingip);

	i+=1


