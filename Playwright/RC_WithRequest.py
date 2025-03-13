import requests
from playwright.sync_api import sync_playwright
import time

# Anti-Captcha API ayarları
api_key = "your_api_key"
site_key = "site_key_of_the_page"
page_url = "url_of_the_page"

# Anti-Captcha ile reCAPTCHA çözümü
payload = {
    "clientKey": api_key,
    "task": {
        "type": "RecaptchaV2TaskProxyless",
        "websiteURL": page_url,
        "websiteKey": site_key
    }
}

response = requests.post('https://api.anti-captcha.com/createTask', json=payload)
task_id = response.json()['taskId']

# Görevi kontrol et
while True:
    check_payload = {"clientKey": api_key, "taskId": task_id}
    result = requests.post('https://api.anti-captcha.com/getTaskResult', json=check_payload)
    if result.json()['status'] == 'ready':
        g_recaptcha_response = result.json()['solution']['gRecaptchaResponse']
        print("reCAPTCHA çözümü alındı:", g_recaptcha_response)
        break
    time.sleep(1)  # Biraz bekleyerek sunucuyu yormamak için

# Playwright ile sayfaya enjeksiyon
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=True yaparsanız tarayıcı görünmez
    page = browser.new_page()
    
    # Hedef sayfaya git
    page.goto(page_url)
    
    # reCAPTCHA response alanını doldurmak için JavaScript enjeksiyonu
    page.evaluate('''(gResponse) => {
        let element = document.getElementById("g-recaptcha-response");
        if (element) {
            element.style.display = "";  // Görünür yap
            element.innerHTML = gResponse;  // Değeri ekle
            element.style.display = "none";  // Tekrar gizle
        }
    }''', g_recaptcha_response)
    
    # Formu göndermek için gerekirse bir butona tıklama ekleyebilirsiniz
    # Örnek: page.click("selector_for_submit_button")
    
    # Sayfanın yüklenmesini beklemek için
    time.sleep(5)  # İhtiyaca göre ayarlayın
    
    # Tarayıcıyı kapat
    browser.close()
