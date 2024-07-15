# **İnşaat Mühendisleri İçin Autocad Otomasyonu (Güncel Olarak Geliştiriliyor)**

Bu proje, İnşaat Mühendislerinin **Autocad** üzerindeki iş akışlarını **Python** kullanarak otomatikleştirmelerine yardımcı olmayı amaçlamaktadır. Aşağıda, projede yer alan ana dosyalar ve işlevleri hakkında detaylı bilgiler bulabilirsiniz.

## **Proje Dosyaları ve İşlevleri**

### 1. `table2xlsx.lsp`
Bu dosya, **LISP** kullanılarak yazılmıştır ve Python betiklerinin Autocad üzerinden verilen komutlarla çalıştırılmasını sağlar.

### 2. `kolon-gui.py`
Bu Python betiği, **kolon çizimi** gerçekleştirmek için kullanılır. Kullanıcı dostu bir arayüz sunar ve kolonların çizimini hızlı ve kolay bir şekilde yapmanıza olanak tanır.

### 3. `table-xlsx.py`
Bu betik, çizimde seçilen alandaki **çizilmiş tabloları** Excel dosyasına aktarır. Bu, veri analizlerinizi ve raporlamalarınızı kolaylaştırır.

### 4. `kiris.py`
Bu dosya, **kiriş detayları** çizmek için kullanılır. Kiriş detaylarını otomatik olarak oluşturur ve zamandan tasarruf etmenizi sağlar.

## **Kurulum ve Kullanım**

Projeyi kullanmaya başlamak için aşağıdaki adımları izleyebilirsiniz:

### **Gereksinimler**
- Python 3.x
- Autocad
- pyautocad kütüphanesi

### **Kurulum**

1. Bu repoyu klonlayın:
    ```sh
    git clone https://github.com/kullaniciadi/proje-adi.git
    ```

2. Gerekli Python kütüphanelerini yükleyin:
    ```sh
    pip install -r requirements.txt
    ```

### **Kullanım**

- **kolon-gui.py** dosyasını çalıştırmak için:
    ```sh
    python kolon-gui.py
    ```

- **table-xlsx.py** dosyasını çalıştırmak için:
    ```sh
    python table-xlsx.py
    ```

- **kiris.py** dosyasını çalıştırmak için:
    ```sh
    python kiris.py
    ```

## **Katkıda Bulunma**

Bu projeye katkıda bulunmak istiyorsanız, lütfen aşağıdaki adımları izleyin:

1. Fork yapın
2. Yeni bir dal (`feature-isim`) oluşturun:
    ```sh
    git checkout -b feature-isim
    ```
3. Değişikliklerinizi commit edin:
    ```sh
    git commit -am 'Yeni özellik ekledim'
    ```
4. Dalınıza push yapın:
    ```sh
    git push origin feature-isim
    ```
5. Bir Pull Request açın


