# General libraries
from machine import Pin, soft_reset
from time import sleep, sleep_ms

# Temperature sensor libraries
from onewire import OneWire
from ds18x20 import DS18X20

# Display libraries
from machine import I2C
from machine_i2c_lcd import I2cLcd


# ---Relay---
relais = Pin(14, Pin.OUT)

# ---Switch---
switch = Pin(10, Pin.IN, Pin.PULL_DOWN)
# Old state switch variable
if (switch.value()==1):switch_state = 0
else:switch_state = 1
# 0 = freeze; 1 = refrigerate

# ---Display---
# Initializing I2C
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
# Initializing LCD via I2C
lcd = I2cLcd(i2c, 0x27, 2, 16)
# Text in lines
sleep(1)
lcd.clear()
lcd.putstr("Starting")
sleep(2)
lcd.clear()

# ---Temperature---
# Initializing GPIO, OneWire, and DS18B20
one_wire_bus = Pin(16)
sensor_ds = DS18X20(OneWire(one_wire_bus))
lcd.putstr(str(sensor_ds))
sleep(3)
lcd.clear()
# Detecting One-Wire devices
devices = sensor_ds.scan()


def temperature():
    sensor_ds.convert_temp()
    sleep_ms(750)
    for device in devices:
        temp = round(sensor_ds.read_temp(device),2)
        print('Temperatur:', temp)
        temp_str = str(temp)
        lcd.move_to(6,1)
        lcd.putstr("      ")
        lcd.move_to(6,1)
        lcd.putstr(temp_str)
        sleep(1)
    return temp


def refrigerate():
    print("Modus: Kühlen")
    temp = temperature()
    
    if temp > 8:
        if relais.value() == 0:
            for i in range(60):
                print(i)
                temperature()
                if(switch.value()==0):return
                sleep(1)
            relais.on()
    elif temp < 6:
        if relais.value() == 1:
            print("Relais aus")
            for i in range(300):
                print(i)
                temperature()
                if(switch.value()==0):return
                sleep(1)
            relais.off()
    else:
        sleep(1)

def freeze():
    print("Modus: Frieren")    
    temp = temperature()
    if temp > -17:
        if relais.value() == 0:
            print("Relais an")
            for i in range(60):
                print(i)
                temperature()
                if(switch.value()==1):return
                sleep(1)
            relais.on()
    elif temp < -19:
        if relais.value() == 1:
            print("Relais aus")
            for i in range(300):
                print(i)
                temperature()
                if(switch.value()==1):return
                sleep(1)
            relais.off()
    else:
        sleep(1)

while True:       
    if(switch.value()==1):
        if(switch_state == 0):
            lcd.move_to(0,0)
            lcd.putstr("               ")
            lcd.move_to(0,0)
            #lcd.putstr("Kuehlschrank" + "\n" + "    Temp:")
            lcd.putstr("Kuehlschrank    Temp:")

            switch_state = 1
        refrigerate()
    else:
        if(switch_state ==1):
            lcd.move_to(0,0)
            lcd.putstr("               ")
            lcd.move_to(0,0)
            lcd.putstr("Gefrierschrank  Temp:")
            switch_state = 0
        freeze()







