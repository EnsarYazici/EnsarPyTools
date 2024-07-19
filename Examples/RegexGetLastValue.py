def DogrulamaKoduAl(metin):
    result = ""
    pat1 = "(?:1[-.])?\s*([A-Za-z0-9]+)"
    pat2 = "(?:2[-.])?\s*([A-Za-z0-9]+)"
    pat3 = "(?:3[-.])?\s*([A-Za-z0-9]+)"
    pat4 = "(?:4[-.])?\s*([A-Za-z0-9]+)"
    pat5 = "(?:5[-.])?\s*([A-Za-z0-9]+)"
    pat6 = "(?:6[-.])?\s*([A-Za-z0-9]+)"
    pat7 = "(?:7[-.])?\s*([A-Za-z0-9]+)"

    try:
        pattern = fr"Ek\s*(?:Rapor)?\s*Do[gĞ]rulama\s*Kod[u]?\s*[:]\s*(?:{pat1})?\s*(?:{pat2})?\s*(?:{pat3})?\s*(?:{pat4})?\s*(?:{pat5})?\s*(?:{pat6})?\s*(?:{pat7})?"
        DogrulamaKodu = re.findall(pattern, metin,re.IGNORECASE)
        if DogrulamaKodu:
            kod = ""
            for i in range(len(DogrulamaKodu[0])):
                if DogrulamaKodu[0][(len(DogrulamaKodu[0])-1)-i] != "Not" and DogrulamaKodu[0][(len(DogrulamaKodu[0])-1)-i] != "":
                    kod = DogrulamaKodu[0][(len(DogrulamaKodu[0])-1)-i]
                    break
            if kod != "":
                print(f"Ek Karar -> {kod}")
                result = kod
            else:
                pattern = r"Do[gĞ]rulama\s*Kod[u]?\s*[:]\s*(?:\d-)?\s*([A-Za-z0-9]+)"
                DogrulamaKodu = re.findall(pattern, metin,re.IGNORECASE)
                if DogrulamaKodu:
                    print(f"Doğrulama -> {DogrulamaKodu[0]}")
                    result = DogrulamaKodu[0]
        else:
            pattern = r"Do[gĞ]rulama\s*Kod[u]?\s*[:]\s*(?:\d-)?\s*([A-Za-z0-9]+)"
            DogrulamaKodu = re.findall(pattern, metin,re.IGNORECASE)
            if DogrulamaKodu:
                print(f"Doğrulama -> {DogrulamaKodu[0]}")
                result = DogrulamaKodu[0]

        def check_string(s):
            pattern = r'^[A-Z0-9]{20}$'
            return re.match(pattern, s) is not None

        if check_string(result):
            return result
        else:
            return "Tanimlanamadi"
    except:
        return "Tanimlanamadi"




text = """Bilirkişi Raporu Doğrulama Kodu : ZPM7J06M38JP5YYOKG13
Bilirkişi Raporu Linki : https://online.sbm.org.tr:443/sbm-belge/public/belgeDogrulama/sorgu.sbm
Ek Rapor Doğrulama Kodu: 1-ABC7J06M38JP5YYOKG13 2-2BC7J06M38JP5YYOKG13 3-3BC7J06M38JP5YYOKG13 4-4BC7J06M38JP5YYOKG13 5-5BC7J06M38JP5YYOKG13
Not : Bilirkişi Raporuna karşı itirazlarınızı lütfen mustafameric.hakem@sigortatahkim.org.tr adresine yapınız. Bu maile dönüş yaptığınız takdirde dikkate alınmayacaktır.
Saygılarımızla.
SİGORTA TAHKİM KOMİSYONU"""

result = DogrulamaKoduAl(text)
print("result . ",result)
