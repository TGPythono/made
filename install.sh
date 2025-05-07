### **2. ملف Shell (install.sh)**

ملف **install.sh** سيساعد على تثبيت جميع المتطلبات تلقائيًا. افتح محرر النصوص وأنشئ الملف، ثم الصق فيه ما يلي:

```bash
#!/bin/bash

# تحديث Termux
echo "تحديث Termux..."
pkg update && pkg upgrade -y

# تثبيت Python
echo "تثبيت Python..."
pkg install python -y

# تثبيت pip
echo "تثبيت pip..."
pkg install python-pip -y

# تثبيت Git
echo "تثبيت Git..."
pkg install git -y

# تثبيت Chromium
echo "تثبيت Chromium..."
pkg install chromium -y

# تثبيت المكتبات المطلوبة عبر pip
echo "تثبيت المكتبات المطلوبة..."
pip install selenium undetected-chromedriver names

echo "تم تثبيت جميع المتطلبات بنجاح!"
echo "الآن يمكنك تشغيل السكربت باستخدام الأمر:"
echo "python auto_accounts.py"
