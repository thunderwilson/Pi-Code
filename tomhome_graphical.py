import os, subprocess, time, sys, bluetooth, csv




running = 1

devnull = open('/dev/null', 'wb')


i = 0 # initialising the iterative counter
people = dict()
people['T_Wil'] = ("192.168.20.110", "F0:6B:CA:AC:EB:06", "out")





##def query(people):
	


		
def writer(person, state):
	
	with open("./%s" % person, "a") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow([state, time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())])
	
			


def checking(people):#Check pingip for users ip. If not found scan BT
	
	for person in people:
		
		
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

	

	



	


	
			
		
		


