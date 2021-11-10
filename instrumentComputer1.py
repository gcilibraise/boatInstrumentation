#import piplates.DAQCplate as DAQC
#this program reads two freq inputs on chans 3 & 4
#it uses a pwm 10hz window to gate the counting of the input pulses
# the output is displayed every ten seconds
#input signal port definitions
#portRPM - GPIO3
#stbRPM -GPIO4
#portOilPress - daqc a00
#stbOilPress -  daqc a01
#portCoolTemp - dagc a02
#stbCoolTemp -  daqc a03
#portAMPHi -    daqc a04
#portAMPLo -    daqc a05
#stbAMPHi -     daqc a06
#stbAMPLo -     daqc a07
#stbEngOn -     daqc d02
#portEngOn -    daqc d03
#gen1On -       daqc d04
#gen2On -       daqc d05
#gen2OilPress - daqc a10
#gem1OilPress - daqc a11
#gen1CoolTemp - daqc a12
#gen2CoolTemp - daqc a13
#stabOilLo -    daqc d10
#acPowerOn -    daqc d11
#refrigOn -     daqc d12
#rearBildgeOn - daqc d13
#frontBildgeOn - daqc d14
#TurnSystemOff - daqc d15

import json
import signal

import time
import sys
import RPi.GPIO as GPIO
import piplates.DAQCplate as DAQC

#GPIO channel assignments
portRPM_channel=3
stbPPM_channel=4
pwm_output_channel=14
timer_int_channel=15

#Dagc channel assignemts
#analog dagc board #0
portOilPress_channel = 0
stbOilPress_channel = 1
portCoolTemp_channel= 2
stbCoolTemp_channel=3
portAMPHi_channel=4
portAMPLo_channel=5
stbAMPHi_channel=6
stbAMPLo_channel=7
#digital daqc board #0
stbEngOn_channel=2
portEngOn_channel=3
gen1On_channel=4
gen2On_channel=5
#analog daqc board #1
gen2OilPress_channel = 0
gen2OilPress_channel = 1
gen1CoolTemp_channel = 2
gen2CoolTemp_channel =3
#digital daqc board #1
stbOilLo_channel = 0
acPowerOn_channel = 1
refrigOn_channel = 2
rearBildgeOn = 3
frontBildgeOn = 4
TurnOffSystem = 5








                                                    
SeqID=0
clock_count=0
portRPMcounter =0
stbRPMcounter=0

def bit_set(x,n):
    if x & (1<<n): return 1
    else: return 0



def portRPM_callback(portRPM_channel):
    global portRPMcounter
    portRPMcounter +=1
    
def stbRPM_callback(stbRPM_channel):
    global stbRPMcouter
    stbRPMcounter1 +=1

def the_callback(in_channel):
    #this callback occurs every 0,1 seconds
    global portRPMcounter
    global stbRPMcounter
    global clock_count 
    clock_count += 1 
    #read data
    avalues0=DAQC.getADCall(0)
    avalues1=DAQC.getADCall(1)
    dvalue0=DAQC.getDINall(0)
    dvalue1=DAQC.getDINall(1)
    if clock_count==10:
        print("rpm counter" , portRPMcounter,stbRPMcounter)
        portRPMcounter=0
        stbRPMcounter=0
        clock_count=0

def signal_handler(sig,frame):
    GPIO.cleanup()
    sys.exit()

if __name__== '__main__':
    #pin 08 or gpio14 is the source pin for the pwm output
    #pin 10 or gpio15 is the input pin for the interrupt dectect
    #pin 12 of gpio18 is the input for the rpm pulse train
    #set pin numbering reference
    GPIO.setmode(GPIO.BCM)

    #setup pin 15 as an input 
    GPIO.setup(15,GPIO.IN)

    #setup pwm pin
    GPIO.setup(14,GPIO.OUT)
    #setup pin 8 as a PWM output with a frequency of 0.1 hertz
    p=GPIO.PWM(14,10)
    #setup call back for clock
    GPIO.add_event_detect(15,GPIO.FALLING,callback=the_callback)
    signal.signal(signal.SIGINT, signal_handler)

    #setup input for rpm signal
    GPIO.setup(3,GPIO.IN)
    GPIO.add_event_detect(3,GPIO.RISING,callback=portRPM_callback)
    GPIO.setup(4,GPIO.IN)
    GPIO.add_event_detect(4,GPIO.FALLING,callback=stbRPM_callback)

#read data file
    path='/home/pi/Projects/pythontests/'

    with open(path+'kfactors.txt') as json_file0:
        kfactor=json.load(json_file0)
    with open(path +'instData.txt') as json_file1:
        data1=json.load(json_file1)


    #start PWM
    p.start(50)
    while (True):
        
        signal.pause()

    p.stop()