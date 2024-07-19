def GetWords(text, target=(0, 3), defaultEmptyValue="Tanimlanamadi", customSeperator=None, unifier=" "):
    words = text.split(
        customSeperator) if customSeperator else text.split()
    # print(words)
    if len(words) == 0:
        return defaultEmptyValue
    else:
        return unifier.join(words[target[0]:target[1]])
