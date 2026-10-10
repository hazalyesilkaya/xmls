import zipfile
import os
import io

# Zip dosyalarının olduğu yer (Orijinaller burada sapasağlam kalacak)
kaynak_klasor = r"C:\Users\yesil\Downloads"

# Çıkarılacak yer (Şu an bulunduğun muzik-xmls klasörü)
hedef_klasor = "."

sayac = 0

for dosya_adi in os.listdir(kaynak_klasor):
    if dosya_adi.endswith('.zip'):
        zip_yolu = os.path.join(kaynak_klasor, dosya_adi)
        print(f"İşleniyor: {dosya_adi}")
        
        with zipfile.ZipFile(zip_yolu, 'r') as z:
            for filename in z.namelist():
                # files/ klasöründeki .mxl dosyalarını bul
                if 'files/' in filename and filename.endswith('.mxl'):
                    mxl_dosya_adi = os.path.basename(filename)
                    mxl_data = z.read(filename)
                    
                    try:
                        with zipfile.ZipFile(io.BytesIO(mxl_data)) as mxl_zip:
                            # MXL içindeki xml dosyalarını bul
                            xml_dosyalari = [f for f in mxl_zip.namelist() if f.endswith('.xml')]
                            asil_xml = None
                            
                            # container.xml dışındaki asıl nota XML'ini bul
                            for x in xml_dosyalari:
                                if 'container.xml' not in x.lower():
                                    asil_xml = x
                                    break
                            
                            if not asil_xml and xml_dosyalari:
                                asil_xml = xml_dosyalari[0]
                            
                            # BULUNAN XML'İ BURAYA KOPYALAYARAK KAYDEDİYORUZ (Silme işlemi kesinlikle yok)
                            if asil_xml:
                                yeni_ad = mxl_dosya_adi.replace('.mxl', '.xml')
                                hedef_yol = os.path.join(hedef_klasor, yeni_ad)
                                
                                # İçeriği okuyup buradaki yeni dosyaya yazıyoruz (Kopyalama)
                                with open(hedef_yol, 'wb') as f_out:
                                    f_out.write(mxl_zip.read(asil_xml))
                                sayac += 1
                                
                    except zipfile.BadZipFile:
                        print(f"Hata: {mxl_dosya_adi} okunurken sorun oluştu, atlanıyor.")

print(f"\nİşlem bitti! Toplam {sayac} adet saf XML dosyası güvenle kopyalanarak muzik-xmls klasörüne kaydedildi.")