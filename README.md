# Tadbircore365

**Tadbircore365** — bu biznes egalari va tadbirkorlar uchun tezkor kredit arizalarini topshirish, hisob-kitoblarni amalga oshirish va bevosita mutaxassislar bilan bog'lanish imkonini beruvchi kompleks avtomatlashtirilgan tizim. U o'z ichiga Telegram bot va qulay Web Dashboardni qamrab oladi.

## 🎯 Loyihaning Maqsadi
Mijozlarga bank kreditlari bo'yicha ma'lumot olish, eng ma'qul foizli kreditlarni topish, arizalarni uydan chiqmasdan Telegram orqali yuborish va savollarga operatorlardan real vaqtda javob olish imkoniyatini taqdim etish. Banklar va xodimlar uchun esa kelib tushayotgan arizalar hamda murojaatlarni samarali markazlashgan holda boshqarish.

## ⚙️ Loyihaning Vazifasi va Funksiyalari

### Telegram Bot imkoniyatlari:
- **🏢 Kredit tanlash va ariza yuborish:** Foydalanuvchining STIR (INN) yoki JShShIR ma'lumotlari asosida mos bankni tanlash va kredit arizasini shakllantirish.
- **🧮 Kredit kalkulyatori:** Kerakli summa, muddat va foiz stavkasiga ko'ra oylik to'lovlarni hisoblab berish.
- **💬 Jonli chat (Live Chat):** Foydalanuvchilarning bevosita operatorlar bilan Telegram bot orqali yozishish imkoniyati.
- **📝 Murojaat qoldirish:** Shikoyat, taklif yoki savollarni yozma ravishda adminlarga yetkazish.
- **🤖 AI-maslahatchi & Yordam/FAQ:** Avtomatlashtirilgan tezkor javoblar va ma'lumotlar bazasi.

### Web Dashboard (Boshqaruv Paneli) imkoniyatlari:
- **📊 Asosiy Dashboard:** Barcha kelib tushgan arizalar va ularning holatlari bo'yicha statistik ma'lumotlar va grafiklar.
- **📄 Arizalar ro'yxati:** Qabul qilingan barcha arizalarni ko'rish, qidirish va ularning holatini ("Kutilyapti", "Qabul qilindi", "Tasdiqlandi", "Rad etildi") o'zgartirish.
- **💬 Live Chat Monitoring:** Foydalanuvchilar va operatorlar o'rtasidagi faol yozishmalarni onlayn kuzatish paneli.
- **📩 Murojaatlar jurnali:** Oddiy taklif va xatlarni qabul qilib oluvchi ro'yxat.
*(Barcha jadvallar DataTables texnologiyasi asosida qidirish va saralash imkoniyatlariga ega)*.

---

## 🛠 Texnologik Stack
- **Bot:** Python, Aiogram 3.x
- **Backend:** FastAPI, Uvicorn, Gunicorn
- **Ma'lumotlar bazasi:** SQLite (aiosqlite)
- **Frontend:** Jinja2, TailwindCSS, Chart.js, jQuery DataTables
- **Infratuzilma:** Docker, Docker Compose, Nginx Reverse Proxy

---

## 🚀 Loyihani Ishga Tushirish va O'rnatish

Tizim to'liq izolyatsiya qilingan mikroservislar (Bot, Web, Nginx) ko'rinishida ishlaydi. Uni ishga tushirish uchun serveringizda **Docker** va **Docker Compose** o'rnatilgan bo'lishi kerak.

### 1. Docker va Docker Compose o'rnatish (Ubuntu / Debian uchun)

Agar serveringizda Docker o'rnatilmagan bo'lsa, quyidagi buyruqlar orqali o'rnating:

**A. Dockerni o'rnatish:**
```bash
# Eski versiyalarni o'chirish (agar mavjud bo'lsa)
sudo apt-get remove docker docker-engine docker.io containerd runc

# Paketlarni yangilash
sudo apt-get update

# Kerakli paketlarni o'rnatish
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Dockerning rasmiy GPG kalitini qo'shish
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Docker repozitoriysini qo'shish
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker dvigatelini o'rnatish
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

**B. Docker Compose'ni o'rnatish (agar alohida kerak bo'lsa):**
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

*(Docker to'g'ri o'rnatilganini tekshirish uchun `docker --version` va `docker compose version` komandalarini ishlating).*

### 2. Loyihani yuklab olish va sozlash

**A. Loyihani serverga yuklash:**
```bash
git clone <repository_url>
cd tadbircore365_bot
```

**B. .env faylini yaratish:**
Loyiha papkasida `.env` faylini yarating va quyidagi ma'lumotlarni o'zingizga moslab to'ldiring:
```env
BOT_TOKEN=Sizning_Telegram_Bot_Tokeningiz
ADMIN_CHAT_ID=-100XXXXXXXXXX
DASHBOARD_USER=admin
DASHBOARD_PASS=admin123
```

### 3. Loyihani ishga tushirish

Barcha xizmatlarni fon rejimida (background) qurish va ishga tushirish uchun quyidagi komandani tering:
```bash
docker compose up -d --build
```

**Muvaffaqiyatli ishga tushgach:**
- Telegram botingiz avtomatik ishga tushadi.
- Web Dashboard serveringizning `80-portida` (yoki Localhost'da) ishlay boshlaydi.
- Brauzer orqali `http://<server-ip>/` ga kirib, `.env` faylda ko'rsatilgan admin paroli orqali tizimga kirishingiz mumkin.

### 4. Qo'shimcha Buyruqlar
- **Loglarni ko'rish:** `docker compose logs -f`
- **Tizimni to'xtatish:** `docker compose down`
- **Web servisni qayta qurish:** `docker compose up -d --build web`


### 4. DNS
- jaxson.ns.cloudflare.com
- lara.ns.cloudflare.com