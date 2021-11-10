

import signal
import time
import sys
#import piplates.DAQCplate as DAQC
import RPi.GPIO as GPIO


""" def Clock_callback(in_channel):
    print(time.time_ns()) """

def signal_handler(sig,frame):
    GPIO.cleanup()
    sys.exit()

def rpm_callback(inter_channel):
    #global input_counter
    
    #int_state=DAQC.getDINall(1)
    print('interrupt detected')
    print(GPIO.input(4))
    
    
    #print(int_state)
    #if int_state==1:
    #   input_counter =input_counter + 1
    
    




if __name__== '__main__':
    #in_channel=10
    #rpm_Daqc_channel=0
    #inter_channel=22
    input_counter=0
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    #set up the interrupt system for gpio #22 with unique callback
    GPIO.add_event_detect(4,GPIO.RISING, callback=rpm_callback)


    #setup pin
    #GPIO.setup(8,GPIO.OUT)
    #setup pin 8 as a PWM output with a frequency of 10 hertz
    #p=GPIO.PWM(8,10)
    #GPIO.add_event_detect(10,GPIO.FALLING,callback=Clock_callback)
    signal.signal(signal.SIGINT, signal_handler)

    #enable interrupts on daqc board 1
    #DAQC.intEnable(1)

    #start PWM
    #p.start(50)
    while (True):
        print("looping")
        #int_state=DAQC.getDINbit(1,0)
        
        
        print(GPIO.input(4))
        #GPIO.output(8,1)
        #print("high")
        #time.sleep(1)
        #GPIO.output(8,0)
        #print("low")
        #signal.pause()
        time.sleep(.1)

    #p.stop()