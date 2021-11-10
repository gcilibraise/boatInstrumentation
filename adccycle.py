from typing import IO
import piplates.DAQCplate as DAQC
import RPi.GPIO as GPIO
import time


while(True):
    print(DAQC.getADC(1,0))
    
    voltage=DAQC.getADC(1,0)
    now=time.localtime()
    nowstring=time.strftime("%I:%M:%S %p",now)
    print(voltage , nowstring)
    time.sleep(2)
        





