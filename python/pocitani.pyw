#!/usr/bin/env python3

from tkinter import *
from tkinter.ttk import *
import pygame
import random
import time
import os

pocitani_max = 40
pocitani_min = 0

random.seed()

def generuj_priklad():

    while True:

        # nahodne generuj
        a = random.randrange(pocitani_min,pocitani_max+1,1)
        b = random.randrange(pocitani_min,pocitani_max+1,1)
        z = random.randrange(2)

        # a + b > max
        if (z==0) and (a+b)>pocitani_max:
            continue

        # a - b < min
        if (z==1) and (a-b)<0:
            continue

        # odesli
        return('{} {} {} = {}'.format(a,'+' if z==0 else '-',b,'X'))

def spocitej_priklad(priklad):

    kousky = priklad.split(' ')
    if (kousky[1]=='+'):
        return (int(kousky[0])+int(kousky[2]))

    return (int(kousky[0])-int(kousky[2]))

ex_font = ("Times", 48, 'bold')
info_font = ("Times", 24, 'bold')

max_bodu = 100
cas_na_priklad = 30

class app:
    
    def __init__(self,master):

        self.root = master
        self.root.title('Počítání do {}'.format(pocitani_max))
        self.root.protocol("WM_DELETE_WINDOW",self.save_result)

        pygame.mixer.init()
        self.sndNew = pygame.mixer.Sound("zvuky/pikon.ogg")
        self.sndSuccess = pygame.mixer.Sound("zvuky/tyarari.ogg")
        self.sndFail = pygame.mixer.Sound("zvuky/piano.ogg")

        self.create_form()
        
    def create_form(self):

        #hlavni ramec
        self.mainFrm = Frame(self.root,padding='40')
        self.mainFrm.pack()

        #ramec progresbaru
        self.progFrm = Frame(self.mainFrm,padding='0 0 0 0')
        self.progFrm.pack(side=TOP,fill=X)
        self.progr = Progressbar(self.progFrm,mode='determinate',value=0,maximum=max_bodu)
        self.progr.pack(side=TOP,fill=X)

        #ramec prikladu
        self.exFrame = Frame(self.mainFrm,padding='0 50 0 50')
        self.exFrame.pack(side=TOP)
        self.aLabel = Label(self.exFrame,text='A',width=3,
                            font=ex_font,padding='0 0 20 0',
                            justify=CENTER,anchor=CENTER)
        self.aLabel.pack(side=LEFT)
        self.zLabel = Label(self.exFrame,text='+',width=1,
                            font=ex_font,padding='0 0 20 0',
                            justify=CENTER,anchor=CENTER)
        self.zLabel.pack(side=LEFT)
        self.bLabel = Label(self.exFrame,text='B',width=3,
                            font=ex_font,padding='0 0 20 0',
                            justify=CENTER,anchor=CENTER)
        self.bLabel.pack(side=LEFT)
        self.eLabel = Label(self.exFrame,text='=',width=1,
                            font=ex_font,padding='0 0 20 0',
                            justify=CENTER,anchor=CENTER)
        self.eLabel.pack(side=LEFT)
        self.result_svar = StringVar()
        self.rEntry = Entry(self.exFrame,justify=CENTER,
                            state=DISABLED,
                            textvariable=self.result_svar,
                            font=ex_font,width=5)
        self.rEntry.pack(side=LEFT)
        self.rEntry.bind('<Return>',self.check_example)
        self.rEntry.bind('<KP_Enter>',self.check_example)

        #ramec vysledku
        self.resFrm = Frame(self.mainFrm,padding='0 0 0 0')
        self.resFrm.pack(side=TOP,fill=X)

        self.smaj1 = PhotoImage(file='smajliky/smajlik.png')
        self.smaj2 = PhotoImage(file='smajliky/premyslik.png')
        self.smaj3 = PhotoImage(file='smajliky/mracik.png')
        self.smaj4 = PhotoImage(file='smajliky/hotovik.png')
        self.smaj5 = PhotoImage(file='smajliky/vykulik.png')
        self.smaj6 = PhotoImage(file='smajliky/strasik.png')

        self.smajLLabel = Label(self.resFrm,image = self.smaj5)
        self.smajLLabel.pack(side=LEFT)
        self.countLabel = Label(self.resFrm,text='Připrav\nse !',
                                font=info_font,justify=CENTER,
                                width=15,anchor=CENTER,
                                foreground = 'gray')
        self.countLabel.pack(side=LEFT,fill=BOTH)
        self.smajRLabel = Label(self.resFrm,image = self.smaj5)
        self.smajRLabel.pack(side=RIGHT)
        
        self.root.after(2000,self.first_start)

    def info_thinking(self):

        self.smajLLabel.config(image=self.smaj2)
        self.smajRLabel.config(image=self.smaj2)

    def info_worry(self):

        self.smajLLabel.config(image=self.smaj6)
        self.smajRLabel.config(image=self.smaj6)
        self.mainFrm.config(bg='yellow')

    def info_happy(self,body):

        self.smajLLabel.config(image=self.smaj1)
        self.smajRLabel.config(image=self.smaj1)
        self.countLabel.config(text='{}\n{} bod{}'.format('Správně' if body!=5 else 'Výborně',
                                                          body,
                                                          'ů' if body>3 else ('' if body<2 else 'y')))
        self.sndSuccess.play()

    def info_unhappy(self):

        self.smajLLabel.config(image=self.smaj3)
        self.smajRLabel.config(image=self.smaj3)
        self.countLabel.config(text='Špatně')

        self.sndFail.play()

    def info_done(self):

        self.smajLLabel.config(image=self.smaj4)
        self.smajRLabel.config(image=self.smaj4)
        self.countLabel.config(text='Hotovo')

    def first_start(self):
        
        self.priklady = []
        self.chyby = []
        self.casy = []
        self.body = 0
        self.started = time.time()

        self.fillin_example()
        
    def fillin_example(self):

        while True:
            self.priklad = generuj_priklad()
            if self.priklad in self.priklady:
                continue
            break
        self.zacatek = time.perf_counter()
        self.pokusy = []

        self.aLabel.config(text=self.priklad.split(' ')[0])
        self.zLabel.config(text=self.priklad.split(' ')[1])
        self.bLabel.config(text=self.priklad.split(' ')[2])

        self.info_thinking()
        
        self.countLabel.config(text=str(cas_na_priklad))
        self.root.after(1000,self.downcount)

        self.result_svar.set('')
        self.rEntry.config(state=NORMAL)
        self.rEntry.focus_set()

        self.sndNew.play()

    def try_again(self):

        self.result_svar.set('')
        self.rEntry.config(state=NORMAL)
        self.rEntry.focus_set()
        self.info_thinking()

    def downcount(self):

        try:
            num = int(self.countLabel.cget('text'))-1
            if num==0:
                self.countLabel.config(text='')
                self.info_worry()
                self.root.after(1000,self.info_thinking)
            else:
                self.countLabel.config(text = str(num))
                self.root.after(1000,self.downcount)
        except:
            pass

    def save_result(self):

        if len(self.priklady)>0:
            if not os.path.isdir("vysledky"):
                os.makedirs("vysledky")
            file = open(time.strftime('vysledky/%m%d_%H%M.csv',time.localtime(self.started)),'w')
            file.write('Datum a čas;{}\n'.format(time.strftime('%Y.%m.%d %H:%M',time.localtime(self.started))))
            file.write('Celkový čas;{}\n'.format(time.strftime('%H:%M:%S',time.gmtime(time.time()-self.started))))
            file.write('Příkladů celkem;{}\n'.format(len(self.priklady)))
            file.write('Bodů;{}/{}\n\n'.format(self.body,max_bodu))
            file.write('příklad;čas;pokusy\n\n')
            for i in range(len(self.priklady)):
                file.write('{};{:0.1f};{}'.format(self.priklady[i],
                                             self.casy[i],
                                             self.chyby[i][0]))
                for c in self.chyby[i][1:]:
                    file.write(',{}'.format(c))
                file.write('\n')
            file.close()
        self.root.after(1000,root.destroy)

    def check_example(self,event):

        try:
            result = int(self.result_svar.get())
        except:
            self.result_svar.set('')
            self.rEntry.focus_set()
            return

        self.rEntry.config(state=DISABLED)
        self.pokusy.append(result)
        
        if result == spocitej_priklad(self.priklad):
            self.priklady.append(self.priklad)
            self.chyby.append(self.pokusy)
            self.casy.append(time.perf_counter()-self.zacatek)
            body = 5
            if self.casy[-1]>cas_na_priklad:
                body -= 2
            if len(self.pokusy)>1:
                body = 1
            self.body += body
            self.info_happy(body)
            if self.body>=max_bodu:
                self.info_done()
                self.save_result()
            else:
                self.root.after(2000,self.fillin_example)
            self.progr.config(value=self.body)
        else:
            self.info_unhappy()
            self.root.after(1000,self.try_again)

if __name__ == "__main__":

    root = Tk()
    gui = app(root)
    root.mainloop()

'''priklad = generuj_priklad()
print(priklad)
print(spocitej_priklad(priklad))'''
