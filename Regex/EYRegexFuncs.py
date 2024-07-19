def Regex_AtoB(Text, A, B, name = "word" ,incA = False, incB = False,ignorecase = False,returnList = False):

    pattern = fr'{A}(.*?){B}'

    flags = re.IGNORECASE if ignorecase else 0

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
        match = re.search(pattern, Text,flags)

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
