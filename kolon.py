from pyautocad import Autocad, APoint
import pythoncom
import time

def restart_autocad_connection():
    try:
        # İlk bağlantı
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

def safe_get_integer(prompt_text):
    value = None
    while value is None:
        try:
            value = acad.doc.Utility.GetInteger(prompt_text)
        except:
            print(f"{prompt_text} girişi başarısız oldu, tekrar deneyin...")
            time.sleep(1)
    return value

def safe_get_point():
    value = None
    while value is None:
        try:
            value = acad.doc.Utility.GetPoint()
        except:
            print("Nokta alınamadı tekrar deneniyor...")
            time.sleep(1)
    return value

try:
    acad.doc.layers.add("kolon").color = 170
    acad.doc.layers.add("donati").color = 3
    kolonX = safe_get_integer("Kolon X uzunluğu: ")
    kolonY = safe_get_integer("Kolon Y uzunluğu: ")
    cover = safe_get_integer("Beton Örtüsü: ")
    rebarX = safe_get_integer("X yönü donatı sayısı: ")
    rebarY = safe_get_integer("Y yönü donatı sayısı: ")
    cornerBar = safe_get_integer("Köşe donatısı çapı: ")
    midBar = safe_get_integer("Orta donatı çapı: ")
    acad.prompt("Bir nokta seçiniz: ")
    point = safe_get_point()
    point1 = APoint(point)
    point2 = APoint(point1[0] + kolonX, point1[1])
    point3 = APoint(point1[0] + kolonX, point1[1] + kolonY)
    point4 = APoint(point1[0], point1[1] + kolonY)
    
    # Büyük dikdörtgenin kenarlarını çiz
    l1 =acad.model.AddLine(point1, point2)
    l1.color = 170
    l1.Layer = "kolon"
    l2 = acad.model.AddLine(point2, point3)
    l2.color = 170
    l2.Layer = "kolon"
    l3 = acad.model.AddLine(point3, point4)
    l3.color = 170
    l3.Layer = "kolon"
    l4 =acad.model.AddLine(point4, point1)
    l4.color = 170
    l4.Layer = "kolon"
    print("Büyük dikdörtgen başarıyla çizildi.")
    
    # Küçük dikdörtgenin köşe noktalarını hesapla
    inner_point1 = APoint(point1[0] + cover, point1[1] + cover)
    inner_point2 = APoint(point2[0] - cover, point2[1] + cover)
    inner_point3 = APoint(point3[0] - cover, point3[1] - cover)
    inner_point4 = APoint(point4[0] + cover, point4[1] - cover)
    
    # Küçük dikdörtgenin kenarlarını çiz
    line1 = acad.model.AddLine(inner_point1, inner_point2)
    line2 = acad.model.AddLine(inner_point2, inner_point3)
    line3 = acad.model.AddLine(inner_point3, inner_point4)
    line4 = acad.model.AddLine(inner_point4, inner_point1)
    
    print("Küçük dikdörtgen başarıyla çizildi.")
    
    # Küçük dikdörtgenin köşelerine daireler ekle
    acad.model.AddCircle(inner_point1, cornerBar / 20).color = 3
    acad.model.AddCircle(inner_point2, cornerBar / 20).color = 3
    acad.model.AddCircle(inner_point3, cornerBar / 20).color = 3
    acad.model.AddCircle(inner_point4, cornerBar / 20).color = 3
    
    print("Köşe daireleri başarıyla eklendi.")
    
    # X yönünde iç dikdörtgenin üzerine daireler ekle
    x_spacing = (kolonX - 2 * cover) / (rebarX - 1)
    for i in range(1, rebarX - 1):
        x_pos = inner_point1[0] + i * x_spacing
        d1 = acad.model.AddCircle(APoint(x_pos, inner_point1[1]), midBar / 20)
        d1.color = 3
        d1.layer = "donati"
        d2 = acad.model.AddCircle(APoint(x_pos, inner_point3[1]), midBar / 20)
        d2.color = 3
        d2.layer = "donati"
    
    print("X yönünde daireler başarıyla eklendi.")
    
    # Y yönünde iç dikdörtgenin üzerine daireler ekle
    y_spacing = (kolonY - 2 * cover) / (rebarY - 1)
    for i in range(1, rebarY - 1):
        y_pos = inner_point1[1] + i * y_spacing
        acad.model.AddCircle(APoint(inner_point1[0], y_pos), midBar / 20).color = 3
        acad.model.AddCircle(APoint(inner_point2[0], y_pos), midBar / 20).color = 3
    
    print("Y yönünde daireler başarıyla eklendi.")
    
    # Küçük dikdörtgeni sil
    line1.Delete()
    line2.Delete()
    line3.Delete()
    line4.Delete()


    # Küçük dikdörtgenin köşe noktalarını hesapla
    outer_point1 = APoint(point1[0] + cover - midBar / 20, point1[1] + cover - midBar / 20)
    outer_point2 = APoint(point2[0] - cover + midBar / 20, point2[1] + cover - midBar / 20)
    outer_point3 = APoint(point3[0] - cover + midBar / 20, point3[1] - cover + midBar / 20)
    outer_point4 = APoint(point4[0] + cover - midBar / 20, point4[1] - cover + midBar / 20)
    # Küçük dikdörtgenin kenarlarını çiz
    line1 = acad.model.AddLine(outer_point1, outer_point2)
    line1.layer = "donati"
    line2 = acad.model.AddLine(outer_point2, outer_point3)
    line2.layer = "donati"
    line3 = acad.model.AddLine(outer_point3, outer_point4)
    line3.layer = "donati"
    line4 = acad.model.AddLine(outer_point4, outer_point1)
    line4.layer = "donati"
    print("Dış dikdörtgen başarıyla daraltıldı.")


except Exception as e:
    print(f"Bir hata oluştu: {e}")
