import tkinter as tk
from tkinter import messagebox
from pyautocad import Autocad, APoint
import time


x_daire_pos = []
y_daire_pos = []

def en_kucuk_fark(sayi, liste):

    en_kucuk_fark = float('inf')
    

    for num in liste:
        fark = abs(sayi - num)
        

        if fark < en_kucuk_fark:
            en_kucuk_fark = sayi - num
    
    return en_kucuk_fark


def restart_autocad_connection():
    try:
        print("AutoCAD bağlantısı kuruluyor...")
        acad = Autocad(create_if_not_exists=True)
        print("AutoCAD bağlantısı kuruldu.")
        return acad
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None

# AutoCAD bağlantısını tekrar kur ve hata durumunda tekrar dene
acad = None
attempts = 0
max_attempts = 5

while acad is None and attempts < max_attempts:
    acad = restart_autocad_connection()
    attempts += 1
    if acad is None:
        print(f"Bağlantı denemesi başarısız oldu. {attempts}/{max_attempts} tekrar dene...")
        time.sleep(2)

if acad is None:
    print("AutoCAD bağlantısı kurulamadı. Lütfen AutoCAD'in açık olduğundan ve COM bağlantısının çalıştığından emin olun.")
    exit(1)

def submit_form():
    global kolonX, kolonY, cover, rebarX, rebarY, cornerBar, midBar, Xciroz, Yciroz, KolonHarf, KolonNumara, KolonBoy, SagKiris, SolKiris, Benzer 
    try:
        kolonX = int(entries["Kolon X uzunluğu:"].get())
        kolonY = int(entries["Kolon Y uzunluğu:"].get())
        cover = int(entries["Beton Örtüsü:"].get())
        rebarX = int(entries["X yönü donatı sayısı:"].get())
        rebarY = int(entries["Y yönü donatı sayısı:"].get())
        cornerBar = int(entries["Köşe donatısı çapı:"].get())
        midBar = int(entries["Orta donatı çapı:"].get())
        Xciroz = int(entries["X yönü çiroz sayısı:"].get())
        Yciroz = int(entries["Y yönü çiroz sayısı:"].get())
        KolonHarf = entries["Kolon Harfi:"].get()
        KolonNumara = entries["Kolon Numarası:"].get()
        KolonBoy = entries["Kolon Boyu:"].get()
        SagKiris = entries["Sağda kiriş bağlı:"].get()
        SolKiris = entries["Solda kiriş bağlı:"].get()
        Benzer = int(entries["Benzer Kolon Sayısı:"].get())
        root.destroy()  # GUI'yi kapat
    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm alanlara geçerli değerler girin")

    try:
        acad.doc.layers.add("kolon").color = 170
        acad.doc.layers.add("donati").color = 3
        acad.prompt("Bir nokta seçiniz: ")
        
        point = None
        while point is None:
            try:
                point = acad.doc.Utility.GetPoint()
            except:
                print("Nokta alınamadı tekrar deneniyor...")
                time.sleep(1)
        
        point1 = APoint(point)
        point2 = APoint(point1[0] + kolonX, point1[1])
        point3 = APoint(point1[0] + kolonX, point1[1] + kolonY)
        point4 = APoint(point1[0], point1[1] + kolonY)
        
        l1 = acad.model.AddLine(point1, point2)
        l1.color = 170
        l1.Layer = "kolon"
        l2 = acad.model.AddLine(point2, point3)
        l2.color = 170
        l2.Layer = "kolon"
        l3 = acad.model.AddLine(point3, point4)
        l3.color = 170
        l3.Layer = "kolon"
        l4 = acad.model.AddLine(point4, point1)
        l4.color = 170
        l4.Layer = "kolon"
        print("Büyük dikdörtgen başarıyla çizildi.")
        
        inner_point1 = APoint(point1[0] + cover, point1[1] + cover)
        inner_point2 = APoint(point2[0] - cover, point2[1] + cover)
        inner_point3 = APoint(point3[0] - cover, point3[1] - cover)
        inner_point4 = APoint(point4[0] + cover, point4[1] - cover)
        
        line1 = acad.model.AddLine(inner_point1, inner_point2)
        line2 = acad.model.AddLine(inner_point2, inner_point3)
        line3 = acad.model.AddLine(inner_point3, inner_point4)
        line4 = acad.model.AddLine(inner_point4, inner_point1)
        
        print("Küçük dikdörtgen başarıyla çizildi.")
        
        acad.model.AddCircle(inner_point1, cornerBar / 20).color = 3
        acad.model.AddCircle(inner_point2, cornerBar / 20).color = 3
        acad.model.AddCircle(inner_point3, cornerBar / 20).color = 3
        acad.model.AddCircle(inner_point4, cornerBar / 20).color = 3
        
        print("Köşe daireleri başarıyla eklendi.")
        
        x_spacing = (kolonX - 2 * cover) / (rebarX - 1)
        y_spacing = (kolonY - 2 * cover) / (rebarY - 1)
        
        for i in range(1, rebarX - 1):
            x_pos = inner_point1[0] + i * x_spacing
            d1 = acad.model.AddCircle(APoint(x_pos, inner_point1[1]), midBar / 20)
            d1.color = 3
            d1.layer = "donati"
            x_daire_pos.append(x_pos)
            d2 = acad.model.AddCircle(APoint(x_pos, inner_point3[1]), midBar / 20)
            d2.color = 3
            d2.layer = "donati"
        
        print("X yönünde daireler başarıyla eklendi.")
        
        for i in range(1, rebarY - 1):
            y_pos = inner_point1[1] + i * y_spacing
            dy1 = acad.model.AddCircle(APoint(inner_point1[0], y_pos), midBar / 20)
            dy1.color = 3
            dy1.layer = "donati"
            y_daire_pos.append(y_pos)
            dy2 = acad.model.AddCircle(APoint(inner_point2[0], y_pos), midBar / 20)
            dy2.color = 3
            dy1.layer = "donati"
    
        print("Y yönünde daireler başarıyla eklendi.")
        print("X pos -------->   ", x_daire_pos)
        print("Y pos -------->   ", y_daire_pos)
        line1.Delete()
        line2.Delete()
        line3.Delete()
        line4.Delete()

        outer_point1 = APoint(point1[0] + cover - midBar / 20, point1[1] + cover - midBar / 20)
        outer_point2 = APoint(point2[0] - cover + midBar / 20, point2[1] + cover - midBar / 20)
        outer_point3 = APoint(point3[0] - cover + midBar / 20, point3[1] - cover + midBar / 20)
        outer_point4 = APoint(point4[0] + cover - midBar / 20, point4[1] - cover + midBar / 20)
        
        line1 = acad.model.AddLine(outer_point1, outer_point2)
        line1.layer = "donati"
        line2 = acad.model.AddLine(outer_point2, outer_point3)
        line2.layer = "donati"
        line3 = acad.model.AddLine(outer_point3, outer_point4)
        line3.layer = "donati"
        line4 = acad.model.AddLine(outer_point4, outer_point1)
        line4.layer = "donati"
        print("Dış dikdörtgen başarıyla daraltıldı.")
        
        # Çirozları çizme
        for i in range(1, Xciroz + 1):
            x_offset = i * (kolonX - 2 * cover) / (Xciroz + 1)
            pos_x = x_offset + inner_point1[0]
            kaydirma_x = en_kucuk_fark(pos_x, x_daire_pos)
            print(x_daire_pos)
            print(f"Çiroz {i}: pos_x = {pos_x}, kaydirma_x = {kaydirma_x}")
            ciroz1 = APoint(inner_point1[0] + x_offset - kaydirma_x -(midBar / 20) -0.5 , inner_point1[1])
            ciroz2 = APoint(inner_point1[0] + x_offset - kaydirma_x -(midBar / 20) - 0.5, inner_point4[1])
            acad.model.AddLine(ciroz1, ciroz2).layer = "donati"

        for i in range(1, Yciroz + 1):
            y_offset = i * (kolonY - 2 * cover) / (Yciroz + 1)
            pos_y = y_offset + inner_point1[1]
            kaydirma_y = en_kucuk_fark(pos_y, y_daire_pos)
            ciroz1 = APoint(inner_point1[0], inner_point1[1] + y_offset - kaydirma_y -(midBar / 20) -0.5)
            ciroz2 = APoint(inner_point2[0], inner_point1[1] + y_offset - kaydirma_y -(midBar / 20) -0.5)
            acad.model.AddLine(ciroz1, ciroz2).layer = "donati"
        print("Çirozlar başarıyla çizildi.")
                


    except Exception as e:
        print(f"Bir hata oluştu: {e}")

