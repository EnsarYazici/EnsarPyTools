def GetWords(metin,
             target=(0, 3),
             defaultEmptyValue="Tanimlanamadi",
             customSeperator=None,
             unifier=" "):
    kelimeler = metin.split(
        customSeperator) if customSeperator else metin.split()
    print(kelimeler)
    if len(kelimeler) == 0:
        return defaultEmptyValue
    else:
        return unifier.join(kelimeler[target[0]:target[1]])
