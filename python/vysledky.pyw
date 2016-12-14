from tkinter import *
from tkinter.ttk import *

class app:

    def __init__(self,master,filename):

        self.parse_file(filename)
        
        self.root = master
        self.root.title('Výsledky')
        self.create_form()

    def parse_file(self,filename):

        f = open(filename)
        line = f.readline().strip()
        self.datetime = line.split(';')[-1]
        line = f.readline().strip()
        self.time = line.split(';')[-1]
        line = f.readline().strip()
        self.examples = int(line.split(';')[-1])
        line = f.readline().strip()
        self.points = line.split(';')[-1].split('/')
        self.points_max = int(self.points[-1])
        self.points = int(self.points[0])
        f.readline()
        f.readline()
        f.readline()
        self.priklady = []
        self.casy = []
        self.pokusy = []
        for i in range(self.examples):
            line = f.readline().strip().split(';')
            self.priklady.append(line[0])
            self.casy.append(float(line[1]))
            self.pokusy.append([])
            pokusy = line[2].split(',')
            for pokus in pokusy:
                self.pokusy[-1].append(int(pokus))
        f.close()

        print(self.priklady)
        print(self.casy)
        print(self.pokusy)

    def create_form(self):

        #hlavni ramec
        self.mainFrm = Frame(self.root,padding=40)
        self.mainFrm.pack()

if __name__ == "__main__":

    root = Tk()
    gui = app(root,"vysledky/1214_2154.csv")
    root.mainloop()