root = tk.Tk()
root.title("KOLON VERİLERİ")

# Giriş kutularını saklamak için bir sözlük oluştur
entries = {}

# Sol taraf için etiketler ve giriş kutuları
left_labels = [    "Kolon X uzunluğu:",    "Kolon Y uzunluğu:",    "Beton Örtüsü:",    "X yönü donatı sayısı:",    "Y yönü donatı sayısı:",    "Köşe donatısı çapı:",    "Orta donatı çapı:",    "X yönü çiroz sayısı:",    "Y yönü çiroz sayısı:"]

right_labels = [    "Kolon Harfi:",    "Kolon Numarası:",    "Kolon Boyu:",    "Sağda kiriş bağlı:",    "Solda kiriş bağlı:",    "Benzer Kolon Sayısı:"]

for i, label in enumerate(left_labels):
    tk.Label(root, text=label).grid(row=i, column=0, sticky=tk.E)
    entries[label] = tk.Entry(root)
    entries[label].grid(row=i, column=1)

for i, label in enumerate(right_labels):
    tk.Label(root, text=label).grid(row=i, column=2, sticky=tk.E)
    if "kiriş bağlı" in label:
        var = tk.IntVar()
        chk = tk.Checkbutton(root, variable=var)
        chk.grid(row=i, column=3)
        entries[label] = var
    else:
        entries[label] = tk.Entry(root)
        entries[label].grid(row=i, column=3)


tk.Button(root, text="Tamam", command=submit_form).grid(row=max(len(left_labels), len(right_labels)), column=1, columnspan=2)

root.mainloop()
