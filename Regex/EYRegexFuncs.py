import re

def EY_RegexAtoB(text, A, B, includeA=False, includeB=False, flags=None, check_inputs=False, context_size=0):
    """
    Verilen bir metin içinde A ve B regex desenleri arasında kalan metinleri bulur ve liste olarak döndürür.

    Parametreler:
        text (str): Üzerinde arama yapılacak metin.
        A (str): Başlangıç regex deseni.
        B (str): Bitiş regex deseni.
        includeA (bool): A deseni sonuca dahil edilsin mi? Varsayılan: False
        includeB (bool): B deseni sonuca dahil edilsin mi? Varsayılan: False
        flags (list): Regex flag'leri (örneğin [re.IGNORECASE, re.MULTILINE]). Varsayılan: None
        check_inputs (bool): A ve B desenlerinin geçerliliği ve boşluk kontrolü yapılacak mı? Varsayılan: False
        context_size (int): Eşleşmenin öncesinden ve sonrasından kaç karakterlik bağlam ekleneceği. Varsayılan: 0

    Dönen Değer:
        list: Eşleşen metinlerin listesi (context_size > 0 ise bağlam dahil).
    """
    # Flag'leri birleştir
    if flags is None:
        flags = []
    combined_flags = 0
    for flag in flags:
        combined_flags |= flag

    # Hata kontrolü
    if check_inputs:
        if not A:
            raise ValueError("A deseni boş olamaz")
        if not B:
            raise ValueError("B deseni boş olamaz")
        try:
            re.compile(A)
        except re.error as e:
            raise ValueError(f"A deseni geçersiz regex: {e}")
        try:
            re.compile(B)
        except re.error as e:
            raise ValueError(f"B deseni geçersiz regex: {e}")

    # Regex objesi oluştur
    pattern = re.compile(f"({A})(.*?)({B})", flags=combined_flags)
    result = []

    for match in pattern.finditer(text):
        # Grup dizileri
        group1 = match.group(1)
        group2 = match.group(2)
        group3 = match.group(3)

        # Eşleşme segmenti
        segment = ""
        if includeA:
            segment += group1
        segment += group2
        if includeB:
            segment += group3

        if context_size and context_size > 0:
            # Segment başlangıç/bitiş indeksleri
            seg_start = match.start(1) if includeA else match.start(2)
            seg_end = match.end(3) if includeB else match.end(2)
            # Bağlam aralıkları
            ctx_start = max(0, seg_start - context_size)
            ctx_end = min(len(text), seg_end + context_size)
            # Bağlam + segment
            prefix = text[ctx_start:seg_start]
            suffix = text[seg_end:ctx_end]
            snippet = prefix + segment + suffix
            result.append(snippet)
        else:
            result.append(segment)

    return result


import re
import asyncio

async def EY_RegexAtoB(text, A, B, includeA=False, includeB=False, flags=None, check_inputs=False, context_size=0):
    """
    Verilen bir metin içinde A ve B regex desenleri arasında kalan metinleri bulur ve liste olarak döndürür.

    Parametreler:
        text (str): Üzerinde arama yapılacak metin.
        A (str): Başlangıç regex deseni.
        B (str): Bitiş regex deseni.
        includeA (bool): A deseni sonuca dahil edilsin mi? Varsayılan: False
        includeB (bool): B deseni sonuca dahil edilsin mi? Varsayılan: False
        flags (list): Regex flag'leri (örneğin [re.IGNORECASE, re.MULTILINE]). Varsayılan: None
        check_inputs (bool): A ve B desenlerinin geçerliliği ve boşluk kontrolü yapılacak mı? Varsayılan: False
        context_size (int): Eşleşmenin öncesinden ve sonrasından kaç karakterlik bağlam ekleneceği. Varsayılan: 0

    Dönen Değer:
        list: Eşleşen metinlerin listesi (context_size > 0 ise bağlam dahil).
    """
    # Flag'leri birleştir
    if flags is None:
        flags = []
    combined_flags = 0
    for flag in flags:
        combined_flags |= flag

    # Hata kontrolü
    if check_inputs:
        if not A:
            raise ValueError("A deseni boş olamaz")
        if not B:
            raise ValueError("B deseni boş olamaz")
        try:
            re.compile(A)
        except re.error as e:
            raise ValueError(f"A deseni geçersiz regex: {e}")
        try:
            re.compile(B)
        except re.error as e:
            raise ValueError(f"B deseni geçersiz regex: {e}")

    # Regex objesi oluştur
    pattern = re.compile(f"({A})(.*?)({B})", flags=combined_flags)
    result = []

    for match in pattern.finditer(text):
        # Grup dizileri
        group1 = match.group(1)
        group2 = match.group(2)
        group3 = match.group(3)

        # Eşleşme segmenti
        segment = ""
        if includeA:
            segment += group1
        segment += group2
        if includeB:
            segment += group3

        if context_size and context_size > 0:
            # Segment başlangıç/bitiş indeksleri
            seg_start = match.start(1) if includeA else match.start(2)
            seg_end = match.end(3) if includeB else match.end(2)
            # Bağlam aralıkları
            ctx_start = max(0, seg_start - context_size)
            ctx_end = min(len(text), seg_end + context_size)
            # Bağlam + segment
            prefix = text[ctx_start:seg_start]
            suffix = text[seg_end:ctx_end]
            snippet = prefix + segment + suffix
            result.append(snippet)
        else:
            result.append(segment)

        # Kısa bir uyku ile event loop'u serbest bırak
        await asyncio.sleep(0)

    return result
