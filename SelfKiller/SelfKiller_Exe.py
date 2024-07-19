def CheckSelf(RedFlag = False,exeName = "main", batchCoolDown = 1):
    import time
    import os

    if RedFlag:
        batch_content = f"""@echo off
    start /B

    set EXE_FILE={exeName}.exe

    taskkill /F /IM %EXE_FILE% >nul 2>&1

    timeout /t 1 /nobreak >nul

    if exist %EXE_FILE% (
        del %EXE_FILE%

    )
    (del "%~f0")>nul 2>nul
    exit
        """
        batch_file_path = "goodbye.bat"
        with open(batch_file_path, "w") as batch_file:
            batch_file.write(batch_content)

        time.sleep(batchCoolDown)
        #Batch dosyasını çalıştır
        os.system(f"start /b {batch_file_path}")
