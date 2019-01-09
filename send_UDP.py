import socket
import time
import daqmx
import matplotlib.pyplot as plt
import numpy as np
import sys


if __name__== "__main__":

	if len(sys.argv) < 3:
		print "usage: send_UDP.py <sample_rate> <dest_ip> [<dest_port>] \n default dest_port: 5000"
		exit(1)
	
	SAMPLE_RATE = sys.argv[1]
	UDP_IP = sys.argv[2]
	UDP_PORT = 50000
	
	if len(sys.argv) == 4:
		UDP_PORT = int(sys.argv[3])

	print "UDP target IP:", UDP_IP
	print "UDP target port:", UDP_PORT
	print "Loop rate:",
	#print "message:", MESSAGE

	sock = socket.socket(socket.AF_INET, # Internet
						 socket.SOCK_DGRAM) # UDP



	# Create a task object
	task = daqmx.tasks.Task()
	task.sample_rate = 1000
	device = 'Dev2'
	channels = []

	# Create a channel object
	MAX_CHANNELS = 6
	for channel_idx in range(MAX_CHANNELS):
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
	sampleTime = 1 # 5 seconds
	sample_counter = 0
	quit = False

	print "Transmitting data... On a separate client, connect to UDP address: %s port: %d to receive it.\n\n"%(UDP_IP,UDP_PORT,)
	while not quit:
		data, samples_per_channel_received = task.read()
		

		#print "Sample DATA: ", str(data[0])[1:-1]
		sdata = str(data[0])[1:-1] + ' %.6f'%(time.time(),) + '\n'
		sock.sendto(sdata, (UDP_IP, UDP_PORT))
		sample_counter += 1	

		elapsed_time = time.time() - start
		if elapsed_time > sampleTime:
			sys.stdout.write("Current Loop Frequency: %d Hz\r"%(sample_counter,))
			sample_counter = 0
			start = time.time()

			# print "Time is up!"


