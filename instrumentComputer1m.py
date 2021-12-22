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
#portVolts -    daqc a04
#stbVolts -     daqc a06
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

#setup server
from flask import Flask
app=Flask(__name__)

@app.route('/')
def first_action():
    return "hello world"

@app.route('/test')
def second_action():
    return "other output"

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
portVolts_channel=4
stbVolts_channel=6
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

#data file definitions  "instData" This is a dictionary object
#fileName: 'instData'
#SeqID: int
#portEngHours: int (cum)
#stbEngHours: int (cum)
#portRPM: int
#stbRPM: int
#portOilPress: int
#stbOilPress: int
#portCoolTemp: int
#stbCoolTemp: int
#portVolts: int
#stbVolts: int
#stbEngOn: int
#portEngOn: int
#gen1On: int
#gen2On: int
#gen2OilPress: int
#gen1OilPress: int
#gen1CoolTemp: int
#gen2CoolTemp: int
#stabOilLo: int
#acPowerOn: int
#refrigOn: int
#rearBildgeOn: int
#frontBildgeOn: int
#TurnOffSystem: int

#data path for instData file
dataPath = "/home/pi/"








                                                    
SeqID=0
clock_count=0
portRPMcounter =0
stbRPMcounter=0
stbHourCounter=0
portHourCounter=0


data1={}

def bit_set(x,n):
    if x & (1<<n): return 1
    else: return 0

def ADCoutTemp(V):
    #R=800.
    #output=int(.211*1023*V*((r)/(r+R))/vmaxinput)
    #output=int(53*V*(1-(r/(r+R))))
    if V <160:
               output=int(V + .21*(160-V))
    return output

def ADCoutPress(V):
    #R=330.
    #output=int(.211*1023*V*((r)/(r+R))/vmaxinput)
    #output=int(53*V*((r)/(r+R)))
    output=int(V + .3*(V-52))
    return output

def ADCoutVolt(V):
    output=int(10*(V/256)+.5)
    return output


def portRPM_callback(portRPM_channel):
    global portRPMcounter
    portRPMcounter +=1
    
def stbRPM_callback(stbRPM_channel):
    global stbRPMcounter
    stbRPMcounter +=1

def the_callback(in_channel):
    #this callback occurs every 0,1 seconds
    global portRPMcounter
    global stbRPMcounter
    global clock_count 
    clock_count += 1 

    #read data
    
    if clock_count==10:

        #read data
        avalues0=DAQC.getADCall(0)
        avalues1=DAQC.getADCall(1)
        dvalue0=DAQC.getDINall(0)
        dvalue1=DAQC.getDINall(1)

        #convert and scale analog data
        data1["portOilPress"]=ADCoutPress(avalues0[0])
        data1["stbOilPress"]=ADCoutPress(avalues0[1])
        data1["portCoolTemp"]=ADCoutTemp(avalues0[2])
        data1["stbCoolTemp"]=ADCoutTemp(avalues0[3])
        data1["portAmp"]=ADCoutVolt(avalues0[4])
        data1["stbAmp"]=ADCoutVolt(avalues0[6])

        data1["gen2OilPress"]=ADCoutPress(avalues1[0])
        data1["gen1OilPress"]=ADCoutPress(avalues1[1])
        data1["gen1CoolTemp"]=ADCoutTemp(avalues1[2])
        data1["gen2CoolTemp"]=ADCoutTemp(avalues1[3])

        #convert digital data
        data1["stbEngOn"]=bit_set(dvalue0[2])
        data1["portEngOn"]=bit_set(dvalue0[3])
        data1["gen1EngOn"]=bit_set(dvalue0[4])
        data1["gen2EngOn"]=bit_set(dvalue0[5])
        data1["stabOilLo"]=bit_set(dvalue1[0])
        data1["acPowerOn"]=bit_set(dvalue1[1])
        data1["refrigOn"]=bit_set(dvalue1[2])
        data1["rearBildgeOn"]=bit_set(dvalue1[3])
        data1["frontBildgeOn"]=bit_set(dvalue1[4])
        data1["TurnOffSystem"]=bit_set(dvalue1[5])

        #setup RPM output
        data1["portRPM"]=portRPMcounter*15
        data1["stbRPMcounter"]=stbRPMcounter

        #setput Engine  meters
        if data1['stbEngOn'] == True: stbHourCounter += 1
        if data1['portEngOn'] == True: stbHourCounter +=1
        

        if stbHourCounter == 360:
            data1['stbEngHour']+= 1
            stbHourCounter = 0
        if portHourCounter == 360:
            data1['portEngHour']+=1
            stbHourCounter = 0

        data1['SeqID']+=1



        #write the data1 object to a file- jsonize first
        
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

    #with open(path+'kfactors.txt') as json_file0:
    #   kfactor=json.load(json_file0)
    with open(path +'instData.txt') as json_file1:
        data1=json.load(json_file1)


    #start PWM
    p.start(50)
    #start server
    app.run(debug=False,port = 80, host='0.0.0.0')
    while (True):
        
        signal.pause()

    p.stop()