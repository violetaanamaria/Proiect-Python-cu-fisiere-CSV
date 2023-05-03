import sys # modulul ofera o serie de capabilitati legate de lucrul cu sistemul de operare
from tkinter import * #libraria pentru interfata grafică
import csv #libraria pentru prelucrarea fisierelor csv
import matplotlib.pyplot as plt #librarie pentru plotarea graficelor
import random #librarie pnetru a importa numere aleatorii
import socket #librarie pentru conectarea la TCP
import queue # librarie pentru urilizarea cozilor
import serial #librarie pentru conectarea la serial
import time #modulul time permite efectuarea operatiunilor comune in programare si formatarea timpului conform cu necesitatile
import threading #librarie pentru utilizarea firelor de executie

def csv():  #definim functia utilizată pentru obtinerea unor fisiere noi csv
    import csv #am importat biblioteca csv in interiorul functiei pentru a nu avea erori
    with open ('Date.csv','r' ,newline ='') as fisier: #se deschide fisierul din care vom prelua datele
        var = csv.reader(fisier,delimiter = ',', quotechar = '|') #citirea datelor din fisier utilizand metoda 'reader' si stocarea acestora intr-o lista

        for rnd in var: # parcurgerea pe linii a datelor din fisier
            #creearea unor noi fisiere csv in care se vor sorta si stoca datele din fisierul 'Date.csv'
            with open ('Temperaturi.csv', 'a', newline ='') as temp, \
             open ('Umiditati.csv', 'a',newline ='') as umid,\
             open ('Viteza.csv', 'a', newline ='') as vit,\
             open ('Prezenta.csv', 'a', newline ='') as prez:
                #definirea variabilelor în care se vor scrie, prin apelarea metodei 'writer', valorile ce vor fi stocate în noul fisier csv creat si scrierea proriu-zisa a datelor
                temp_scris = csv.writer(temp, delimiter = ',', quotechar = '|') #definirea variabilei 'temp_scris'
                temp_scris.writerow([rnd[0],rnd[1],rnd[2],rnd[3],rnd[10]]) #stocarea datelor
              
                umid_scris = csv.writer(umid, delimiter = ',', quotechar = '|') #definirea variabilei 'umid_scris'
                umid_scris.writerow([rnd[0],rnd[4],rnd[5],rnd[6],rnd[10]]) #stocarea datelor
                
     
                vit_scris = csv.writer(vit, delimiter = ',', quotechar = '|') #definirea variabilei 'vit_scris'
                vit_scris.writerow([rnd[0],rnd[7],rnd[10]]) #stocarea datelor
                
           
                prez_scris = csv.writer(prez, delimiter = ',', quotechar = '|') #definirea variabilei 'prez_scris'
                prez_scris.writerow([rnd[0], rnd[8],rnd[9],rnd[10]]) #stocarea datelor

#se crează liste în care vom stoca datele
indexNo = [] #index
temp1 = [] #temperatura 1
temp2 = [] #temperatura 2
temp3 = [] #temperatura 3
umid2 = [] #umiditatea 2
umid1 = [] #umiditatea 1
umid3 = [] #umiditatea 3
vit1= []   #viteza
prez1 = [] #prezenta 1
prez2 = [] #prezenta 2
timp = []  #timp
var1=[]
var2=[]
var3=[]

def grafice(): #definim functia utilizată pentru obtinerea graficelor
    import csv
    with open ('Date.csv', 'r', newline ='') as date: #se deschide fisierul din care vom prelua datele si utilizam metoda 'r' pentru citire
                date_scris = csv.reader(date, delimiter = ',', quotechar = '|') #citirea datelor din fisier utilizand metoda 'reader' si stocarea acestora intr-o lista
                next(date_scris) #trecerea peste prima linie, deoarece nu contine date
                for randNou in date_scris: # parcurgerea pe linii a datelor din fisier
                    #stocarea datelor din fisier in listele create mai devreme pentru a realiza graficele
                    temp1.append(float(randNou[1]))
                    temp2.append(float(randNou[2]))
                    temp3.append(float(randNou[3]))
                    umid1.append(float(randNou[4]))
                    umid2.append(float(randNou[5]))
                    umid3.append(float(randNou[6]))
                    vit1.append(float(randNou[7]))
                    prez1.append(float(randNou[8]))
                    prez2.append(float(randNou[9]))
                    timp.append((randNou[10]))
                #realizarea graficelor    
                plt.figure(1) #declararea figurii
                plt.plot (timp, temp1, label = 'Temp 1') #crearea graficelor pentru fiecare valoare a temperaturii
                plt.plot (timp, temp2, label = 'Temp 2')
                plt.plot (timp, temp3, label = 'Temp 3')
                plt.xlabel ("timp") #denumirea axei x
                plt.ylabel ("Temperatura") #denumirea axei y
                plt.title ('temp (timp)') #titlul graficului
                plt.legend() # legenda graficului
                plt.xticks ([0,50,99]) #dimensiunile axelor
                plt.show() # afisarea graficului

                    
                plt.figure(2) #declararea figurii
                plt.plot (timp, umid1, label = 'Umiditate 1') #crearea graficelor pentru fiecare valoare a umiditatii
                plt.plot (timp, umid2, label = 'Umiditate 2')
                plt.plot (timp, umid3, label = 'Umiditate 3')
                plt.xlabel ("timp") #denumirea axei x
                plt.ylabel ("Umiditate") #denumirea axei y
                plt.title ('umiditate (timp)') #titlul graficului
                plt.legend() # legenda graficului
                plt.xticks ([0,50,99]) #dimensiunile axelor
                plt.show() # afisarea graficului
                
      
                plt.figure(3) #declararea figurii
                plt.plot (timp, vit1, label = 'Viteza')
                plt.xlabel ("timp")#denumirea axei x
                plt.ylabel ("Viteza") #denumirea axei y
                plt.title ('viteza (timp)') #titlul graficului
                plt.xticks ([0,50,99])
                plt.show() # afisarea graficului

                plt.figure(4) #declararea figurii
                plt.plot (timp, prez1, label = 'Prezenta 1')
                plt.plot (timp, prez2, label = 'Prezenta 2')
                plt.xlabel ("timp") #denumirea axei x
                plt.ylabel ("Prezenta") #denumirea axei y
                plt.title ('prezenta (timp)') #titlul graficului
                plt.legend() # legenda graficului
                plt.xticks ([0,50,99]) #dimensiunile axelor
                plt.show() # afisarea graficului



