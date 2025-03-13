import asyncio
import os
import aiohttp
import base64
import xml.etree.ElementTree as ET

async def E_Devlet_Login(page,tc,passw):
    await page.get_by_label("T. C. Kimlik Numaranızı Girin").click()
    await page.get_by_label("T. C. Kimlik Numaranızı Girin").fill(tc)
    await page.get_by_label("e-Devlet Şifrenizi Girin").click()
    await page.get_by_label("e-Devlet Şifrenizi Girin").fill(passw)
    await page.get_by_label("Güvenlik Kodu").click()

    # Captcha'yı kullanıcıdan al
    captchaImage = await is_element_exists(page, "img.captchaImage", timeout=5000)
    if captchaImage:
        await captchaImage.screenshot(path="captcha.png")
        captcha = await SolveCaptcha_ImageToText("API_KEY", "captcha.png")
        await page.get_by_label("Güvenlik Kodu").fill(captcha)

    # Giriş Yap butonuna bas
    await page.get_by_role("button", name="Giriş Yap").click()

async def E_Devlet_Login_Spam(page,tc,passw):
    for i in range(5):
        await E_Devlet_Login(page,tc,passw)
        
        Alert = await is_element_exists(page, ".alert-icon", timeout=5000)
        if Alert:
            print(f"{i+1}. E-Devlet Girişi Başarısız")
            continue
        else:
            print(f"{i+1}. E-Devlet Girişi Başarılı")
            return True



async def SolveCaptcha_RecaptchaV2(api_key, site_key, page_url, spamValue=1):
    payload = {
        "clientKey": api_key,
        "task": {
            "type": "RecaptchaV2TaskProxyless",
            "websiteURL": page_url,
            "websiteKey": site_key
        }
    }

    async with aiohttp.ClientSession() as session:
        # Görevi Anti-Captcha'ya gönder
        async with session.post('https://api.anti-captcha.com/createTask', json=payload) as response:
            response_data = await response.json()

        if response_data.get("errorId", 0) != 0:
            print(f"Hata: {response_data.get('errorDescription', 'Hata oluştu')}")
            return

        task_id = response_data['taskId']
        print(f"Görev oluşturuldu, task_id: {task_id}")

        check_payload = {"clientKey": api_key, "taskId": task_id}

        while True:
            async with session.post('https://api.anti-captcha.com/getTaskResult', json=check_payload) as result:
                result_data = await result.json()

            if result_data['status'] == 'ready':
                print(f"Çözülen CAPTCHA metni: {result_data['solution']['gRecaptchaResponse']}")
                return result_data['solution']['gRecaptchaResponse']
            elif result_data['status'] == 'processing':
                print("Görev hala işleniyor, bekleniyor...")
                await asyncio.sleep(spamValue)  # Bekleme süresi, isteğe bağlı olarak ayarlanabilir
            else:
                print(f"Hata: {result_data.get('errorDescription', 'Bilinmeyen hata')}")
                break
        return None




