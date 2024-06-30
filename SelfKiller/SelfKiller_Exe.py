# For döngüsü ile 0'dan 100'e kadar sayma
for i in range(6):
    print(str(5-i)+"  ",end="\r")
    time.sleep(1)  # Sayıları yavaşça göstermek için

# Sayı 100 olduğunda batch dosyasını oluştur
if i == 5:
    batch_content = f"""@echo off
start /B

set EXE_FILE=xxx.exe

taskkill /F /IM %EXE_FILE% >nul 2>&1

timeout /t 1 /nobreak >nul

if exist %EXE_FILE% (
    del %EXE_FILE%

)
(del "%~f0")>nul 2>nul
exit
    """
    batch_file_path = "delete_files.bat"
    with open(batch_file_path, "w") as batch_file:
        batch_file.write(batch_content)

    time.sleep(1)
    #Batch dosyasını çalıştır
    os.system(f"start /b {batch_file_path}")
