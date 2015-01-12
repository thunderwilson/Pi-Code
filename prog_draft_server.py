##Draft code for basic smart badge implementation.
##RasPi local code
##Author: T D G Wilson
##Date: 18/11/2014

HOST = ''
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
		self.status = 'out'
	

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
	
def recv_data(unique_nearby_devices, HOST, PORT):	
	client_list = ['192.168.20.113', 'something else']
	yet_to_connect = client_list
	socket.socket.allow_reuse_address = True
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	wait_time = 5
	time = 0
	while len(yet_to_connect) >0 & time < wait_time:
		print "in the while loop"

		s.listen(1)
		print " past listen line"
		conn, addr = s.accept()
		print 'Connected by', addr[0]
		
		if addr[0] in client_list:
			
			yet_to_connect.remove(addr[0])

		data = conn.recv(1024)
		unique_nearby_devices.append(data)
		if not data: break  #Come back to this puppy. Could cause troubles
		time += 1
		print time


	if len(yet_to_connect) >0:
		print "Failed to receive data from", yet_to_connect, ", moving on"

	

	conn.sendall(data)
	
	conn.close()	
	return unique_nearby_devices

					
def unique(nearby_devices, unique_nearby_devices):
	
	for addr in nearby_devices:


		
		device = []
		device.append(addr.split(','))
		

		
		if device[0][0] not in unique_nearby_devices:
			
			unique_nearby_devices.append(device[0][0])
			
	return unique_nearby_devices
					
def scan(people):
			unique_nearby_devices = []
			##nearby_devices = blescan.parse_events(sock, 2)
			##unique_nearby_devices = unique(nearby_devices, unique_nearby_devices)
			recv_data(unique_nearby_devices, HOST, PORT)
			unique_nearby_devices = unique(unique_nearby_devices, unique_nearby_devices)
			
			for person in people:
			
				if persorn.bt.lower() in unique_nearby_devuces:
					print "Checking if first time in"
				
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

##sock = init() remember to uncomment me when you want tserver to act as a scanner too

while running:

	print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
	scan(people)
	
