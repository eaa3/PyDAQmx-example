from __future__ import print_function

import socket
import time
import daqmx
import matplotlib.pyplot as plt
import numpy as np
import sys

from ft_calib import calibrate_ft_reading, load_calib_matrix


if __name__== "__main__":

	if len(sys.argv) < 5:
		print("usage: send_UDP.py <sample_rate> <dest_host(ip_address or hostname)> <device> <channel_list> [calib_file] [bias_calib_file] [<dest_port>] \n default dest_port: 5000")
		print("e.g.: send_UDP.py 1000 irlab-ubuntu-16 Dev2 [0,1,2,3,4,5] 5000 FT14509.cal FT14509bias.cal")
		exit(1)
	
	SAMPLE_RATE = int(sys.argv[1])
	UDP_IP = sys.argv[2]
	UDP_PORT = 50000
	device = sys.argv[3]#'Dev2'
	channel_list = eval(sys.argv[4])

	calib_matrix = np.eye(6)
	bias = None
	
	if len(sys.argv) == 6:
		calib_file = sys.argv[5]
		calib_matrix = load_calib_matrix(calib_file)
	
	if len(sys.argv) == 7:
		bias_calib_file = sys.argv[6]
		file = open(bias_calib_file,"r")
		bias_line = file.readline()
		bias = np.array([float(v) for v in bias_line.split(',')])
		print("Loaded bias from file: ", bias)


	if len(sys.argv) == 8:
		UDP_PORT = int(sys.argv[7])

	print("UDP target IP:", UDP_IP)
	print("UDP target port:", UDP_PORT)
	print("Loop rate:", SAMPLE_RATE)
	#print "message:", MESSAGE

	sock = socket.socket(socket.AF_INET, # Internet
						 socket.SOCK_DGRAM) # UDP



	# Create a task object
	task = daqmx.tasks.Task()
	task.sample_rate = SAMPLE_RATE
	
	channels = []

	# Create a channel object
	for channel_idx in channel_list:
		channel = daqmx.channels.AnalogInputVoltageChannel()
		channel.physical_channel =  "%s/ai%d"%(device,channel_idx,)

		channel_name = "analog input %d"%(channel_idx,)
		channels.append(channel_name)
		channel.name = channel_name
		# Add the channel to the task and activate option to append data in memory
		#task.setup_append_data() (optionally)
		task.add_channel(channel)

	# task.setup_append_data()


	task.configure_sample_clock(sample_rate=task.sample_rate,samples_per_channel=1)
	start = time.time()
	elapsed_time = 0
	
	bias_calib_steps = 5*SAMPLE_RATE # calibrate the bias in 5 seconds
	sampleTime = 1 # 1 second
	sample_counter = 0
	quit = False
	
	if bias is None:
		bias = np.zeros(6)
		print("Calibrating bias...")
		
		
		for i in range(bias_calib_steps):
			raw_data, samples_per_channel_received = task.read()
			bias += raw_data[0]
			
		bias /= bias_calib_steps
		print("Bias calibrated: ",bias)
		
	print("Transmitting data... On a separate client, connect to UDP address: %s port: %d to receive it.\n\n"%(UDP_IP,UDP_PORT,))
	
	
	

	while not quit:
		raw_data, samples_per_channel_received = task.read()
		
		data = calibrate_ft_reading(raw_data[0] - bias, calib_matrix)

		#print("Sample Raw DATA: ", str(raw_data[0])[1:-1])
		#print("Sample Calbtd DATA: ", str(data)[1:-1])
		sdata = str(data)[1:-1] + ' %.3f'%(time.time(),) + '\n'
		sock.sendto(sdata, (UDP_IP, UDP_PORT))
		sample_counter += 1	

		elapsed_time = time.time() - start
		if elapsed_time > sampleTime:
			sys.stdout.write("Current Loop Frequency: %d Hz\r"%(sample_counter,))
			sample_counter = 0
			start = time.time()

			# print "Time is up!"


