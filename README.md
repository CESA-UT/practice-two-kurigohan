## اسکرین‌شات‌ها

| منوی شروع                                         | داخل بازی                                     |
| ------------------------------------------------- | --------------------------------------------- |
| ![start menu](docs/screenshots/01_start_menu.png) | ![gameplay](docs/screenshots/02_gameplay.png) |

| برد                                        | حالت pause                                   |
| ------------------------------------------ | -------------------------------------------- |
| ![win](docs/screenshots/03_win_screen.png) | ![pause](docs/screenshots/04_pause_menu.png) |

## پیش‌نیازها و نصب

نیازمند Python 3.10+ است.

```bash
pip install -r requirements.txt
```

for windows also install this if you have python 3.14: pip install pygame-ce Pillow

کتابخانه‌های استفاده‌شده:

- `pygame` — رندر گرافیکی، حلقه اصلی بازی، مدیریت ورودی
- `Pillow` — استخراج فریم‌های انیمیشن GIF (pygame به‌تنهایی GIF متحرک را پشتیبانی نمی‌کند)

## اجرا

```bash
python3 main.py
windows python main.py
```

## کنترل‌ها

- کلیک روی کارت گیاه → انتخاب → کلیک روی خانه خالی زمین → کاشت
- کلیک روی Sun (چه از آسمان چه از SunFlower) → جمع‌آوری
- کلیک روی آیکون بیل (Shovel) → انتخاب حالت حذف → کلیک روی گیاه → حذف آن
- `Esc` یا `P` → توقف/ادامه بازی (Pause)
- در صفحه برد/باخت → دکمه «Play Again» برای شروع دوباره

## امکانات پیاده‌سازی‌شده

### بخش‌های الزامی

- زمین ۵×۹ روی `Frontyard.png` با حلقه اصلی بازی (منو → بازی → برد/باخت)
- سیستم Sun کامل: مقدار اولیه ۱۵۰، تولید آسمانی هر ۱۰ ثانیه (۲۵ واحد)، تولید توسط SunFlower
- کارت‌های گیاه با هزینه، cooldown و غیرفعال‌شدن خودکار در نبود Sun کافی
- سه گیاه الزامی: **PeaShooter** (شلیک/آسیب/برد طبق مشخصات)، **SunFlower** (تولید Sun)، **WallNut** (HP بالا + انیمیشن آسیب‌دیده در HP کم)
- **NormalZombie**: حرکت راست‌به‌چپ، توقف و خوردن گیاه روبه‌رو، آسیب طبق مشخصات
- برخورد گلوله-زامبی و کم‌شدن HP و حذف موجودیت‌ها
- دقیقاً جدول «حداقل موج قابل قبول»: موج‌های ۲۰/۵۰/۹۰ ثانیه با ۳/۵/۷ زامبی (مجموع ۱۵)
- شرط برد (همه موج‌ها تمام + همه زامبی‌ها نابود) و باخت (زامبی به خانه برسد)
- طراحی شیءگرا مطابق کلاس‌های پیشنهادی تمرین (پایین صفحه توضیح داده شده)

### امکانات اختیاری اضافه‌شده (امتیاز بونس)

- **LawnMower** برای هر ردیف (طبق `docs/characters/LawnMower.md`)
- **Shovel** برای حذف گیاه کاشته‌شده
- منوی شروع بازی و صفحه Pause
- صفحه برد/باخت با دکمه شروع دوباره
- افکت‌های صوتی (کاشت، برخورد گلوله، خوردن، غرش زامبی، اعلام موج، لان‌موور) — در صورت نبودن دستگاه صوتی روی سیستم اجرا‌کننده، بازی بدون خطا و بی‌صدا اجرا می‌شود

امکانات اختیاری پیاده‌سازی‌نشده (SnowPea، Repeater، CherryBomb، ConeheadZombie و…) در
`docs/characters` مستند هستند و با همان الگوی `PLANT_CLASSES` / `ZOMBIE_CLASSES` قابل اضافه‌شدنند.

## ساختار پروژه و کلاس‌ها

```
main.py                  # نقطه ورود
src/
  constants.py            # همه مقادیر عددی (HP، cooldown، آسیب، جدول موج‌ها...) از docs/characters
  assets.py                # بارگذاری تصاویر و استخراج فریم‌های GIF (AnimatedSprite)
  game.py                  # کلاس Game: حلقه اصلی، رویدادها، برد/باخت
  game_state.py            # Enum حالت‌های بازی (MENU/PLAYING/PAUSED/WIN/LOSE)
  board.py                 # کلاس‌های Board و Cell + تبدیل مختصات پیکسل↔خانه
  wave_manager.py           # کلاس WaveManager: زمان‌بندی و spawn موج‌ها
  entities/
    entity.py               # کلاس پایه انتزاعی Entity (hp, alive, update, draw)
    plant.py                 # Plant + PeaShooter, SunFlower, WallNut
    zombie.py                # Zombie + NormalZombie
    projectile.py             # Pea
    sun_drop.py               # SunDrop (Sun آسمانی و Sun گیاهی)
    lawn_mower.py              # LawnMower
  ui/
    card.py                  # Card و CardBar (کارت‌های گیاه)
    hud.py                    # HUD: شمارنده Sun، بیل، دکمه Pause
    menu.py                   # StartMenu, PauseMenu, EndScreen
```
