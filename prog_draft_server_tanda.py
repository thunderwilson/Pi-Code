##Draft code for asic smart badge implementation
#RasPi local code
##Author: T D G Wilson
##Date: 18/11/2014


##*****************************GLOBALS***************************************
HOST = ''
PORT = 50007
device_id = '4b200275-5153-4cc3-8356-a52e5539a801' ##THIS IS VEWY IMPORTANT
client_list = ['192.168.1.76', '192.192.192.192']
##*************************************************************************

import os, time, datetime, subprocess, time, sys, bluetooth, csv, blescan 

import bluetooth._bluetooth as bluez

import socket

import requests, json, simplejson
	
running = 1
	

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


def People(device_id):
		
	
	people_keys = {}
	payload = {'device_id' : device_id}
	r = requests.get("https://www.tanda.co/api/userlist?", params = payload)
	data = r.text

	j = json.loads(data)
	for item in j:
				
		people_keys[item["user_name"]] = [item["passcode"], ' ', findAddress(item["user_name"])]

	
				
	return people_keys

	
def findAddress(name):
	
	with open('address.csv', 'rb') as name_data:
		address_list = csv.reader(name_data)
		for row in address_list:
			
			if (row[0] == name):
				
				return row[1]
				
				
				
def clock(person, state, people_keys):
	print "In clock"
	timestamp = int(time.time())
	access_code = people_keys[person][0]
	if state == 'in':
		print "clocking in: ", people_keys[person][0]
		r = requests.post('https://www.tanda.co/api/login -i --data "device_id=",device_id, "&time =",timestamp,"&access_code=",access_code')
	elif state == 'out':
		print "clocking out: ", people_keys[person][0]
		r = requests.post('https://www.tanda.co/api/logout -i --data "device_id=",device_id, "&time =",timestamp,"&access_code=",access_code')


def recv_data(unique_nearby_devices, HOST, PORT, client_list):	
	yet_to_connect = []	
	for item in client_list:
		yet_to_connect.append(item)


	socket.socket.allow_reuse_address = True
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.settimeout(10)
	fuck_this = 0

	while len(yet_to_connect) > 0:
		
		
		try:

			s.listen(1)

	
		
	
			conn, addr = s.accept()
			if addr[0] in yet_to_connect:
				print 'Connected by', addr[0]
			fuck_this += 1
			if fuck_this > 2* len(yet_to_connect):
				print "Did not reveive data from: ", yet_to_connect
				conn.sendall(data)
				conn.close()
				return unique_nearby_devices

			if addr[0] in yet_to_connect:
			
				yet_to_connect.remove(addr[0])



			data = conn.recv(1024)
			unique_nearby_devices.append(data)


##		if not data: 
##			break  #Come back to this puppy. Could cause troubles


			
			
		

		except socket.timeout, e:
			err = e.args[0]
			if err == 'timed out':
				print "Did not receive data from: ", yet_to_connect				
				
				return unique_nearby_devices
			
	
		


		conn.sendall(data)
	
		
	
	conn.close()	
	return unique_nearby_devices



					
def unique(nearby_devices, unique_nearby_devices):
	
	for addr in nearby_devices:


		
		device = []
		device.append(addr.split(','))
		

		
		if device[0][0] not in unique_nearby_devices:
			
			unique_nearby_devices.append(device[0][0].upper())
			
	return unique_nearby_devices
					
def scan(people):
			unique_nearby_devices = []
			nearby_devices = blescan.parse_events(sock, 2)
			unique_nearby_devices = unique(nearby_devices, unique_nearby_devices)
			recv_data(unique_nearby_devices, HOST, PORT, client_list)
			unique_nearby_devices = unique(unique_nearby_devices, unique_nearby_devices)
			print "Devices: ", unique_nearby_devices
			for person in people:
				
				print people[person][2], "\n"
				
				if people[person][2] in unique_nearby_devices and person =="Tom's Tester":
					print "Checking if first time in"
				
					if people[person][1] != "in":
					
						people[person][1] = "in"
						
						clock(person, "in", people)
				
				else:
				
					if people[person][1] != "out":
						people[person][1] = "out"
						
						clock(person, "out", people)

							


					
		
people = People(device_id)

print people["Tom's Tester"][2]
sock = init() #remember to uncomment me when you want tserver to act as a scanner too

while running:

	print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
	scan(people)
	