async def SolveCaptcha_ImageToText(api_key, image_path, spamValue=1):
    # Resmi base64 formatına çevir
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Görev oluşturma isteği için yük verisi
    payload = {
        "clientKey": api_key,
        "task": {
            "type": "ImageToTextTask",  # Kelime yazma CAPTCHA'sı için görev türü
            "body": image_base64,       # Base64 formatındaki resim
            "phrase": False,            # Birden fazla kelime değil
            "case": False,              # Büyük/küçük harf duyarlılığı yok
            "numeric": False,           # Sayısal değil
            "math": False,              # Matematiksel işlem değil
            "minLength": 0,             # Minimum uzunluk (isteğe bağlı)
            "maxLength": 10             # Maksimum uzunluk (örneğin 5-6 harfli kelimeler için)
        }
    }

    async with aiohttp.ClientSession() as session:
        # Görevi Anti-Captcha'ya gönder
        async with session.post('https://api.anti-captcha.com/createTask', json=payload) as response:
            response_data = await response.json()

        # Hata kontrolü
        if response_data.get("errorId", 0) != 0:
            print(f"Hata: {response_data['errorDescription']}")
            return

        # Görev ID'sini al
        task_id = response_data['taskId']
        print(f"Görev oluşturuldu, task_id: {task_id}")

        # Görevin tamamlanmasını kontrol etmek için yük
        check_payload = {
            "clientKey": api_key,
            "taskId": task_id
        }

        while True:
            async with session.post('https://api.anti-captcha.com/getTaskResult', json=check_payload) as result:
                result_data = await result.json()

            if result_data['status'] == 'ready':
                # CAPTCHA çözüldüğünde kelimeyi yazdır
                captcha_text = result_data['solution']['text']
                print(f"Çözülen CAPTCHA metni: {captcha_text}")
                return captcha_text
            elif result_data['status'] == 'processing':
                print("Görev hala işleniyor, bekleniyor...")
                await asyncio.sleep(spamValue)
            else:
                print(f"Hata: {result_data.get('errorDescription', 'Bilinmeyen hata')}")
                break
        return None


async def is_element_exists(page, selector, timeout=5000):
    """
    Playwright ile belirtilen elementin var olup olmadığını kontrol eder.
    :param page: Playwright page nesnesi
    :param selector: CSS veya XPath seçici
    :param timeout: Maksimum bekleme süresi (ms cinsinden, varsayılan: 5000ms)
    :return: Element bulunduysa locator nesnesi, bulunamazsa False
    """
    try:
        # Belirtilen süre boyunca elementi bekle
        await page.wait_for_selector(selector, timeout=timeout)
        return page.locator(selector)  # Elementi döndür
    except:
        return False  # Element bulunamazsa False döndür
    


async def get_value_from_xml_async(xml_data,
                                   xpath=None,
                                   tag=None,
                                   text_contains=None,
                                   attribute=None,
                                   attribute_value=None,
                                   return_attribute=None):
    """
    Esnek XML veri çekme fonksiyonunun asenkron versiyonu.

    Parametreler:
      - xml_data: İşlenecek XML verisi (string formatında).
      - xpath: Belirli bir XPath sorgusu. Sağlanırsa, bu sorguya uyan elementler üzerinde işlem yapılır.
      - tag: Sadece belirtilen tag'e sahip elementler işleme alınır.
      - text_contains: Elementin metin içeriğinde aranacak alt string (büyük/küçük harf duyarsız).
      - attribute: Elementin sahip olması gereken attribute adı.
      - attribute_value: Eğer attribute belirtilmişse, elementin bu attribute değeri bu değere eşit olmalıdır.
      - return_attribute: Eğer belirtilirse, döndürülecek değer elementin metni yerine bu attribute'nun değeri olur.

    Dönüş:
      - Filtrelere uyan elementlerin metin veya belirtilen attribute değerlerini içeren liste.
    """

    root = ET.fromstring(xml_data)
    if xpath:
        elements = root.findall(xpath)
    else:
        elements = list(root.iter())

    results = []
    for elem in elements:
        # Tag filtresi uygulanıyorsa
        if tag and elem.tag != tag:
            continue

        # Attribute filtresi uygulanıyorsa
        if attribute:
            if attribute not in elem.attrib:
                continue
            if attribute_value and elem.attrib[attribute] != attribute_value:
                continue

        # Metin filtresi uygulanıyorsa
        if text_contains:
            if not elem.text or text_contains.lower() not in elem.text.lower():
                continue

        # Sonuç olarak metin veya belirtilen attribute değerini döndür
        if return_attribute:
            value = elem.attrib.get(return_attribute, "")
        else:
            value = elem.text.strip() if elem.text else ""
        results.append(value)
    return results

async def get_files(klasor_yolu):
    list = []
    # os.walk, klasör içindeki tüm dizinleri, alt dizinleri ve dosyaları döner.
    for dizin, alt_dizinler, dosyalar in os.walk(klasor_yolu):
        for dosya in dosyalar:
            list.append(dosya)
    return list
