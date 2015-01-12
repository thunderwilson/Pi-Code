##Draft code for basic smart badge implementation.
##RasPi local code
##Author: T D G Wilson
##Date: 18/11/2014

HOST = '192.168.20.113'
PORT = 50007

import os, time, subprocess, time, sys, bluetooth, csv, blescan #Will need to import ble library

import bluetooth._bluetooth as bluez

import socket


	
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


	
def send_data(unique_nearby_devices, HOST, PORT):	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	for line in unique_nearby_devices:
		
		
		s.sendall(str(line))
	data = s.recv(1024)
	s.close

				
def unique(nearby_devices, unique_nearby_devices):
	
	for addr in nearby_devices:


		device = []
		device.append(addr.split(','))
		
		
		if device[0][0] not in unique_nearby_devices:
			
			unique_nearby_devices.append(device[0][0])
			
		
					
	return unique_nearby_devices
					
def scan():
			unique_nearby_devices = []
			nearby_devices = blescan.parse_events(sock, 4)
			
			unique_nearby_devices = unique(nearby_devices, unique_nearby_devices)
			
			#send_data(unique_nearby_devices, HOST, PORT)
			for addr in unique_nearby_devices:
				print addr

					
		
sock = init()

while running:

	print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
	scan()
	
