import time
#Waage
EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

class Waage():
    def __init__(self): 
        self.hxDose = HX711(24, 25)
        self.hxFillLevel = HX711(17, 27)
        self.hxDose.set_reading_format("MSB", "MSB")
        self.hxFillLevel.set_reading_format("MSB", "MSB")
        self.hxDose.set_reference_unit(226.6)
        self.hxFillLevel.set_reference_unit(78.7)
        self.hxDose.reset()
        self.hxFillLevel.reset()
        self.hxDose.tare()
        # Gewicht der Behälterkonstruktion (Tara)
        self.const_weight = 10430
        #Wägezelle für Füllstand nicht tarieren, damit eventuell enthaltener Kaffee bei Programmstart nicht wegtariert wird
        #self.hxFillLevel.tare()
        
    def get_weight_dose(self):
            val_dose = max(0,int(self.hxDose.get_weight(3)))
            #self.hxDose.power_down()
            #self.hxDose.power_up()
            return val_dose
        
    def get_weight_level(self):
            print('a')
            val_level = max(0, int(self.hxFillLevel.get_weight(3) - self.const_weight))
            print('b')
            #self.hxFillLevel.power_down()
            #self.hxFillLevel.power_up()
            return val_level
    
    def isGoodResult(self, max_weight, result):
            if result < max_weight - 3 or result > max_weight + 3:
                print("Schlechte Abfüllung!")
                return "OUT"
            else:
                print("Gute Abfüllung!")
                return "IN" 
    