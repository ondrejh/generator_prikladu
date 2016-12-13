from tkinter import *
from tkinter.ttk import *
import random

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

        # a - b ... b>20
        if (z==1) and (b>20):
            continue
        
        # odesli
        return(a,z,b)

def spocitej_priklad(priklad):

    if (priklad[1]==0):
        return (priklad[0]+priklad[2])

    return (priklad[0]-priklad[2])

def vytiskni_priklad(priklad):

    print('{} {} {} = {}'.format(priklad[0],
                                 '+' if priklad[1]==0 else '-',
                                 priklad[2],
                                 spocitej_priklad(priklad)))

ex_font = ("Times", 32, font.BOLD)
info_font = ("Times", 24, font.BOLD)

max_bodu = 10

class app:
    
    def __init__(self,master):

        self.priklady = []
        self.vysledky = []
        self.bylopozde = []
        self.body = 0
        
        self.create_form()
        
    def create_form(self):

        #hlavni ramec
        self.mainFrm = Frame(root,padding='20 20 20 20')
        self.mainFrm.pack()

        #ramec progresbaru
        self.progFrm = Frame(self.mainFrm,padding='0 0 0 0')
        self.progFrm.pack(side=TOP,fill=X)
        self.progr = Progressbar(self.progFrm,mode='determinate',value=0,maximum=max_bodu)
        self.progr.pack(side=TOP,fill=X)

        #ramec prikladu
        self.exFrame = Frame(self.mainFrm,padding='0 20 0 20')
        self.exFrame.pack(side=TOP)
        self.aLabel = Label(self.exFrame,text='A',width=2,
                            font=ex_font,padding='0 0 20 0')
        self.aLabel.pack(side=LEFT)
        self.zLabel = Label(self.exFrame,text='+',width=1,
                            font=ex_font,padding='0 0 20 0')
        self.zLabel.pack(side=LEFT)
        self.bLabel = Label(self.exFrame,text='B',width=2,
                            font=ex_font,padding='0 0 20 0')
        self.bLabel.pack(side=LEFT)
        self.eLabel = Label(self.exFrame,text='=',width=1,
                            font=ex_font,padding='0 0 20 0')
        self.eLabel.pack(side=LEFT)
        self.result_svar = StringVar()
        self.rEntry = Entry(self.exFrame,justify=CENTER,
                            state=DISABLED,
                            textvariable=self.result_svar,
                            font=ex_font,width=5)
        self.rEntry.pack(side=LEFT)
        self.rEntry.bind('<Return>',self.check_example)

        #ramec vysledku
        self.resFrm = Frame(self.mainFrm,padding='0 0 0 0')
        self.resFrm.pack(side=TOP,fill=X)
        self.infoLabel = Label(self.resFrm,text='Připrav se !!!',
                               font=info_font)
        self.infoLabel.pack(side=TOP)
        
        root.after(2000,self.fillin_example)


    def fillin_example(self):

        self.priklad = generuj_priklad()
        self.vysledek = []
        self.pozde = False

        self.aLabel.config(text=str(self.priklad[0]))
        self.zLabel.config(text='+' if self.priklad[1]==0 else '-')
        self.bLabel.config(text=str(self.priklad[2]))

        self.infoLabel.config(text='30')
        root.after(1000,self.downcount)
        self.result_svar.set('')
        self.rEntry.config(state=NORMAL)
        self.rEntry.focus_set()

    def downcount(self):

        try:
            num = int(self.infoLabel.cget('text'))-1
            if num==0:
                self.infoLabel.config(text='Pozdě !!!')
            else:
                self.infoLabel.config(text = str(num))
                root.after(1000,self.downcount)
        except:
            pass

    def check_example(self,event):

        try:
            result = int(self.result_svar.get())
        except:
            self.result_svar.set('')
            self.rEntry.focus_set()
            return

        if result == spocitej_priklad(self.priklad):
            self.priklady.append(self.priklad)
            self.vysledky.append(self.vysledek)
            self.bylopozde.append(self.pozde)
            if len(self.vysledek)==0:
                self.body += 5
            else:
                self.body += 3
            if self.pozde==True:
                self.body -= 2
            self.progr.config(value=self.body)
            if self.body>=max_bodu:
                print(self.priklady)
                print(self.vysledky)
                print(self.bylopozde)
                self.rEntry.config(state=DISABLED)
            else:
                self.fillin_example()
            return
        else:
            self.vysledek.append(result)
            self.result_svar.set('')
            self.rEntry.focus_set()            

root = Tk()
gui = app(root)
root.mainloop()
