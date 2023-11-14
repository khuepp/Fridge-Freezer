# Bibs allgeimein
from machine import Pin, soft_reset
from time import sleep, sleep_ms
#import threading

# Bibs Temperatursensor
from onewire import OneWire
from ds18x20 import DS18X20

# Bibs Display
from machine import I2C
from machine_i2c_lcd import I2cLcd



# ---Relais---
relais = Pin(14, Pin.OUT)

# ---Schalter---
schalter = Pin(10, Pin.IN, Pin.PULL_DOWN)
# Alter Zustand Schalter Variable
if (schalter.value()==1):schalter_state = 0
else:schalter_state = 1
# 0 = frieren; 1 = kuehlen

# ---Display---
# Initialisierung I2C
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
# Initialisierung LCD über I2C
lcd = I2cLcd(i2c, 0x27, 2, 16)
# Text in Zeilen
sleep(1)
lcd.clear()
lcd.putstr("Starting")
sleep(2)
lcd.clear()

# ---Temperatur---
# Initialisierung GPIO, OneWire und DS18B20
one_wire_bus = Pin(16)
sensor_ds = DS18X20(OneWire(one_wire_bus))
lcd.putstr(str(sensor_ds))
sleep(3)
lcd.clear()
# One-Wire-Geräte ermitteln
devices = sensor_ds.scan()


def temperatur():
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


def kuehlen():
    print("Modus: Kühlen")
    temp = temperatur()
    
    if temp > 8:
        if relais.value() == 0:
            for i in range(60):
                print(i)
                temperatur()
                if(schalter.value()==0):return
                sleep(1)
            relais.on()
    elif temp < 6:
        if relais.value() == 1:
            print("Relais aus")
            for i in range(300):
                print(i)
                temperatur()
                if(schalter.value()==0):return
                sleep(1)
            relais.off()
    else:
        sleep(1)

def frieren():
    print("Modus: Friefen")    
    temp = temperatur()
    if temp > -17:
        if relais.value() == 0:
            print("Relais an")
            for i in range(60):
                print(i)
                temperatur()
                if(schalter.value()==1):return
                sleep(1)
            relais.on()
    elif temp < -19:
        if relais.value() == 1:
            print("Relais aus")
            for i in range(300):
                print(i)
                temperatur()
                if(schalter.value()==1):return
                sleep(1)
            relais.off()
    else:
        sleep(1)

while True:       
    if(schalter.value()==1):
        if(schalter_state == 0):
            lcd.move_to(0,0)
            lcd.putstr("               ")
            lcd.move_to(0,0)
            #lcd.putstr("Kuehlschrank" + "\n" + "    Temp:")
            lcd.putstr("Kuehlschrank    Temp:")

            schalter_state = 1
        kuehlen()
    else:
        if(schalter_state ==1):
            lcd.move_to(0,0)
            lcd.putstr("               ")
            lcd.move_to(0,0)
            lcd.putstr("Gefrierschrank  Temp:")
            schalter_state = 0
        frieren()







