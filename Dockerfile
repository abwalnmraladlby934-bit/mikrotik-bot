# استخدام Python 3.11 كصورة أساسية
FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات المشروع
COPY . .

# إنشاء المجلدات المطلوبة
RUN mkdir -p logs temp/cards

# تعيين الصلاحيات
RUN chmod +x simple_bot.py

# تعريف المنفذ
EXPOSE 5000

# الأمر الافتراضي لتشغيل البوت
CMD ["python", "simple_bot.py"]

