import tkinter as tk
import time
import sys
import csv
import os
import waage
import servo
from datetime import datetime
from threading import *
from tkinter import messagebox
#from PIL import Image

# Gui Klasse
class App(tk.Frame):
    # Konstruktor
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        # Eingestellter Wert zum wiegen initialisieren
        self.wanted_weight = 0
        self._waage = waage.Waage()
        self._servo = servo.Servo()
        time.sleep(0.5)
        self._create_buttons_main()
        self._create_labels_main()
        self._create_slider_main()
        self._update_clock_main()
                

    # getter
    def _get_wanted_weight(self):
        return self.wanted_weight

    # setter 
    def _set_wanted_weight(self, wanted_weight):
        self.wanted_weight = wanted_weight

    def _get_weight_dose(self):
        return self._waage.get_weight_dose()

    def _get_weight_level(self):
        return self._waage.get_weight_level()

    def _actionBeenden_main(self):
        print("Programm geschlossen")
        fenster = self.master        
        fenster.destroy()
        fenster.quit()
        os.system("sudo shutdown -h now")        

    def _update_clock_main(self):
        now = time.strftime("%H:%M:%S")
        self._clock_label_1.configure(text=now)
        self.after(1000, self._update_clock_main)

    #def _update_fill_level_main(self):
        #now = time.strftime("%H:%M:%S")
        #fill_level_main = self._waage.get_weight_level()
        #self.fill_level_main_label.config(text = fill_level_main)
        #self.after(1000, self._update_fill_level_main)

    #Anzeige Eingestellter Wert
    def _show_values_main(self):
        sliderwert = self.slider.get()
        self.sliderwert_label.config(text = sliderwert)
        self.wanted_weight = sliderwert
 
    #Anzeige Eingestellter Wert zurücksetzen
    def _reset_values_main(self):
        self.sliderwert_label.config(text = "0")

    def _set_choice(self, weight):
        self.wanted_weight = weight
        self.sliderwert_label.config(text = str(self.wanted_weight))
        self._abfuellung_fenster()
    
    def empty_fill_level(self):
        fill_level = self._waage.get_weight_level()
        time.sleep(0.3)
        if fill_level > 1000:
            messagebox.showwarning("Fehlermeldung", "In der Schütte befinden sich zu viele Bohnen!", parent = fenster)
        self._servo.empty_fill_level(self._waage.get_weight_level())
        time.sleep(0.3)
        self.schuette_leeren_text_label.config(text = "Bitte den Fußtaster betätigen")
        self._servo.openWithSwitch(self.wanted_weight)
        self.schuette_leeren_text_label.config(text = "")
        self.fill_level_main_label.config(text = str(self._waage.get_weight_level()))
        time.sleep(0.3)
        
    def threading_schuette_leeren(self):
        # Startet abfüllen mit Thread
        self.t3 = Thread(target=self.empty_fill_level)
        self.t3.start()
        
    #Alle Buttons erstellen    
    def _create_buttons_main(self):
        #Button Main Fenster
        fenster = self.master
        
        self.empty_level_button = tk.Button(fenster,
                                    text = "Schütte leeren",
                                    fg = "black",
                                    bg = "white",
                                    command = self.threading_schuette_leeren, 
                                    activebackground = "blue",
                                    activeforeground = "black")
        
        self.empty_level_button.place(relx = 0.88,
                            rely = 0.7,
                            width = 250,
                            height = 80,
                            anchor = tk.CENTER)
        
        abfuell_fenster_oeffnen = tk.Button(fenster,
                                            text = "Abfüllung",
                                            command = self._abfuellung_fenster,
                                            fg = "black",
                                            bg = "white",
                                            activebackground = "green",
                                            activeforeground = "white")

         #Buttons fuer neue Fenster platzieren
        abfuell_fenster_oeffnen.place(relx = 0.13, rely = 0.65, width = 250, height = 80, anchor = tk.CENTER)

        beenden_button = tk.Button(fenster,
                                   text = "Beenden",
                                   command = self._actionBeenden_main,
                                   fg = "black",
                                   bg = "white",
                                   activebackground = "red",
                                   activeforeground = "white")

        beenden_button.place(relx = 0.88,
                             rely = 0.85,
                             width = 250,
                             height = 80,
                             anchor = tk.CENTER)

        #Button, um das Einstellgewicht zu uebernehmen
        ok_button = tk.Button(fenster,
                              text = "Wert übernehmen",
                              command = self._show_values_main,
                              fg = "black",
                              bg = "white",
                              activebackground = "green",
                              activeforeground = "white")

        ok_button.place(relx = 0.11,
                        rely = 0.40,
                        width = 200,
                        height = 50,
                        anchor = tk.CENTER)
        
        #Button, um das Einstellgewicht zurueckzusetzen
        reset_button = tk.Button(fenster,
                                 text = "Wert zurücksetzen",
                                 command = self._reset_values_main,
                                 fg = "black",
                                 bg = "white",
                                 activebackground = "red",
                                 activeforeground = "white")

        reset_button.place(relx = 0.11, rely = 0.50, width = 200, height = 50, anchor = tk.CENTER)

        #Button, um das Einstellgewicht zu uebernehmen
        button_250 = tk.Button(fenster,
                               text = "250",
                               font = ("Arial", 18),
                               command = lambda x=250: self._set_choice(x),
                               fg = "black",
                               bg = "white",
                               activebackground = "blue",
                               activeforeground = "white")
        
        #Button, um das Einstellgewicht zu uebernehmen
        button_500 = tk.Button(fenster,
                               text = "500",
                               font = ("Arial", 18),
                               command = lambda x=500: self._set_choice(x),
                               fg = "black",
                               bg = "white",
                               activebackground = "blue",
                               activeforeground = "white")
                               
        
        #Button, um das Einstellgewicht zu uebernehmen
        button_1000 = tk.Button(fenster,
                                text = "1000",
                                font = ("Arial", 18),
                                command = lambda x=1000: self._set_choice(x),
                                fg = "black",
                                bg = "white",
                                activebackground = "blue",
                                activeforeground = "white")
       
        #Button, um das Einstellgewicht zu uebernehmen
        button_250.place(relx = 0.38, rely = 0.5, width = 100, height = 80, anchor = tk.CENTER)
        button_500.place(relx = 0.48, rely = 0.5, width = 100, height = 80, anchor = tk.CENTER)
        button_1000.place(relx = 0.58, rely = 0.5, width = 100, height = 80, anchor = tk.CENTER)
          
        #button_250.bind('<Button-1>', button_250.config(bg = 'red', fg = 'black'))
        #button_500.bind('<Button-2>', button_500.config(bg = 'green', fg = 'black'))
        #button_1000.bind('<Button-3>', button_1000.config(bg = 'blue', fg = 'black'))
        
        #ok_button.bind('<Button-1>', ok_button.config(bg = 'white', fg = 'black'))
        #reset_button.bind('<Button-1>', reset_button.config(bg = 'white', fg = 'black'))
        #abfuell_fenster_oeffnen.bind('<Button-1>', abfuell_fenster_button.config(bg = 'white', fg = 'black'))

        # Events
        #button_250.bind('<Button-1>', self._fast_choice_main(250))
        #button_500.bind('<Button-1>', self._fast_choice_main(500))
        #button_1000.bind('<Button-1>', self._fast_choice_main(1000))

    #Erstellt die Labels
    def _create_labels_main(self):
        fenster = self.master
        
        self.schuette_leeren_text_label = tk.Label(text = "",
                                                   fg = "red",
                                                   bg = "white",
                                                   font = ("Arial", 18))
        
        self.schuette_leeren_text_label.place(relx = 0.5,
                                              rely = 0.8,
                                              anchor = tk.CENTER)

        self._clock_label_1 = tk.Label(text = "",
                              fg = "black",
                              font = ("Arial", 18),
                              bg = "white")
        
        self._clock_label_1.place(relx = 0.94,
                         rely = 0.04,
                         anchor = tk.CENTER)  


        self.eingestellter_wert_label = tk.Label(fenster,
                                         bg = "white",
                                         text = "Eingestellter Wert [g]: ",
                                         font = ("Arial", 15))


        self.eingestellter_wert_label.place(relx = 0.11,
                                    rely = 0.75,
                                    width = 200,
                                    height = 50,
                                    anchor = tk.CENTER)
        
        self.sliderwert_label = tk.Label(fenster,
                                         bg = "white",
                                         text = str(self.wanted_weight),
                                         font = ("Arial", 18))
        
        self.sliderwert_label.place(relx = 0.22,
                                    rely = 0.75,
                                    width = 50,
                                    height = 25,
                                    anchor = tk.CENTER)

        
        self.fill_label = tk.Label(fenster,
                                    bg = "white",
                                    text = "Füllstand [g]: ",
                                    font = ("Arial", 15))
        
        self.fill_label.place(relx = 0.08,
                                    rely = 0.85,
                                    width = 200,
                                    height = 25,
                                    anchor = tk.CENTER)
        
        self.fill_level_main_label = tk.Label(fenster,
                                        text = str(self._waage.get_weight_level()),
                                        bg = "white",
                                        font = ("Arial", 18))

        self.fill_level_main_label.place(relx = 0.22,
                                    rely = 0.85,
                                    width = 150,
                                    height = 80,
                                    anchor = tk.CENTER)
    
    #Erstellt den Schieberegler zum Einstellen des Abfuellgewichtes
    def _create_slider_main(self):
        #Schieberegler zum einstellen des gewuenschten Abfuellgewichtes
        fenster = self.master
        self.slider = tk.Scale(fenster,
                               from_ = 0,
                               to = 1000,
                               orient = tk.HORIZONTAL,
                               tickinterval = 50,
                               resolution = 5)
        
        self.slider.config(bg = "white",
                           borderwidth = 4,
                           highlightbackground = "grey",
                           sliderlength = 50,
                           troughcolor = "black",
                           width = 25)

        self.slider.place(relx = 0.5,
                          rely = 0.25,
                          width = 1200,
                          height = 80,
                          anchor = tk.CENTER)
    

    #Fenster Abfüllung
    def _abfuellung_fenster(self):
        fenster = self.master
        abfuell_fenster = tk.Toplevel(fenster)
        w,h = abfuell_fenster.winfo_screenwidth(), abfuell_fenster.winfo_screenheight()
        abfuell_fenster.geometry("%dx%d+0+0" % (w, h))
        abfuell_fenster.title("Abfüllung")
        #abfuell_fenster.overrideredirect(1)
        abfuell_fenster.config(background = "#FFFFFF")

        def _action_back():
            abfuell_fenster.destroy()
            self.fill_level_main_label.config(text =str(self._waage.get_weight_level()))
            
        def _stop_abfuellen():
            self._servo.kill_thread = True
            self._servo.stopDoseMotor()
            self._servo.stopMotors()
            print("STOPP!")
        
        def threading_abfuellen():
            # Startet abfüllen mit Thread
            self.t1 = Thread(target=_abfuellen)
            self._servo.kill_thread = False
            print("START!")
            self.t1.start()
            
        def threading_stop():
            # Stop abfüllung mit Thread
            t2=Thread(target=_stop_abfuellen)
            t2.start()
         
        def _abfuellen():
            valider_Fuellstand = False
            fertig = False
            
            #Status aktualisieren
            self.status_abfuellung_label.config(text = "Start-Button wurde gedrückt.")  
            #self.wert_fuellstand_label.config(text = str(fill_level))
            
            while self._servo.kill_thread == False:                
                #Füllstand holen
                fill_level = self._waage.get_weight_level()
                #Zielgewicht holen
                target_weight = self.wanted_weight
                #Ausreichender Füllstand
                valider_Fuellstand = fill_level > (target_weight + 200)
                print('1')                
                while valider_Fuellstand == False and self._servo.kill_thread == False:
                    print('2')
                    #Status aktualisieren
                    self.status_abfuellung_label.config(text = "Bitte Schütte befüllen!")
                    fill_level = self._waage.get_weight_level()
                    valider_Fuellstand = fill_level > (target_weight + 200)
                    if valider_Fuellstand:
                        time.sleep(10)
                    fill_level = self._waage.get_weight_level()
                    #Füllstand auf Display aktualsien
                    self.wert_fuellstand_label.config(text = str(fill_level))
                    #debug
                    now = time.strftime("%H:%M:%S")
                    print('Zu geringer Füllstand', now)
                    if self._servo.kill_thread == True:
                        self.status_abfuellung_label.config(text = "ABFÜLLUNG GESTOPPT!")
                
                while valider_Fuellstand == True and self._servo.kill_thread == False:                    
                    thread_numbers = active_count()
                    if thread_numbers > 2:
                        self.status_abfuellung_label.config(text = "ABFÜLLUNG GESTOPPT!")                        
                        self._servo.kill_thread = True
                        messagebox.showwarning("Fehlermeldung", "Der Start-Button wurde zu oft gedrückt.", parent = abfuell_fenster)
                        break
                    
                    print('3')
                    #Status aktualisieren
                    self.status_abfuellung_label.config(text = "Abfüllungsprozess läuft.")
                    #Startzeit
                    start = time.time()                        
                    actual_weight = self._waage.get_weight_dose()
                    #Abfüllung
                    fertig = self._servo.abfuellen(target_weight, actual_weight)                    
                    #Endzeit
                    end = time.time()
                    #Abfüllzeit
                    diff = end-start
                    time.sleep(0.3)
                    #Abgefüllltes Gewicht
                    ergebnis = int(self._waage.get_weight_dose())
                    
                    dosiertIn = float(("%0.2f"%diff))
                    #Ausgabe auf der Oberfläche
                    self.wert_zeit_messung_label.config(text = str(dosiertIn))
                    #Prüfen ob das Gewicht in Toleranzbereich liegt                    
                    if ergebnis < (target_weight - 2):
                        self._servo.addSomeBones()
                        time.sleep(0.5)
                        
                    ergebnis = int(self._waage.get_weight_dose())
                    #Ausgabe auf der Oberfläche
                    self.wert_waage_label.config(text = str(ergebnis))
                    
                    str_goodResult = self._waage.isGoodResult(target_weight,ergebnis)
                    if str_goodResult == "IN":
                        self.wert_waage_label.config(bg = "green")
                    else:
                        self.wert_waage_label.config(bg = "red")

                    #Prüfen ob Füllstand noch valide
                    fill_level = self._waage.get_weight_level()
                    valider_Fuellstand = fill_level > (target_weight + 200)
                    self.wert_fuellstand_label.config(text = str(fill_level))
                    
                    if self._servo.kill_thread == True:
                        self.status_abfuellung_label.config(text = "ABFÜLLUNG GESTOPPT!")
                                            
                    #Fußtaster abfragen
                    if fertig and self._servo.kill_thread == False:
                        self.status_abfuellung_label.config(text = "Warten auf Fußtaster.")
                        self._servo.openWithSwitch(self.wanted_weight)
                        if self._servo.kill_thread == True:
                            self.status_abfuellung_label.config(text = "ABFÜLLUNG GESTOPPT!") 
                        self.wert_waage_label.config(background = "#FFFFFF")
                        #Zeit bis zur nächsten Abfüllung
                        time.sleep(1)
                        
                        #Daten für das Log-File
                        date = datetime.today()
                        info = {"Datum": date,
                                    "Zielgewicht[g]": target_weight,
                                    "Abgefülltes_Gewicht[g]": ergebnis,
                                    "Dauer[s]": dosiertIn,
                                    "Differenz Idealgewicht[g]": ergebnis-target_weight,
                                    "Toleranzbereich": str_goodResult,
                                    "Füllstand[g]": fill_level}
                        
                        log_exists = os.path.isfile("log.csv")
                    
                        with open("log.csv", "a") as f:
                            wr = csv.DictWriter(f, fieldnames=info.keys())
                            if not log_exists:
                                wr.writeheader()
                            wr.writerow(info)
                            
                        self.wert_waage_label.config(text = "0")
                        self.wert_zeit_messung_label.config(text = "0.00")    
                        fertig = False                  
                        break
            

        def _create_buttons_abfuellen():

            self.abfuellen_button = tk.Button(abfuell_fenster,
                                    text = "Start",
                                    font = ("Arial", 15),
                                    command = threading_abfuellen, 
                                    activebackground = "green",
                                    activeforeground = "white")
        
            self.abfuellen_button.place(relx = 0.5,
                                rely = 0.4,
                                width = 200,
                                height = 50,
                                anchor = tk.CENTER)
        
            self.stop_button = tk.Button(abfuell_fenster,
                                        text = "Stop",
                                        font = ("Arial", 15),
                                        command = threading_stop,
                                        activebackground = "red",
                                        activeforeground = "white")
            
            self.stop_button.place(relx = 0.5,
                                    rely = 0.5,
                                    width = 150,
                                    height = 50,
                                    anchor = tk.CENTER)
                        
            self.abfuell_fenster_exit_button = tk.Button(abfuell_fenster,
                                                    text = "Zurück",
                                                    font = ("Arial", 13),
                                                    command = _action_back,
                                                    activebackground = "red",
                                                    activeforeground = "black")    
            # Buttons platzieren
            self.abfuell_fenster_exit_button.place(relx = 0.9,
                                                rely = 0.9,
                                                width = 200,
                                                height = 50,
                                                anchor = tk.CENTER)

        def _create_labels_abfuellen():

            self.text_fuellstand_label = tk.Label(abfuell_fenster,
                                                bg = "white",
                                                font = ("Arial", 15),
                                                text = "Füllstand [g]")
            
            self.text_fuellstand_label.place(relx = 0.4,
                                        rely = 0.85,
                                        width = 250,
                                        height = 25,
                                        anchor = tk.CENTER)
            
            self.wert_fuellstand_label = tk.Label(abfuell_fenster,
                                                bg = "white",
                                                font = ("Arial", 15),
                                                text = str(self._waage.get_weight_level()))
            
            self.wert_fuellstand_label.place(relx = 0.6,
                                        rely = 0.85,
                                        width = 100,
                                        height = 25,
                                        anchor = tk.CENTER)
            
            
            self.text_einstellgewicht_label = tk.Label(abfuell_fenster,
                                                bg = "white",
                                                font = ("Arial", 15),
                                                text = "Eingestelltes Gewicht [g]")
            
            self.text_einstellgewicht_label.place(relx = 0.4,
                                        rely = 0.65,
                                        width = 350,
                                        height = 25,
                                        anchor = tk.CENTER)
            
            self.wert_einstellgewicht_label = tk.Label(abfuell_fenster,
                                                bg = "white",
                                                font = ("Arial", 15),
                                                text = str(self.wanted_weight))
            
            self.wert_einstellgewicht_label.place(relx = 0.6,
                                        rely = 0.65,
                                        width = 100,
                                        height = 25,
                                        anchor = tk.CENTER)

            
            self.text_waage_label = tk.Label(abfuell_fenster,
                                                bg = "white",
                                                font = ("Arial", 15),
                                                text = "Endgewicht [g]")
            
            self.text_waage_label.place(relx = 0.4,
                                        rely = 0.7,
                                        width = 150,
                                        height = 25,
                                        anchor = tk.CENTER)
            
            self.wert_waage_label = tk.Label(abfuell_fenster,
                                                bg = "white",
                                                font = ("Arial", 15),
                                                text = str(self._waage.get_weight_dose()))
            
            self.wert_waage_label.place(relx = 0.6,
                                        rely = 0.7,
                                        width = 100,
                                        height = 25,
                                        anchor = tk.CENTER)
            
            
            self.text_zeit_messung_label = tk.Label(abfuell_fenster,
                                                bg = "white",
                                                font = ("Arial", 15),
                                                text = "Abfüllzeit [s]")
            
            self.text_zeit_messung_label.place(relx = 0.4,
                                        rely = 0.75,
                                        width = 150,
                                        height = 25,
                                        anchor = tk.CENTER)
            
            self.wert_zeit_messung_label = tk.Label(abfuell_fenster,
                                                bg = "white",
                                                font = ("Arial", 15),
                                                text = "0")
            
            self.wert_zeit_messung_label.place(relx = 0.6,
                                        rely = 0.75,
                                        width = 150,
                                        height = 25,
                                        anchor = tk.CENTER)
            
            #self.statustext_abfuellung_label = tk.Label(abfuell_fenster, 
                                    #bg = "white", 
                                    #font = ("Arial", 15),
                                    #text = "Status: ")

            #self.statustext_abfuellung_label.place(relx = 0.4,
                                        #rely = 0.25,
                                        #width = 80,
                                        #height = 25,
                                        #anchor = tk.CENTER)

            self.status_abfuellung_label = tk.Label(abfuell_fenster,
                                        #borderwidth = 2,
                                        #relief= "ridge",
                                        bg = "white",
                                        fg = "red",
                                        font = ("Arial", 18),
                                        text = "Warte auf Start")

            self.status_abfuellung_label.place(relx = 0.5,
                                        rely = 0.25,
                                        width = 600,
                                        height = 25,
                                        anchor = tk.CENTER)
            
            self.mare_img = tk.PhotoImage(file = "/home/pi/Desktop/logo.png")
            
            self.toplevel_mare_label = tk.Label(abfuell_fenster,
                                        bg = "white",
                                        image = self.mare_img)
            
            self.toplevel_mare_label.place(relx = 0.42,
                                  rely = 0.001,
                                  width = 180,
                                  height = 120)
            
                    
        #def update_label_weight(self, y):
            #self.wert_waage_label.after(1000, self.update_label_weight)
            #def _update_label(self, fill_data, dose_data):
            #self.wert_fuellstand_label.config(text = str(fill_data))
            #self.wert_waage_label.config(text = str(dose_data)
            
        #def _update_fill_level():
            #now = time.strftime("%H:%M:%S")
            #fill_level = self._waage.get_weight_level()
            #self.wert_fuellstand_label.configure(text= str(fill_level))
            #self.wert_fuellstand_label.after(200, _update_fill_level)

        def _update_weight():
            #now = time.strftime("%H:%M:%S")
            curr_weight = max(0,int(self._waage.get_weight_dose()))
            #fill_level = self._waage.get_weight_level()
            #self.wert_fuellstand_label.configure(text= str(fill_level))
            self.wert_waage_label.configure(text= str(curr_weight))
            #self.wert_waage_label.after(2500, _update_weight)
            #self.wert_fuellstand_label.after(1000, _update_weight)
            
        _create_buttons_abfuellen()
        _create_labels_abfuellen()
        
        _update_weight()
        #abfuell_fenster.mainloop()

#Mainfunktion -ausführen der App
def main():
    fenster = tk.Tk()
    w, h = fenster.winfo_screenwidth(), fenster.winfo_screenheight()
    fenster.geometry("%dx%d+0+0" % (w, h))
    fenster.title("Mare Kaffee")
    #fenster.overrideredirect(1)
    fenster.config(background = "#fff")
    
    mare_img = tk.PhotoImage(file = "/home/pi/Desktop/logo.png")
    
    mare_label_main = tk.Label(fenster,
                                bg = "white",
                                image = mare_img )
    
    mare_label_main.place(relx = 0.42,
                          rely = 0.001,
                          width = 180,
                          height = 120)
    
    app = App(fenster)

    #app._update_fill_level_main()
    app._update_clock_main()
    #app.wert_waage_label.after(1000, _update_weight())
    
    app.mainloop()

if __name__ == "__main__":
    main()