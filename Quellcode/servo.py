import Adafruit_PCA9685
import waage
import time
import RPi.GPIO as GPIO

class Servo():
    def __init__(self):
        self._waage = waage.Waage()
        #Servopositionen
        #self.servo_lastGramm = 340
        #self.servo_fine = 320
        self.servo_auf = 390
        self.servo_zu = 260
        self.servo_tuer_auf = 300
        self.servo_tuer_zu = 130
        self.is_servo_open = False
        self.kill_thread = False
        
        try:
            self.pwm = Adafruit_PCA9685.PCA9685()
            self.pwm.set_pwm_freq(50)
            print("Servo Init")
            self.pwm.set_pwm(0, 0, self.servo_zu)
            time.sleep(1)
            self.pwm.set_pwm(0, 0, 0)
        except OSError as e:
            print('Kein Servo')
            self.pwm = None
    
    def openWithSwitch(self, wanted_weight):
        #try:
        GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        #pwm = Adafruit_PCA9685.PCA9685()
        #pwm.set_pwm_freq(50)
        self.pwm.set_pwm(2, 0, self.servo_tuer_zu)
        #while GPIO.input(23) == 0:
        while GPIO.input(23) == 0:
            self.pwm.set_pwm(2, 0, self.servo_tuer_zu)
        
        if wanted_weight <= 250:
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(3)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            print("Abgefüllt")
        elif wanted_weight <= 500:
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(5)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            print("Abgefüllt")
        elif wanted_weight <= 750:
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(7)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            print("Abgefüllt")
        else:
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(9)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_auf)
            time.sleep(0.5)
            self.pwm.set_pwm(2,0,self.servo_tuer_zu)
            time.sleep(0.5)
            print("Abgefüllt")
        #except:
             #print("Das Programm wurde geschlossen")
        #finally:
            #GPIO.cleanup()
    
    def empty_fill_level(self, fill_level):
        temp = fill_level
        if temp < 1000:
            self.pwm.set_pwm(0, 0, self.servo_auf)
            while (temp > 10):
                time.sleep(0.5)
                temp = self._waage.get_weight_level()
        else:
            print("zu hoher Füllstand!")
            
        time.sleep(3)
        self.pwm.set_pwm(0, 0, self.servo_zu)
        time.sleep(0.5)
        self.pwm.set_pwm(0, 0, 0)
        self.pwm.set_pwm(2, 0, 0)
            
        
    def stopDoseMotor(self):        
        self.pwm.set_pwm(0, 0, self.servo_zu)
        time.sleep(0.5)
        self.pwm.set_pwm(0, 0, 0)
        self.pwm.set_pwm(2, 0, 0)
        #GPIO.cleanup()
            
    def stopMotors(self):
        #try:
        self.pwm.set_pwm(2, 0, 0)
        self.pwm.set_pwm(0, 0, 0)
        #except:
            #print("Programm wurde geschlossen!")
        #finally:
            #GPIO.cleanup()
    
    def addSomeBones(self):
        print("Nachjustieren")
        self.pwm.set_pwm(0,0,self.servo_auf)
        time.sleep(0.21)
        self.pwm.set_pwm(0,0,self.servo_zu)
        time.sleep(0.4)
      
    def abfuellen(self, max_weight, current_weight):
        print('max weights:', max_weight)
        print('curr weights:', current_weight)
        wanted_weight = max_weight - 3
        val_A = current_weight
        #fill_level = self._waage.get_weight_level
        if not self.is_servo_open:
            self.is_servo_open = True
            if ((wanted_weight - 180) >= 0):
                while val_A < wanted_weight and self.kill_thread == False:   
                    print("Aktuelles Gewicht: ", val_A)
                    #print("Aktueller Füllstand: ", fill_level)
                    #magic number haengt von wert self.servo_auf ab
                    #durchschnittlich 80-90g Schritte
                    #if val_A <= wanted_weight - 795:
                    if val_A <= wanted_weight - 795:
                        print("Dosiere grob für extrem hohe Gewichte")
                        self.pwm.set_pwm(0,0,self.servo_auf)
                        time.sleep(3.7)
                        self.pwm.set_pwm(0,0,self.servo_zu)
                        time.sleep(0.3)
                        
                    elif val_A <= wanted_weight - 495:
                        print("Dosiere grob für hohe Gewichte")
                        self.pwm.set_pwm(0,0,self.servo_auf)
                        time.sleep(2)
                        self.pwm.set_pwm(0,0,self.servo_zu)
                        time.sleep(0.3)
                       
                    elif val_A <= wanted_weight - 180:
                        print("Dosiere grob")
                        self.pwm.set_pwm(0,0,self.servo_auf)
                        time.sleep(0.9)
                        self.pwm.set_pwm(0,0,self.servo_zu)
                        time.sleep(0.3)
                    
                    #Dosiert je iteration ca 50g
                    elif val_A <= wanted_weight - 70:
                        print("Dosiere mittelgrob")
                        self.pwm.set_pwm(0,0,self.servo_auf)
                        #ca 30g
                        #time.sleep(0.5)
                        time.sleep(0.55)
                        self.pwm.set_pwm(0,0,self.servo_zu)
                        time.sleep(0.4)
                        
                    #durchschnittlich 20g schritte
                    elif val_A <= wanted_weight - 15:
                        print("Dosiere feiner")
                        self.pwm.set_pwm(0,0,self.servo_auf)
                        time.sleep(0.3)
                        self.pwm.set_pwm(0,0,self.servo_zu)
                        time.sleep(0.6)
                        
                    else:
                        #durchschnittlich 1-3g Schritte
                        print("Dosiere letzte Bohnen")
                        self.pwm.set_pwm(0,0,self.servo_auf)
                        time.sleep(0.22)
                        self.pwm.set_pwm(0,0,self.servo_zu)
                        time.sleep(0.4)
                        
                    val_A = self._waage.get_weight_dose()
                    print("iteration")  
            
            #Einstellgewicht (wanted_weight) unter 180g
            #andere grenzwerte
            #andere zeit    
            else:
                while val_A < wanted_weight:
                    print("Aktuelles Gewicht: ", val_A)
                    print("Dosiere von Anfang an mittelgrob")
                    if val_A <= wanted_weight - 70:
                        self.pwm.set_pwm(0,0,self.servo_auf)
                        time.sleep(0.35)
                        self.pwm.set_pwm(0,0,self.servo_zu)
                        time.sleep(0.3)
                        
                    elif val_A <= wanted_weight - 20:                
                        print("Dosiere feiner")
                        self.pwm.set_pwm(0,0,self.servo_auf)                   
                        time.sleep(0.28)
                        self.pwm.set_pwm(0,0,self.servo_zu)
                        time.sleep(0.4)
                    else:
                        print("Dosiere letzte Bohnen")
                        self.pwm.set_pwm(0,0,self.servo_auf)
                        time.sleep(0.22)
                        self.pwm.set_pwm(0,0,self.servo_zu)
                        time.sleep(0.4)
                    val_A = self._waage.get_weight_dose()
                    print("iteration")
                
            self.pwm.set_pwm(0, 0, self.servo_zu)
            self.is_servo_open = False
            print("Fertig")
            time.sleep(0.5)
            self.pwm.set_pwm(0, 0, 0)
            val_A = self._waage.get_weight_dose()
            print("Endgewicht: ", val_A)
            return True
        else:
            return False
    '''
    Abfüllmechanismus
    Dosierung bis Wunschgewicht erreicht
    '''
    def test_abfuellen(self, wanted_weight, current_weight):
        print('max weights:', wanted_weight)
        print('curr weights:', current_weight)
        currWeight = current_weight
    
        if not self.is_servo_open:
            #self.pwm.set_pwm(0, 0, self.servo_open)
            self.is_servo_open = True
            while currWeight < max_weight:
                print(currWeight)
                #magic number haengt von wert self.servo_auf ab
                #durchschnittlich 80-90g Schritte
                if ((max_weight - 180) >= 0):
                    if currWeight <= max_weight - 180:
                        self.pwm.set_pwm(0,0,self.servo_open)
                        print("Dosiere grob")
                        #durchschnittlich 10g schritte
                    elif currWeight <= max_weight - 25:
                        print("Dosiere nun feiner")
                        self.pwm.set_pwm(0,0,self.servo_closed)
                        time.sleep(0.5)
                        self.pwm.set_pwm(0,0,self.servo_fine)
                        time.sleep(0.35)
                        self.pwm.set_pwm(0,0,self.servo_closed)
                    else:
                        #durchschnittlich 1-3g Schritte
                        print("Dosiere letzte Bohnen")
                        self.pwm.set_pwm(0,0,self.servo_closed)
                        time.sleep(0.5)
                        self.pwm.set_pwm(0,0,self.servo_lastGramm)
                        time.sleep(0.18)
                        self.pwm.set_pwm(0,0,self.servo_closed)
                #Einstellgewicht (max_weight) unter 180g
                #andere grenzwerte
                #andere zeit
                elif currWeight <= max_weight - 25:                
                    print("Dosiere von Anfang an feiner")
                    self.pwm.set_pwm(0,0,self.servo_closed)
                    time.sleep(0.5)
                    self.pwm.set_pwm(0,0,self.servo_fine)                   
                    time.sleep(0.4)
                    self.pwm.set_pwm(0,0,self.servo_closed)
                else:
                    print("Dosiere letzte Bohnen")
                    self.pwm.set_pwm(0,0,self.servo_closed)
                    time.sleep(0.5)
                    self.pwm.set_pwm(0,0,self.servo_lastGramm)
                    time.sleep(0.18)
                    self.pwm.set_pwm(0,0,self.servo_closed)
                currWeight = self._waage.get_weight_dose()
            print("Fertig")    
            self.pwm.set_pwm(0, 0, self.servo_closed)
            self.is_servo_open = False
            return True
        else:
            return False