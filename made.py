import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import names
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# إعداد المتصفح
def get_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')  # تشغيل بدون واجهة
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return uc.Chrome(options=options)

# إعداد ملفات الحسابات
def setup_account_files(platforms):
    if not os.path.exists("accounts"):
        os.mkdir("accounts")
    for platform in platforms:
        path = f"accounts/{platform}.txt"
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("")

# جلب إيميل من موقع مهمل
def get_temp_email(driver):
    driver.get("https://www.moakt.com/en")
    time.sleep(3)
    email_input = driver.find_element(By.ID, "email")
    return email_input.get_attribute("value")

# جلب كود التفعيل
def get_verification_code(driver):
    for _ in range(10):
        time.sleep(5)
        driver.refresh()
        soup = driver.page_source
        if "confirm your email" in soup.lower():
            start = soup.find("code:") + len("code: ")
            code = soup[start:start + 6]
            return code.strip()
    return None

# إنشاء حساب فيسبوك
def create_facebook(driver, email, password):
    fname = names.get_first_name()
    lname = names.get_last_name()
    print(f"[+] صنع حساب فيسبوك على {email}")
    driver.get("https://www.facebook.com/r.php")
    time.sleep(3)
    driver.find_element(By.NAME, "firstname").send_keys(fname)
    driver.find_element(By.NAME, "lastname").send_keys(lname)
    driver.find_element(By.NAME, "reg_email__").send_keys(email)
    driver.find_element(By.NAME, "reg_email_confirmation__").send_keys(email)
    driver.find_element(By.NAME, "reg_passwd__").send_keys(password)
    driver.find_element(By.NAME, "birthday_day").send_keys("10")
    driver.find_element(By.NAME, "birthday_month").send_keys("Jan")
    driver.find_element(By.NAME, "birthday_year").send_keys("1998")
    driver.find_element(By.XPATH, "//input[@value='2']").click()
    driver.find_element(By.NAME, "websubmit").click()
    print("[*] بإنتظار كود التفعيل...")
    code = get_verification_code(driver)
    if code:
        print(f"[+] الكود: {code}")
        driver.find_element(By.NAME, "code").send_keys(code)
        driver.find_element(By.NAME, "confirm").click()
        with open("accounts/facebook.txt", "a") as f:
            f.write(f"{email} | {password}\n")
    else:
        print("[-] فشل التفعيل لفيسبوك.")

# إنشاء حساب تيك توك
def create_tiktok(driver, email, password):
    print(f"[+] صنع حساب تيك توك على {email}")
    driver.get("https://www.tiktok.com/signup/phone-or-email/email")
    time.sleep(5)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(),'Sign up')]").click()
    print("[*] بإنتظار كود التفعيل...")
    code = get_verification_code(driver)
    if code:
        print(f"[+] الكود: {code}")
        driver.find_element(By.NAME, "code").send_keys(code)
        driver.find_element(By.XPATH, "//button[contains(text(),'Confirm')]").click()
        with open("accounts/tiktok.txt", "a") as f:
            f.write(f"{email} | {password}\n")
    else:
        print("[-] فشل التفعيل لتيك توك.")

# إنشاء حساب إنستغرام
def create_instagram(driver, email, password):
    print(f"[+] صنع حساب إنستغرام على {email}")
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    time.sleep(3)
    driver.find_element(By.NAME, "emailOrPhone").send_keys(email)
    driver.find_element(By.NAME, "fullName").send_keys(names.get_full_name())
    driver.find_element(By.NAME, "username").send_keys(f"{names.get_first_name()}{random.randint(100, 999)}")
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(),'Sign up')]").click()
    time.sleep(3)
    print("[*] بإنتظار كود التفعيل...")
    code = get_verification_code(driver)
    if code:
        print(f"[+] الكود: {code}")
        driver.find_element(By.NAME, "verificationCode").send_keys(code)
        driver.find_element(By.XPATH, "//button[contains(text(),'Confirm')]").click()
        with open("accounts/instagram.txt", "a") as f:
            f.write(f"{email} | {password}\n")
    else:
        print("[-] فشل التفعيل لإنستغرام.")

# واجهة المستخدم
def main():
    start_time = time.time()
    platforms = ["facebook", "tiktok", "instagram"]
    setup_account_files(platforms)

    print("اختر المنصة:")
    print("1. Facebook")
    print("2. TikTok")
    print("3. Instagram")
    print("4. كل المنصات")
    choice = input("اختيارك (رقم): ").strip()

    count = int(input("كم عدد الحسابات؟ "))
    use_custom_pass = input("هل تريد كلمة سر موحدة؟ (y/n): ").strip().lower()
    if use_custom_pass == 'y':
        password = input("أدخل كلمة السر الموحدة: ")
    else:
        password = None

    for _ in range(count):
        driver = get_driver()
        try:
            email = get_temp_email(driver)
            time.sleep(2)

            if not password:
                passwd = f"Abc{random.randint(1000,9999)}"
            else:
                passwd = password

            if choice == '1':
                create_facebook(driver, email, passwd)
            elif choice == '2':
                create_tiktok(driver, email, passwd)
            elif choice == '3':
                create_instagram(driver, email, passwd)
            elif choice == '4':
                create_facebook(driver, email, passwd)
                create_tiktok(driver, email, passwd)
                create_instagram(driver, email, passwd)
            else:
                print("خيار غير صحيح.")
                break
        except Exception as e:
            print(f"[!] خطأ: {e}")
        finally:
            driver.quit()

    end_time = time.time()
    print(f"[+] العملية اكتملت في {round(end_time - start_time, 2)} ثانية.")

if __name__ == "__main__":
    main()