import tkinter as tk
from PIL import Image, ImageTk  # Dodane importy do obsługi obrazów

class Karton:
    def __init__(self, nazwa, wysokosc, szerokosc, dlugosc, kat_obrotu):
        self.nazwa = nazwa
        self.wysokosc = wysokosc
        self.szerokosc = szerokosc
        self.dlugosc = dlugosc
        self.kat_obrotu = kat_obrotu

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
        self.zlapany_karton_flag = False

        # Etykieta "Paleta i Kartony"
        # self.etykieta = tk.Label(master, text="Paleta i Kartony", font=("Arial", 14))
        # self.etykieta.pack()

        self.canvas = tk.Canvas(master, width=self.paleta.szerokosc, height=self.paleta.dlugosc, bg="brown")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", lambda event: self.dodaj_karton(event, dlugosc=150, szerokosc=50, wysokosc=50, kat_obrotu=19))
        self.canvas.bind("<B3-Motion>", self.przemiesc_karton)
        self.canvas.bind("<ButtonRelease-3>", self.zakoncz_przenoszenie)
        self.przenoszony_karton = None


        
    def dodaj_karton(self, event, szerokosc, dlugosc, wysokosc, kat_obrotu):
        nazwa_kartona = "Karton" + str(len(self.kartony) + 1)
        nowy_karton = Karton(nazwa_kartona, wysokosc, szerokosc, dlugosc, kat_obrotu)
        obraz_kartona_poczatkowy = Image.open("paleta_i_kartony_gui\\Graph\\karton.jpg").convert("RGBA")

        # Resizowanie obrazu
        obraz_kartona_resize = obraz_kartona_poczatkowy.resize((nowy_karton.szerokosc, nowy_karton.dlugosc))
        # Obrót obrazu
        obraz_kartona_obrocony = obraz_kartona_resize.rotate(nowy_karton.kat_obrotu, expand=True)
        
        # Stwórz nowy obraz z kanałem alfa
        nowy_szerokosc = max(obraz_kartona_obrocony.width, nowy_karton.szerokosc)
        nowy_dlugosc = max(obraz_kartona_obrocony.height, nowy_karton.dlugosc)
        obraz_kartona = Image.new("RGBA", (nowy_szerokosc, nowy_dlugosc), (0, 0, 0, 0))
        
        # Wklej obrócony obraz w środek nowego obrazu
        x_offset = (nowy_szerokosc - obraz_kartona_obrocony.width) // 2
        y_offset = (nowy_dlugosc - obraz_kartona_obrocony.height) // 2
        obraz_kartona.paste(obraz_kartona_obrocony, (x_offset, y_offset), obraz_kartona_obrocony)

        # obraz_kartona = obraz_kartona.resize((nowy_karton.szerokosc, nowy_karton.dlugosc))
        obraz_kartona = ImageTk.PhotoImage(obraz_kartona)

        karton_id = self.canvas.create_image(event.x, event.y, anchor=tk.NW, image=obraz_kartona)
        self.kartony.append((nowy_karton, karton_id, obraz_kartona))
        print("Dodano: " + nazwa_kartona + " o X: " + str(szerokosc) + " o Y: " + str(dlugosc))

    

    def przemiesc_karton(self, event):
        self.zacznij_przenoszenie(event)
        if self.przenoszony_karton:
            karton, karton_id = self.przenoszony_karton
            self.canvas.coords(karton_id, event.x, event.y, event.x + karton.szerokosc, event.y + karton.dlugosc)

    def znajdz_karton(self, event):
        x, y = event.x, event.y
        print("Odczyt z myszki: " + str(x) + " " + str(y))
        if not(self.zlapany_karton_flag):
            for karton, karton_id in self.kartony:
                x1, y1, x2, y2 = self.canvas.coords(karton_id)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.zlapany_karton_flag = True
                    print("Zlapano karton")
                    return karton, karton_id
        return None

    def zacznij_przenoszenie(self, event):
        karton_info = self.znajdz_karton(event)
        if karton_info:
            self.przenoszony_karton = karton_info

    def zakoncz_przenoszenie(self, event):
        if self.zlapany_karton_flag:
            self.zlapany_karton_flag = False
            self.przenoszony_karton = None
            print("Puszczono zlapany karton")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Paleta i Kartony")
    app = App(root)
    root.mainloop()
