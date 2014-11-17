import os, subprocess, time, sys, bluetooth

print("Tom's shitty programming skills proudly present...")
print("The autobox")



running = 1
while running:
	devnull = open('/dev/null', 'wb')


	i = 0 # initialising the iterative counter

	T_Wil = "192.168.20.110"
	JC = "192.168.20.106" # IP globals
	lstip = [T_Wil, JC]
	Peeps = ['T_Wil']# Global Names
	bt = ["F0:6B:CA:AC:EB:06", "34:C0:59:B5:9C:94"]# GLobal BT addresses

	print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())

	def checking(pingip):#Check pingip for users ip. If not found scan BT
	
		if pingip == 0:
		
			print Peeps[i], "; in"
	
		elif pingip == 1:
		
			result = bluetooth.lookup_name(bt[i], timeout=4)
		
			if (result != None): 
				print Peeps[i], ": in"
		
			else:
				print Peeps[i], ": out"
		return;
	
	while i < len(Peeps):
		pingip = subprocess.call(['ping', '-w', '1', '--', lstip[i]], 
	
		stdout = devnull)
	
		checking(pingip)
		i += 1
	
	
	
	




	


	
			
		
		
