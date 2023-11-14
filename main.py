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
if (schalter.value()==1):schalter_old = 0
else:schalter_old = 1

# ---Temperatur---
# Initialisierung GPIO, OneWire und DS18B20
one_wire_bus = Pin(16)
sensor_ds = DS18X20(OneWire(one_wire_bus))
# One-Wire-Geräte ermitteln
devices = sensor_ds.scan()
# temp

# ---Display---
# Initialisierung I2C
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
# Initialisierung LCD über I2C
lcd = I2cLcd(i2c, 0x27, 2, 16)
# Text in Zeilen
sleep(1)

reset = 0


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
    global reset
    print("Modus: Kühlen")
    temp = temperatur()
    
    if temp > 8:
        if relais.value() == 0:
            print("Relais an")
            for i in range(60):
                print(i)
                temperatur()
                sleep(1)
            relais.on()
            reset = reset + 1
            
    elif temp < 6:
        if relais.value() == 1:
            print("Relais aus")
            for i in range(300):
                print(i)
                temperatur()
                sleep(1)
            relais.off()
            reset = reset + 5

def frieren():
    global reset
    print("Modus: Friefen")    
    temp = temperatur()
    if temp > -17:
        if relais.value() == 0:
            print("Relais an")
            for i in range(60):
                print(i)
                temperatur()
                sleep(1)
            relais.on()
            reset = reset + 1

    elif temp < -19:
        if relais.value() == 1:
            print("Relais aus")
            for i in range(300):
                print(i)
                temperatur()
                sleep(1)
            relais.off()
            reset = reset + 5


while True:
    if reset>60:
        reset = 0
        soft_reset()
        
    if(schalter.value()==1):
        if(schalter_old == 0):
            lcd.move_to(0,0)
            lcd.putstr("               ")
            lcd.move_to(0,0)
            lcd.putstr("Kuehlschrank" + "\n" + "Temp:")
            schalter_old = 1
        kuehlen()
    else:
        if(schalter_old ==1):
            lcd.move_to(0,0)
            lcd.putstr("               ")
            lcd.move_to(0,0)
            lcd.putstr("Gefrierschrank" + "\n" + "Temp:")
            schalter_old = 0
        frieren()







