from datetime import datetime
import traceback

def faulty_function():
    # Bilerek bir hata oluşturan fonksiyon
    return 1 / 0  # Sıfıra bölme hatası

try:
    faulty_function()
except Exception as e:
    # Bugünün tarihini al ve uygun formatta bir stringe dönüştür
    tarih = datetime.now().strftime("%Y-%m-%d")
    dosya_adi = f"ErrorLogs\\ErrorLog_{tarih}.txt"

    with open(dosya_adi, "a",encoding="utf-8") as f:
        hour = datetime.now().strftime("%H:%M:%S")
        f.write(f"\nHata türü: {type(e).__name__}___{hour}\n")
        f.write("Hata mesajı: {}\n".format(e))
        f.write("Hata izleme bilgisi:\n")
        traceback.print_exc(file=f)
        f.write("\n---\n")
