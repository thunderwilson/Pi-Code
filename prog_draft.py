##Draft code for basic smart badge implementation.
##RasPi local code
##Author: T D G Wilson
##Date: 18/11/2014



import os, time, subprocess, time, sys, bluetooth, csv, blescan #Will need to import ble library

import bluetooth._bluetooth as bluez



	
running = 1



class Staff:
	
	def __init__(self, name, bt, start_time, end_time, status):
		
		self.name = name 
		self.bt = bt
		self.start_time = start_time
		self.end_time = end_time
		self.status = 'out'
	

def init():
		
	dev_id = 0
	try:
		sock = bluez.hci_open_dev(dev_id)
		print sock

	except:
		print "error accessing bluetooth device..."
		sys.exit(1)

	blescan.hci_le_set_scan_parameters(sock)
	blescan.hci_enable_le_scan(sock)
	return sock


def People(filename):
		
	people = []
	
	with open(filename, 'rb') as data:

		roster = csv.reader(data)
		for row in roster:
			
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
		writer.writerow([state, time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())])				
				
				
def scan(people):
	
			nearby_devices = blescan.parse_events(sock, 10)
			print "im in"
			for addr in nearby_devices:
				print addr
				for person in people:
					
					if (addr[0] == person.bt):
						
						
						if person.status != "in":
								person.status = "in"
								darl = person.name + ".csv"
								print person.name, person.status
								writer(darl, "in")
						
				
						else:

							if person.status != "out":
								person.status = "out"
								darl = person.name + ".csv"
								print person.name, person.status
								writer(darl, "out")	
		
			 

								
	
	
					
		
people = People('daily.csv')

sock = init()

while running:

	print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
	scan(people)
	
