import socket
import time
import daqmx
import matplotlib.pyplot as plt
import numpy as np

UDP_IP = "localhost"
UDP_PORT = 50000

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
#print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP



# Create a task object
task = daqmx.tasks.Task()
task.sample_rate = 900
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


task.configure_sample_clock(sample_rate=900,samples_per_channel=1)
start = time.time()
elapsed_time = 0
sampleTime = 10 # 5 seconds
sample_counter = 0
quit = False
all_data = np.zeros(6)
while not quit:
	data, samples_per_channel_received = task.read()
	all_data = np.vstack([all_data,data[0]])
	sample_counter += 1

	print "Sample DATA: ", str(data[0])[1:-1]
	sdata = str(data[0])[1:-1] + '\n'
	sock.sendto(sdata, (UDP_IP, UDP_PORT))


	elapsed_time = time.time() - start
	if elapsed_time > sampleTime:
		quit = True

		print "Time is up!"

print "Total samples collected:", sample_counter, " samples"
print "Time elapsed", elapsed_time, " seconds"
print "Observed Frequency", sample_counter/elapsed_time, " Hz"

plt.figure()
plt.plot(all_data)
plt.show()

