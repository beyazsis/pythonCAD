from pyautocad import Autocad, APoint

def draw_line(acad, start, end, color=7):
    line = acad.model.AddLine(APoint(*start), APoint(*end))
    line.color = color

def add_text(acad, text, position, height=50):
    text_obj = acad.model.AddText(text, APoint(*position), height)
    text_obj.color = 7

def draw_kiris():
    acad = Autocad(create_if_not_exists=True)

    # Kirişin uzunluğu ve yüksekliği
    kiris_length = 4000
    kiris_height = 400
    cover_offset = 40
    ilave_length = kiris_length / 4

    # Sarı renk kodu: 2
    # Kirişin dışında yer alan beton sınırlarını belirten sarı çizgiler
    draw_line(acad, (0, 0), (kiris_length, 0), color=2)
    draw_line(acad, (0, kiris_height), (kiris_length, kiris_height), color=2)

    # Beton sınırlarının ortasına metin eklemek gerekiyorsa buradan eklenebilir. Ama niye gereksin ki?
    #add_text(acad, "4%%c16", (kiris_length / 2, -20))
    #add_text(acad, "4%%c16", (kiris_length / 2, kiris_height + 20))    

    #DONATI ÇİZİMİNE DAİR SEMBOLİZM
    
    #SolSon = Doğru olaması durumunda Sol tarafta kiriş devam etmiyor. Donatılar kıvrılıyor ve bitiyor. Yanlış ise kiris süreklidir. 
    #SagSon = Doğru olaması durumunda Sol tarafta kiriş devam etmiyor. Donatılar kıvrılıyor ve bitiyor. Yanlış ise kiris süreklidir.
    #Her koşul için mutlaka if kullanılmalıdır. Elif kullanılması durumunda program ilk sağlanan koşulda biteceği için diğer kiriş ucunu çizmeden bırakacaktır.
    #Kolon = Kirişden gelen donatının kolonun ne kadar mm içine gireceğine temsil eder.
    #SolUst = Sol üst ilave donatının varlığını temsil eder. False yok demektir.
    #SagUst = Sağ üst ilave donatının varlığını temsil eder. False yok demektir.
    #SolAlt = Sol alt ilave donatının varlığını temsil eder. False yok demektir.
    #SagAlt = Sağ alt ilave donatının varlığını temsil eder. False yok demektir.
    #SolKolon = Solda ki kolonun varlığını temsil eder. False yok demektir.
    #SagKolon = Sağda ki kolonun varlığını temsil eder. False yok demektir.
    #Ula oğlum bunlar json a mı bağlacam?

    SolSon = True
    SagSon = True
    Kolon = 100
    KolonEn = 300
    SolUst = True
    SolAlt = False
    SagUst = True
    SagAlt = False
    SolKolon = True
    SagKolon = True
    
    #Kolonları çizelim
    if SolKolon:
        draw_line(acad, (-0, 0), (0,-400), color=2)
        draw_line(acad, (-0, kiris_height), (0, kiris_height+400), color=2)
        draw_line(acad, (-KolonEn, 0), (-KolonEn,-400), color=2)
        draw_line(acad, (-KolonEn, kiris_height), (-KolonEn, kiris_height+400), color=2)
        
    if SagKolon:
        draw_line(acad, (kiris_length, 0), (kiris_length,-400), color=2)
        draw_line(acad, (kiris_length, kiris_height), (kiris_length, kiris_height+400), color=2)
        draw_line(acad, (kiris_length+KolonEn, 0), (kiris_length+KolonEn,-400), color=2)
        draw_line(acad, (kiris_length+KolonEn, kiris_height), (kiris_length+KolonEn, kiris_height+400), color=2)
    # Mor renk kodu: 6
    # Beton örtüsü kadar içeride yer alan mor renkli donatı çizgileri
    draw_line(acad, (cover_offset - Kolon, cover_offset), (kiris_length - cover_offset + Kolon + 50, cover_offset), color=6)
    draw_line(acad, (cover_offset - Kolon-50 , kiris_height - cover_offset), (kiris_length - cover_offset + Kolon, kiris_height - cover_offset), color=6)
    if SolSon:#Kiriş devam etmiyor durumu.
        # Mor renk kodu: 6
        # Beton örtüsü kadar içeride yer alan mor renkli donatı çizgileri
        draw_line(acad, (cover_offset - Kolon, cover_offset), (cover_offset - Kolon, (-cover_offset + (kiris_height * 0.9))), color=6)
        draw_line(acad, (cover_offset - Kolon - 50, kiris_height - cover_offset), (cover_offset - Kolon - 50, (-(kiris_height*0.5) + cover_offset)), color=6)

    if SagSon:#Kiriş devam etmiyor durumu.
        # Mor renk kodu: 6
        # Beton örtüsü kadar içeride yer alan mor renkli donatı çizgileri
        draw_line(acad, (kiris_length + Kolon - cover_offset +50, cover_offset), (kiris_length + Kolon - cover_offset +50, -cover_offset + kiris_height * 0.9), color=6)
        draw_line(acad, (kiris_length + Kolon - cover_offset, kiris_height - cover_offset), (kiris_length + Kolon - cover_offset, -kiris_height * 0.5 + cover_offset), color=6)

    if not SagSon:
        pass #Yapacak bir şey aklıma gelmedi. Zaten devam edercesine çizdiydik donatıları
    if not SagSon:
        pass #Yapacak bir şey aklıma gelmedi. Zaten devam edercesine çizdiydik donatıları
        
        
    # Donatı çizgilerinin ortasına metin ekle
    add_text(acad, "4%%c16", ((kiris_length) / 2, cover_offset - 20))
    add_text(acad, "4%%c16", ((kiris_length) / 2, kiris_height - cover_offset + 20))

    # Montaj donatısı (kirişin tam ortasından geçen)
    montaj_y = kiris_height / 2
    draw_line(acad, (cover_offset, montaj_y), (kiris_length - cover_offset, montaj_y), color=6)
    add_text(acad, "4%%c16", (kiris_length / 2, montaj_y - 20))

    # İlave donatılar 
    # Üst sol
    if SolAlt:
        draw_line(acad, (cover_offset - 125, cover_offset + 60), (cover_offset - 75 + ilave_length, cover_offset + 60), color=6)
        add_text(acad, "4%%c16", (cover_offset - 75 + ilave_length / 2, cover_offset + 40))

    # Üst sağ
    if SagAlt:
        draw_line(acad, (kiris_length - cover_offset - ilave_length + 125, cover_offset + 60), (kiris_length - cover_offset + 125, cover_offset + 60), color=6)
        add_text(acad, "4%%c16", (kiris_length - cover_offset - ilave_length / 2 + 75, cover_offset + 40))

    # Alt sol
    if SolUst:
        draw_line(acad, (cover_offset - 75, kiris_height - cover_offset - 60), (cover_offset - 75 + ilave_length, kiris_height - cover_offset - 60), color=6)
        add_text(acad, "4%%c16", (cover_offset - 25 + ilave_length / 2, kiris_height - cover_offset - 80))

    # Alt sağ
    if SagUst:
        draw_line(acad, (kiris_length - cover_offset - ilave_length + 75, kiris_height - cover_offset - 60), (kiris_length - cover_offset + 75, kiris_height - cover_offset - 60), color=6)
        add_text(acad, "4%%c16", (kiris_length - cover_offset - ilave_length / 2 + 25, kiris_height - cover_offset - 80))

    #İlave Donatı Bükümleri
    if SolSon:
        draw_line(acad, (cover_offset -125, cover_offset + 60), (cover_offset - 125, - cover_offset + kiris_height), color=6)
        draw_line(acad, (cover_offset - 75, kiris_height - cover_offset - 60), (cover_offset - 75, cover_offset + 60 + 12), color=6)
    if SagSon:
        draw_line(acad, (kiris_length - cover_offset + 125, cover_offset + 60), (kiris_length - cover_offset + 125, - cover_offset + kiris_height), color=6)
        draw_line(acad, (kiris_length - cover_offset + 75, kiris_height - cover_offset - 60), (kiris_length - cover_offset + 75, + cover_offset + 60 + 12 ) , color=6)

if __name__ == "__main__":
    draw_kiris()