q = queue.Queue() #se creaza cozile pe care le vom utiliza in organizarea valorilor 
p = queue.Queue()

def serverTCP(): #definim functia ce va realiza conectarea la TCP 
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crearea unui obiect a clasei socket
    #socket.AF_INET = tipul de adresa prin care comunica (Internet Protocol v4 addresses)
    #socket.SOCK_STREAM = tipul de socket (specific TCP)
    host = "localhost" #alegerea host-ului
    port = 9999 # alegerea portului
    serversocket.bind((host,port)) #crearea legaturii dintre host si port
    #serversocket.settimeout(3)
    serversocket.listen(5) # ascultarea conexiunilor de intrare

    clientsocket,addr = serversocket.accept()
    while True: # programul se executa cat timp este adevarat
        if ( q.empty()!=True): #se verifica daca coada nu este goala
            var = q.get() #se vor extrage datele din coada
            clientsocket.send(var.encode()) #se trimite valoare din lista catre client
       
def scriitor(): #definim functia ce va crea un fisier csv     
    import csv
    while True:
        var = p.get() #sunt extrase valorile cozii
        #creearea unui nou fisier csv in care se vor stoca datele citite pe TPC'
        with open('Date_TCP.csv', 'a', newline = '') as variabila:
            variabila_writer = csv.writer(variabila, delimiter = ',', quotechar =' ', quoting = csv.QUOTE_MINIMAL)
            variabila_writer.writerow(str(var).split())
            
def RS232_generat():  #definim functia ce va produce date aleatorii
    k=1
    while k<=50:
         a= str(k)+","+str(random.randint(60, 90))+","+str(random.randint(58, 88))+","+str(random.randint(59, 92)) + '\n' #se creaza o linie cu numere aleatorii  
         q.put(a) #se adauga linia citita
         p.put(a) #se adauga linia citita
         k+=1 #incrementare

def conectare_TCP(): #functie de activare a firelor cu ajutorul butonului 3
    fir1 = threading.Thread(target = RS232_generat, name = 'Fir1')
    #crearea unui fir de executie pentru executia functiei de scriere a fisierului csv
    fir1.start() #activarea firului
    fir2 = threading.Thread(target = serverTCP, name = 'Fir2')
    #crearea unui fir de executie pentru conexiunea la 
    fir2.start() #activarea firului

def grafic_TCP(): #crearea graficului cu datele citite de pe TCP
    import csv
    #se deschide fisierul din care vom prelua datele si utilizam metoda 'r' pentru citire
    with open ('Date_TCP.csv','r' ,newline ='') as vari:
        vari_scris = csv.reader(vari, delimiter = ',', quotechar = '|') #citirea datelor din fisier utilizand metoda 'reader' si stocarea acestora intr-o lista
       
        for randNou in vari_scris: # parcurgerea pe linii a datelor din fisier
            #stocarea datelor din fisier in listele create mai devreme pentru a realiza graficele
            indexNo.append (float(randNou [0]))
            var1.append(float(randNou[1]))
            var2.append(float(randNou[2]))
            var3.append(float(randNou[3]))
        plt.figure(5)
        plt.plot (indexNo, var1, label = 'Date 1')
        plt.plot (indexNo, var2, label = 'Date 2')
        plt.plot (indexNo, var3, label = 'Date 3')
        plt.xlabel ("indexNo") #denumirea axei x
        plt.ylabel ("Date") #denumirea axei y
        plt.title ('date (indexno)') #titlul graficului
        plt.legend() # legenda graficului
        plt.xticks ([0,25,50]) #dimensiunile axelor
        plt.show() # afisarea graficului

tkWindow = Tk()  #crearea unei ferestre 
tkWindow.geometry('400x150') #setarea dimensiunilor ferestrei
tkWindow.title('Proiect Python') # titlul ferestrei

#crearea unui buton care activeaza functia csv()
button1 = Button(tkWindow,   
	text = 'Creeaza CSV-uri', bg='DarkOrchid2', fg='light cyan',
	command = csv)  
button1.pack()  # organizarea butonului in fereastra

#crearea unui buton care activeaza functia grafice()
button2 = Button(tkWindow,
	text = 'Grafice CSV-uri', bg='DarkOrchid2', fg='light cyan',
	command = grafice)  
button2.pack() # organizarea butonului in fereastra

#crearea unui buton care activeaza functia conectare_TCP()
button3 = Button(tkWindow,
	text = 'Conectare TCP', bg='DarkOrchid2', fg='light cyan',
	command = conectare_TCP)  
button3.pack() # organizarea butonului in fereastra

#crearea unui buton care activeaza functia grafic_TCP()
button4 = Button(tkWindow,
	text = 'Grafic TCP', bg='DarkOrchid2', fg='light cyan',
	command = grafic_TCP)  
button4.pack() # organizarea butonului in fereastra

tkWindow.mainloop() #metoda de mentinere a ferestrei deschise pana cand aceasta este inchisa
