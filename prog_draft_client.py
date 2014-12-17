##Draft code for basic smart badge implementation.
##RasPi local code
##Author: T D G Wilson
##Date: 18/11/2014

HOST = '192.168.20.116'
PORT = 50007

import os, time, subprocess, time, sys, bluetooth, csv, blescan #Will need to import ble library

import bluetooth._bluetooth as bluez

import socket


	
running = 1



class Staff:
	
	def __init__(self, name, bt, start_time, end_time, status):
		
		self.name = name 
		self.bt = bt
		self.start_time = start_time
		self.end_time = end_time
		self.status = "out"
	

def init():
		
	dev_id = 0
	try:
		sock = bluez.hci_open_dev(dev_id)
		

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
	
def send_data(unique_nearby_devices, HOST, PORT):	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	for line in unique_nearby_devices:
		
		
		s.sendall(str(line))
	data = s.recv(1024)
	s.close

				
def unique(nearby_devices, unique_nearby_devices):
	
	for addr in nearby_devices:


		#print("In Unique function", addr)	Yay for debugging
		device = []
		device.append(addr.split(','))
		
		#print "Device name to compare", device[0][0]
		#for thing in unique_nearby_devices:
			#print "In list already", thing	
		
		if device[0][0] not in unique_nearby_devices:
			#print("adding  loop")
			unique_nearby_devices.append(device[0][0])
			
		
					
	return unique_nearby_devices
					
def scan(people):
			unique_nearby_devices = []
			nearby_devices = blescan.parse_events(sock, 4)
			#print (nearby_devices)		Yay more debugging =P =P
			unique_nearby_devices = unique(nearby_devices, unique_nearby_devices)
			
			send_data(unique_nearby_devices, HOST, PORT)
			for person in people:
			
				
				if person.bt.lower() in unique_nearby_devices:						
						
						print "checking first time in"

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
	
