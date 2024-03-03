import tkinter as tk

class Karton:
    def __init__(self, nazwa, wysokosc, szerokosc, dlugosc):
        self.nazwa = nazwa
        self.wysokosc = wysokosc
        self.szerokosc = szerokosc
        self.dlugosc = dlugosc

class Paleta:
    def __init__(self, szerokosc, dlugosc):
        self.szerokosc = szerokosc
        self.dlugosc = dlugosc
        self.kartony = []

class App:
    def __init__(self, master):
        self.master = master
        self.paleta = Paleta(800*0.7, 1200*0.7)
        self.kartony = []

        # Etykieta "Paleta i Kartony"
        self.etykieta = tk.Label(master, text="Paleta i Kartony", font=("Arial", 14))
        self.etykieta.pack()

        self.canvas = tk.Canvas(master, width=self.paleta.szerokosc, height=self.paleta.dlugosc, bg="brown")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.dodaj_karton)
        self.canvas.bind("<B3-Motion>", self.przemiesc_karton)
        self.przenoszony_karton = None

    def dodaj_karton(self, event):
        nazwa_kartona = "Karton" + str(len(self.kartony) + 1)
        nowy_karton = Karton(nazwa_kartona, 20, 50, 70)
        karton_id = self.canvas.create_rectangle(event.x, event.y, event.x + nowy_karton.szerokosc,
                                                 event.y + nowy_karton.dlugosc, fill="blue")
        self.kartony.append((nowy_karton, karton_id))
        print("Dodano: " + nazwa_kartona)

    def przemiesc_karton(self, event):
        self.zacznij_przenoszenie(event)
        if self.przenoszony_karton:
            karton, karton_id = self.przenoszony_karton
            self.canvas.coords(karton_id, event.x, event.y, event.x + karton.szerokosc, event.y + karton.dlugosc)

    def znajdz_karton(self, event):
        x, y = event.x, event.y
        for karton, karton_id in self.kartony:
            x1, y1, x2, y2 = self.canvas.coords(karton_id)
            if x1 <= x <= x2 and y1 <= y <= y2:
                return karton, karton_id
        return None

    def zacznij_przenoszenie(self, event):
        karton_info = self.znajdz_karton(event)
        if karton_info:
            self.przenoszony_karton = karton_info

    def zakoncz_przenoszenie(self, event):
        self.przenoszony_karton = None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Paleta i Kartony")
    app = App(root)
    root.mainloop()
