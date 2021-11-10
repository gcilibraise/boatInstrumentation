#import piplates.DAQCplate as DAQC
#this program reads for freq inputs on chans 3 & 4 & 19 & 26
#it uses a pwm 10hz window to gate the counting of the input pulses
# the output is displayed every ten seconds
import signal
import time
import sys
import RPi.GPIO as GPIO

in_channel=10
counter=0
counter1=0
counter2=0
counter3=0
rpm_channel =3
rpm1_channel=4  
rpm2_channel=19
rpm3_channel=26                                                    

clock_count=0
old_time=0
new_time=0

def count_callback(rpm_channel):
    global counter
    counter +=1
    
def count1_callback(rpm1_channel):
    global counter1
    counter1 +=1

def count2_callback(rpm2_channel):
    global counter2
    counter2 +=1 

def count3_callback(rpm3_channel):
    global counter3
    counter3 +=1     

def the_callback(in_channel):
    #this callback occurs every 0,1 seconds
    global counter
    global counter1
    global counter2
    global counter3
    global clock_count 
    clock_count += 1  
    if clock_count==100:
        print("rpm counter" , counter,counter1,counter2,counter3)
        counter=0
        counter1=0
        counter2=0
        counter3=0
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
    GPIO.add_event_detect(3,GPIO.RISING,callback=count_callback)

    GPIO.setup(4,GPIO.IN)
    GPIO.add_event_detect(4,GPIO.FALLING,callback=count1_callback)

    GPIO.setup(19,GPIO.IN)
    GPIO.add_event_detect(19,GPIO.RISING,callback=count2_callback)
    
    GPIO.setup(26,GPIO.IN)
    GPIO.add_event_detect(26,GPIO.FALLING,callback=count3_callback)



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