##Draft code for basic smart badge implementation.
##RasPi local code
##Author: T D G Wilson
##Date: 18/11/2014



import os, time, subprocess, time, sys, bluetooth, csv




	
running = 1

devnull = open('/dev/null', 'wb')

i = 0

class Staff:
	
	def __init__(self, name, bt, start_time, end_time, status):
		
		self.name = name 
		self.bt = bt
		self.start_time = start_time
		self.end_time = end_time
		self.status = 'out'
	

	

def todaysPeople(filename):
		
	people = []
	
	with open(filename, 'rb') as data:

		todays_roster = csv.reader(data)
		for row in todays_roster:
			
			if (row[0] != "Name"):
				
				people.append(Staff(row[0], findAddress(row[0]), row[1], row[3], 'out')) 
				
	return people	
			
		
def findAddress(name):
	
	with open('address.csv', 'rb') as name_data:
		address_list = csv.reader(name_data)
		for row in address_list:
			
			if (row[0] == name):
				
				return row[1]
				
				
				
def writer(person, state):

	with open("./%s" % person, "a") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow([state, time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())])				
				
				
def scan(person):
	
			result = bluetooth.lookup_name(person.bt, timeout=2)
		
			 

			if (result != None):
			 
				if person.status != "in":
					person.status = "in"
					darl = person.name + ".csv"
					writer(darl, "in")
				
		
			else:

				if person.status != "out":
					person.status = "out"
					darl = person.name + ".csv"
					writer(darl, "out")									
	
	
					
		
people = todaysPeople('daily.csv')
while running:

	print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
	for person in people:
		scan(person)
		print person.name, person.status
		time.sleep(2)
