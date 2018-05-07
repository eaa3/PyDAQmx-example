#!/usr/bin/env python
import sys
from ctypes import *
import ctypes

# Diar imports
import time 
import numpy
float64 = ctypes.c_double
int32 = ctypes.c_long
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong

# Diar variables
readVals = 10000
dataz = numpy.zeros((readVals,), dtype=numpy.float64)
countr = 0


dll = windll.LoadLibrary("nicaiu.dll")

#Steps:
#    1. Create a task.
#    2. Create an analog input voltage channel.
#    3. Read a scalar value from the channel.
#    4. Call the Clear Task function to clear the task.
#    5. Display an error if any.

#Note: All DAQmx function return 0 on success.
#This example checks for 0 at each step and reports an error for non-zero return values

##############################
#Create a Task
##############################
taskHandle = c_int(0)           #DAQmx TaskHandle
taskName = "AITask"             #Task Name

print "Creating a Task"

#First create the task and get a handle to the task that will be used for all subsequenct operations
#Function Prototype: int32 DAQmxCreateTask (const char taskName[], TaskHandle *taskHandle);
returnValue = dll.DAQmxCreateTask(taskName, byref(taskHandle))
if returnValue != 0:
    print >> sys.stderr, "Could not Create Task. Error: ", returnValue, "\n"
    sys.exit(returnValue)

print "TaskName: ", taskName
print "taskHandle: ", taskHandle
print "returnValue: ", returnValue, "\n"

###############################
##Add an AI Channel to the Task
###############################
physicalChannel = "dev1/ai2"    #Physical Channel: AI0 on Dev1
channelName = "ai2"             
terminalConfig = -1             #DAQmx_Val_Cfg_Default constant from NIDAQmx.h
minVal = c_double(-10.0)
maxVal = c_double(10.0)
units = 10348                   #DAQmx_Val_Volts constant from NIDAQmx.h
customScaleName = None

print "Adding an AI Channel to the Task"

#Add an analog input channel to the task and specify/configure the channel to read on:
#Specify dev1/ai0 as the channel, use the default terminal configuration and specify that the units is Volts
#Function Prototype: int32 DAQmxCreateAIVoltageChan (TaskHandle taskHandle, const char physicalChannel[],
    #const char nameToAssignToChannel[], int32 terminalConfig, float64 minVal, float64 maxVal,
    #int32 units, const char customScaleName[])
returnValue = dll.DAQmxCreateAIVoltageChan(taskHandle, physicalChannel, channelName, terminalConfig, minVal, maxVal, units, customScaleName)

DAQmx_Val_Rising = 10280
DAQmx_Val_FiniteSamps = 10178
max_num_samples = 1000 
sampleRate = float64(60.0) # Sample rate similar to Unity3D game engine sampling/refresh rate
DAQmx_Val_ContSamps = 10123

dll.DAQmxCfgSampClkTiming(taskHandle,"",sampleRate,DAQmx_Val_Rising,DAQmx_Val_ContSamps,uInt64(max_num_samples));
								

if returnValue != 0:
    print >> sys.stderr, "Could not add Channel. Error: ", returnValue, "\n"
    sys.exit(returnValue)

print "ReturnValue: ", returnValue, "\n"

###############################
##Read a scalar value
###############################
timeout = c_double(10.0) # originally set at 10.0
value = c_double(0)
reserved = None

#############################################################################################
#############################################################################################
######################################### The meat ##########################################
######################################## by Diar K. #########################################
#############################################################################################
freq=0.01 # Frequency set at 100kHz but only samples at 47.8Hz: >> Check what is bottlenecking
sampleTime = 5.0 # Duration of sampling aka trial duration
t=time.time()
while True:
	#t+=freq
	
	#print "Reading a scalar value from the channel"

	#Next, use the taskHandle to read a single scalar value on the channel specified earlier
	#Function Prototype: int32 DAQmxReadAnalogScalarF64 (TaskHandle taskHandle, float64 timeout, float64 *value, bool32 *reserved);
	returnValue = dll.DAQmxReadAnalogScalarF64(taskHandle, timeout, byref(value), reserved)
	if returnValue != 0:
		print >> sys.stderr, "Could not read Value. Error: " ,returnValue, "\n"
		sys.exit(returnValue)
	
	#dataz[countr] = value	
	
	print value
	#print countr
	#print time.time()-t2
	
	#print "Value: ", value
	#print "ReturnValue: ", returnValue, "\n"
	
	countr +=1
	
	#time.sleep(max(0,t-time.time()))
	
	if(time.time()-t >=sampleTime):
		break
	
print "The count is: ", countr
print "Sampling Frequency: ", countr/sampleTime, "Hz \n"
#############################################################################################
#############################################################################################
########################################## End ##############################################
#############################################################################################
#############################################################################################
	
##############################
##Clear the Task
##############################
print "Clearing the task"

#Finally, clear the task to release its resources
#Function Prototype: int32 DAQmxClearTask (TaskHandle taskHandle);
returnValue = dll.DAQmxClearTask(taskHandle)
if returnValue != 0:
    print >> sys.stderr, "Could not clear Task. Error: " ,returnValue, "\n"
    sys.exit(returnValue)

print "ReturnValue: ", returnValue, "\n"