import os, subprocess, time, sys, bluetooth, csv




running = 1

devnull = open('/dev/null', 'wb')


i = 0 # initialising the iterative counter
people = dict()
people['T_Wil'] = ("192.168.20.110", "F0:6B:CA:AC:EB:06", "out")
#people['Cunt1'] = ("192.168.20.110", "F0:6B:CA:AC:EB:16", "out")
#people['Cunt2'] = ("192.168.20.102", "F0:6B:CA:AC:EB:02", "out") # IP globals




def query(people):
	while running:
		checking(people)
		person = raw_input("Query a name? ")
		template = "{0:20}|{1:20}|{2:20}|{3:20}" # column widths: 8, 10, 15, 7, 10
		template2 = "{0:20} {1:20} {2:20} {3:20}" # column widths: 8, 10, 15, 7, 10
		print template.format("NAME", "IP", "BT", "SATUS", end="")
	
		if person in people:
		

			print template2.format(person, people[person][0], people[person][1], people[person][2])


		
def writer(person, state):
	
	with open("./%s" % person, "a") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow([state, time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())])
	
			


def checking(people):#Check pingip for users ip. If not found scan BT
	
	for person in people:
		
		pingip = subprocess.call(['ping', '-w', '1', '--', people[person][0]], 
	
	stdout = devnull)
		
		if pingip == 0:
			
			if people[person][2] != "in":
				people[person] = (people[person][0], people[person][1], "in")
				darl = person + ".csv"
				writer(darl, "in")
				
				
				
			
	
		elif pingip == 1:
		
			result = bluetooth.lookup_name(people[person][1], timeout=4)
		
			if (result != None):
			 
				if people[person][2] != "in":
					people[person] = (people[person][0], people[person][1], "in")
					darl = person + ".csv"
					writer(darl, "in")
				
		
			else:
				if people[person][2] != "out":
					people[person] = (people[person][0], people[person][1], "out")
					darl = person + ".csv"
					writer(darl, "out")
				
	return people


	
while running:
	
	
	checking(people)

	

	



	


	
			
		
		


