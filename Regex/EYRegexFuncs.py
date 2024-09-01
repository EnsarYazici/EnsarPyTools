def Regex_AtoB(Text, A, B, name="word", incA=False, incB=False, ignorecase=False, dotall=False, target="(.*?)", returnList=False):
    # For Name target -> ([a-zA-ZğüşıöçĞÜŞİÖÇ\s-]+) if Names have - or . use ([a-zA-ZğüşıöçĞÜŞİÖÇ\s.-]+)
    # For Everything target -> (.*?)
    pattern = fr'{A}{target}{B}'

    flags = 0
    if ignorecase:
        flags |= re.IGNORECASE
    if dotall:
        flags |= re.DOTALL

    if returnList:
        matches = re.findall(pattern, Text, flags)

        if matches:
            results = []
            for match in matches:
                result = match
                if incA:
                    result = A + result
                if incB:
                    result = result + B
                results.append(result.strip())

            return results
        else:
            print(f"Regex_AtoB -> {name} is Not Matched")
            return ["Tanimlanamadi"]
    else:
        match = re.search(pattern, Text, flags)

        if match:
            result = match.group(1)
            if incA:
                result = A + result
            if incB:
                result = result + B

            return result.strip()
        else:
            print(f"Regex_AtoB -> {name} is Not Matched")
            return "Tanimlanamadi"


def DogrulamaKoduAl_Oulook(metin):
    result = ""
    pat = "(?:(?:\d{1,2})?\s*[-.])?\s*([A-Z0-9]{20})"
    patfull = ""
    for i in range(7):
        patfull += f"\s*(?:{pat})?"

    # print(patfull)

    # \s*(?:{pat})?\s*(?:{pat})?\s*(?:{pat})?\s*(?:{pat})?\s*(?:{pat})?\s*(?:{pat})?\s*(?:{pat})?"

    try:
        pattern = fr"Ek\s*(?:.*)?\s*Do[gĞ]rulama\s*Kod[u]?\s*[:]?{patfull}"
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
                print("else1")
                pattern = r"Do[gĞ]rulama\s*Kod[u]?\s*[:]?\s*(?:\d-)?\s*([A-Za-z0-9]+)"
                DogrulamaKodu = re.findall(pattern, metin,re.IGNORECASE)
                if DogrulamaKodu:
                    print(f"Doğrulama -> {DogrulamaKodu[0]}")
                    result = DogrulamaKodu[0]
        else:
            print("else2")
            pattern = r"Do[gĞ]rulama\s*Kod[u]?\s*[:]?\s*(?:\d-)?\s*([A-Za-z0-9]+)"
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
            print("else3")
            return "Tanimlanamadi"
    except:
        return "Tanimlanamadi"
