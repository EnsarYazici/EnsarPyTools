import os
import struct
import io
import zipfile
from playwright.sync_api import sync_playwright

def extract_crx(crx_path, extract_to):
    """
    CRX dosyasını açıp, versiyona göre header'ı atladıktan sonra
    kalan ZIP verisini çıkartır.
    """
    with open(crx_path, 'rb') as f:
        # İlk 4 bayt: magic number ("Cr24")
        magic = f.read(4)
        if magic != b'Cr24':
            raise ValueError("Geçerli bir CRX dosyası değil!")
        # 4 bayt: sürüm
        version = struct.unpack('<I', f.read(4))[0]
        
        if version == 2:
            # CRX2 formatı: 
            # 4 bayt public key uzunluğu, 4 bayt imza uzunluğu
            pub_key_len = struct.unpack('<I', f.read(4))[0]
            sig_len = struct.unpack('<I', f.read(4))[0]
            # Public key ve imzayı atla
            f.seek(pub_key_len + sig_len, 1)
        elif version == 3:
            # CRX3 formatı: 
            # 4 bayt header uzunluğu (header protokolü protobuf ile kodlanmıştır)
            header_size = struct.unpack('<I', f.read(4))[0]
            # Header kısmını atla
            f.seek(header_size, 1)
        else:
            raise ValueError(f"Desteklenmeyen CRX sürümü: {version}")
        
        # Geri kalan kısım ZIP verisidir
        zip_data = f.read()
    
    try:
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            z.extractall(extract_to)
    except zipfile.BadZipFile as e:
        raise ValueError("Çıkarılan veri geçerli bir zip dosyası değil. CRX formatı desteklenmiyor olabilir.") from e

if __name__ == "__main__":
    # CRX dosyanızın yolunu belirtin
    crx_file_path = "crx_dosyasi"
    # Uzantı dosyalarının çıkarılacağı klasör
    extension_dir = "extracted_extension"
    os.makedirs(extension_dir, exist_ok=True)

    # CRX dosyasını çıkartıyoruz
    extract_crx(crx_file_path, extension_dir)
    print(f"Uzantı dosyaları '{extension_dir}' klasörüne çıkartıldı.")

    # Persistent context için kullanıcı verisi dizini
    user_data_dir = "user_data_dir"
    os.makedirs(user_data_dir, exist_ok=True)

    with sync_playwright() as p:
        # Chromium tarayıcısını başlatıyoruz (headless modda eklentiler çalışmaz)
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=[
                f"--disable-extensions-except={os.path.abspath(extension_dir)}",
                f"--load-extension={os.path.abspath(extension_dir)}"
            ]
        )
        page = context.new_page()
        page.goto("https://www.google.com")
        print("Google'a gidildi. Tarayıcıyı kapatana kadar açık kalacaktır.")

        # Tarayıcı kapatılana kadar bekle
        context.wait_for_event("close")
