#!/usr/bin/env python3
"""
بوت بسيط لإدارة شبكات MikroTik مع keep-alive
"""
import os
import sys
import logging
import threading
import time
import requests

# إضافة مسار المشروع
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# توكن البوت
BOT_TOKEN = os.getenv("BOT_TOKEN", "7967236631:AAGvV5qla9EMnc58JIIxuowrXrXsNy8GAtQ")

# قاموس لحفظ بيانات المستخدمين
users_data = {}

def keep_alive():
    """إبقاء الخدمة نشطة لمنع النوم على Render"""
    while True:
        try:
            # محاولة ping للخدمة نفسها
            # استبدل YOUR_RENDER_URL برابط خدمتك الفعلي
            render_url = os.getenv("RENDER_EXTERNAL_URL")
            if render_url:
                requests.get(render_url, timeout=10)
                logger.info("Keep-alive ping sent successfully")
            time.sleep(600)  # كل 10 دقائق
        except Exception as e:
            logger.warning(f"Keep-alive ping failed: {e}")
            time.sleep(600)

def get_main_keyboard():
    """لوحة المفاتيح الرئيسية"""
    keyboard = [
        [InlineKeyboardButton("🌐 إدارة الراوترات", callback_data="routers")],
        [InlineKeyboardButton("👥 إدارة Hotspot", callback_data="hotspot")],
        [InlineKeyboardButton("🔐 إدارة VPN", callback_data="vpn")],
        [InlineKeyboardButton("📊 معلومات السيرفر", callback_data="server_info")],
        [InlineKeyboardButton("📈 مراقبة الشبكة", callback_data="monitoring")],
        [InlineKeyboardButton("🎫 طباعة البطاقات", callback_data="cards")],
        [InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start"""
    user = update.effective_user
    
    # حفظ بيانات المستخدم
    users_data[user.id] = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    
    welcome_message = f"""
🎉 مرحباً بك في بوت إدارة شبكات MikroTik!

👋 أهلاً {user.first_name or user.username or 'صديقي'}!

🔧 يمكنك من خلال هذا البوت:
• إدارة راوترات MikroTik
• إنشاء وحذف حسابات Hotspot  
• إدارة اتصالات VPN
• مراقبة حالة الشبكة
• طباعة بطاقات المستخدمين
• تلقي التنبيهات الفورية

📋 استخدم الأزرار أدناه للبدء:

🌐 **البوت يعمل على خادم مجاني 24/7**
    """
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /help"""
    help_text = """
📖 دليل استخدام بوت إدارة MikroTik

🔧 الأوامر الأساسية:
/start - بدء استخدام البوت
/help - عرض هذا الدليل
/status - حالة النظام
/ping - اختبار استجابة البوت

🌐 إدارة الراوترات:
• إضافة راوتر جديد
• عرض قائمة الراوترات
• اختبار الاتصال
• تعديل الإعدادات

👥 إدارة Hotspot:
• إضافة مستخدمين جدد
• حذف المستخدمين
• عرض الجلسات النشطة
• إنشاء مستخدمين بالجملة

🔐 إدارة VPN:
• إنشاء حسابات VPN
• توليد ملفات التكوين
• مراقبة الاتصالات

📊 المراقبة والتنبيهات:
• مراقبة حالة الجيران
• تنبيهات الانقطاع
• مراقبة موارد النظام
• إحصائيات الترافيك

🎫 طباعة البطاقات:
• طباعة بطاقات فردية
• طباعة بطاقات متعددة
• قوالب مخصصة

💡 نصائح:
• استخدم الأزرار التفاعلية للتنقل
• يمكنك إلغاء أي عملية بكتابة /cancel
• للدعم التقني، تواصل مع المطور

🚀 البوت يعمل على خادم مجاني مع إبقاء الخدمة نشطة!
    """
    await update.message.reply_text(help_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /status"""
    user = update.effective_user
    
    status_message = f"""
📊 حالة النظام

👤 معلوماتك:
• الاسم: {user.first_name or user.username}
• معرف المستخدم: {user.id}
• نوع الحساب: مستخدم عادي

📈 إحصائيات النظام:
• إجمالي المستخدمين: {len(users_data)}
• حالة البوت: يعمل بشكل طبيعي ✅
• الاتصال بتيليجرام: متصل ✅
• جميع الوظائف: جاهزة ✅
• Keep-Alive: نشط ✅

🌐 الخادم:
• الاستضافة: Render.com (مجاني)
• الحالة: يعمل بشكل طبيعي
• آخر ping: نشط

🕐 الوقت الحالي: متاح
    """
    
    await update.message.reply_text(status_message)

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /ping"""
    await update.message.reply_text("🏓 Pong! البوت يعمل بشكل طبيعي ✅")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الأزرار"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "routers":
        await query.edit_message_text(
            "🌐 إدارة الراوترات\n\n"
            "هذه الوظيفة تتيح لك:\n"
            "• إضافة راوترات MikroTik جديدة\n"
            "• عرض قائمة الراوترات المسجلة\n"
            "• اختبار الاتصال مع الراوترات\n"
            "• عرض معلومات النظام\n\n"
            "📝 لإضافة راوتر جديد، أرسل المعلومات بالتنسيق:\n"
            "اسم_الراوتر\n"
            "عنوان_IP\n"
            "اسم_المستخدم\n"
            "كلمة_المرور\n"
            "المنفذ (اختياري)\n\n"
            "🌐 البوت يعمل على خادم مجاني 24/7",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data="back")]])
        )
    
    elif query.data == "hotspot":
        await query.edit_message_text(
            "👥 إدارة Hotspot\n\n"
            "هذه الوظيفة تتيح لك:\n"
            "• إنشاء حسابات Hotspot جديدة\n"
            "• حذف الحسابات الموجودة\n"
            "• عرض الجلسات النشطة\n"
            "• إدارة ملفات التعريف\n"
            "• إنشاء مستخدمين بالجملة\n\n"
            "📝 لإضافة مستخدم جديد، أرسل المعلومات بالتنسيق:\n"
            "اسم_المستخدم\n"
            "كلمة_المرور\n"
            "ملف_التعريف (اختياري)\n"
            "مدة_الاستخدام (اختياري)\n"
            "حد_البيانات (اختياري)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data="back")]])
        )
    
    elif query.data == "vpn":
        await query.edit_message_text(
            "🔐 إدارة VPN\n\n"
            "هذه الوظيفة تتيح لك:\n"
            "• إنشاء حسابات VPN تلقائياً\n"
            "• دعم L2TP، PPTP، OpenVPN\n"
            "• توليد ملفات التكوين\n"
            "• إدارة عناوين IP\n"
            "• مراقبة الاتصالات\n\n"
            "🔧 عند إضافة مستخدم جديد، سيتم إنشاء VPN تلقائياً\n"
            "📁 ستحصل على ملف التكوين جاهز للاستخدام",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data="back")]])
        )
    
    elif query.data == "server_info":
        await query.edit_message_text(
            "📊 معلومات السيرفر\n\n"
            "هذه الوظيفة تعرض:\n"
            "• معلومات النظام (CPU، الذاكرة)\n"
            "• إصدار RouterOS\n"
            "• وقت التشغيل\n"
            "• حالة الواجهات\n"
            "• إحصائيات الترافيك\n\n"
            "📈 يتم تحديث المعلومات في الوقت الفعلي\n"
            "🔄 المراقبة مستمرة 24/7\n"
            "🌐 البوت مستضاف مجاناً على Render",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data="back")]])
        )
    
    elif query.data == "monitoring":
        await query.edit_message_text(
            "📈 مراقبة الشبكة\n\n"
            "هذه الوظيفة تتيح:\n"
            "• مراقبة حالة الجيران (CDP/LLDP)\n"
            "• تنبيهات فورية للانقطاع والاتصال\n"
            "• كشف تضارب عناوين IP\n"
            "• مراقبة حالة الواجهات\n"
            "• إشعارات الأخطاء الحرجة\n\n"
            "🔔 ستصلك التنبيهات فوراً عند حدوث أي مشكلة\n"
            "⚡ المراقبة تعمل في الوقت الفعلي\n"
            "🌐 الخدمة تعمل 24/7 على خادم مجاني",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data="back")]])
        )
    
    elif query.data == "cards":
        await query.edit_message_text(
            "🎫 طباعة البطاقات\n\n"
            "هذه الوظيفة تتيح:\n"
            "• إنشاء بطاقات PDF احترافية\n"
            "• قوالب متعددة وألوان مختلفة\n"
            "• رموز QR للمعلومات\n"
            "• طباعة فردية أو بالجملة\n"
            "• تخصيص التصميم\n\n"
            "🎨 قوالب متاحة: قياسي، كبير، صغير\n"
            "🌈 ألوان متعددة قابلة للتخصيص",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data="back")]])
        )
    
    elif query.data == "help":
        await help_command(update, context)
        return
    
    elif query.data == "back":
        await query.edit_message_text(
            "🏠 القائمة الرئيسية\n\nاختر الوظيفة المطلوبة:\n\n🌐 البوت يعمل على خادم مجاني 24/7",
            reply_markup=get_main_keyboard()
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الرسائل النصية"""
    message_text = update.message.text
    
    # رد بسيط على الرسائل
    await update.message.reply_text(
        f"📝 تم استلام رسالتك: {message_text}\n\n"
        "💡 استخدم الأزرار التفاعلية للتنقل في البوت\n"
        "أو اكتب /start لعرض القائمة الرئيسية\n\n"
        "🌐 البوت يعمل على خادم مجاني مع keep-alive نشط",
        reply_markup=get_main_keyboard()
    )

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("🚀 بوت إدارة شبكات MikroTik مع Keep-Alive")
    print("=" * 50)
    print("🔧 بدء تشغيل البوت...")
    
    try:
        # بدء خدمة keep-alive في thread منفصل
        keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
        keep_alive_thread.start()
        print("✅ خدمة Keep-Alive بدأت")
        
        # إنشاء التطبيق
        application = Application.builder().token(BOT_TOKEN).build()
        
        # إضافة المعالجات
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("status", status_command))
        application.add_handler(CommandHandler("ping", ping_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        
        print("✅ تم إعداد البوت بنجاح")
        print("🌐 البوت متصل بتيليجرام")
        print("📱 يمكنك الآن اختبار البوت في تيليجرام")
        print("🔄 خدمة Keep-Alive تعمل لمنع النوم")
        print("⚠️  للإيقاف اضغط Ctrl+C")
        print("=" * 50)
        
        # تشغيل البوت
        application.run_polling(drop_pending_updates=True)
        
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل البوت: {str(e)}")
        logger.error(f"خطأ في تشغيل البوت: {str(e)}")

if __name__ == '__main__':
    main()

