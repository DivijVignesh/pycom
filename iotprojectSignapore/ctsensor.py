import machine
from machine import ADC
import time
adc = machine.ADC(bits=10) 
apin = adc.channel(pin='P13',attn=ADC.ATTN_11DB)

def CtCurrent():
    i=1
    j=0
    peakI=0
    while i<=10:
        i=i+1
        peakI= apin()
        if peakI<j:
            peakI=j
            time.sleep(0.001)
    rmsI=((peakI/1023)*30*3.3)/1.414
    

    print('Current'+str(rmsI))
    # print(peakI)
    peakI=0
    time.sleep(0.1)
    return rmsI
