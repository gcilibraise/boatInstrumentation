

import signal
import time
import sys
import piplates.DAQCplate as DAQC
import RPi.GPIO as GPIO

in_channel=10
rpm_channel=0
inter_channel=22
input_counter=0

def Clock_callback(in_channel):
    print(time.time_ns())

def signal_handler(sig,frame):
    GPIO.cleanup()
    sys.exit()

def rpm_callback(rpm_channel):
    #global input_counter
    #int_state=DAQC.getINTflags(1)
    #print(int_state)
    #if int_state==1:
    #   input_counter =input_counter + 1
    print("input pulse dectected")
    




if __name__== '__main__':
    #pin 08 or gpio14 is the source pin for the pwm output
    #pin 10 or gpio15 is the input pin for the interrupt dectect

    #set pin numbering reference
    GPIO.setmode(GPIO.BOARD)

    #setup pin 10 as an input 
    GPIO.setup(10,GPIO.IN)
    #set pin 22 for processing interrupts from DAGC
    #GPIO.setup(inter_channel,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    #set up the interrupt system for gpio #22 with unique callback
    #GPIO.add_event_detect(22,GPIO.FALLING, callback=rpm_callback)


    #setup pin
    GPIO.setup(8,GPIO.OUT)
    #setup pin 8 as a PWM output with a frequency of 10 hertz
    p=GPIO.PWM(8,10)
    GPIO.add_event_detect(10,GPIO.FALLING,callback=Clock_callback)
    signal.signal(signal.SIGINT, signal_handler)

    #enable interrupts on daqc board 1
    #DAQC.intEnable(1)

    #start PWM
    p.start(50)
    while (True):
        print("looping")
        #GPIO.output(8,1)
        #print("high")
        #time.sleep(1)
        #GPIO.output(8,0)
        #print("low")
        signal.pause()

    p.stop()