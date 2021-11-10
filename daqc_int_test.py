

import signal
import time
import sys
import piplates.DAQCplate as DAQC
import RPi.GPIO as GPIO


rpm_Daqc_channel=0
inter_channel=15




def signal_handler(sig,frame):
    GPIO.cleanup()
    sys.exit()

def rpm_callback(inter_channel):
    print('interrupt received')
    




if __name__== '__main__':
    
    GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    #set up the interrupt system for gpio #22 with unique callback
    GPIO.add_event_detect(22,GPIO.FALLING, callback=rpm_callback)
    #enable interrupts on daqc board 1
    DAQC.intEnable(1)

    
    
    signal.signal(signal.SIGINT, signal_handler)

    
    

    
    while (True):
        print("looping")
        #get input square wave coming into daqc digital input 0
        int_state=DAQC.getDINbit(1,0)
        print(int_state)

        
        time.sleep(.1)

    