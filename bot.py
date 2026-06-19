import asyncio
import logging
import os
import json
import random
import string
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)

TOKEN = "8481542334:AAGEeDuWzac0akTODnra_EEXb5oilnXmnJw"

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ===== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =====
WORKER_IDS = [8984858752]
SUPPORT_IDS = [8984858752]

# ФОТО ДЛЯ РАЗНЫХ МЕСТ (ЗАПОЛНЯЮТСЯ АВТОМАТИЧЕСКИ)
PHOTO_MAIN = None
PHOTO_PROFILE = None
PHOTO_SEARCH = None

PROFILES = {}
USER_LANGUAGE = {}
USER_NAMES = {}
USER_REGISTERED = {}
ORDERS = {}

# ===== ПЕРЕВОДЫ =====
TEXTS = {
    'ru': {
        'main_menu': '🌐 Главное меню',
        'vip_models': '⭐ VIP Модели',
        'profile': '👤 Мой профиль',
        'search': '🔎 Найти девушку',
        'submit': '📩 Подать анкету',
        'worker_panel': '⚙️ Панель воркера',
        'settings': '⚙️ Настройки',
        'language': '🌍 Язык',
        'back': '🔙 Назад',
        'back_to_main': '🔙 Главное меню',
        'change_language': '🌍 Выберите язык',
        'language_changed': '✅ Язык изменен на русский!',
        'language_changed_uk': '✅ Мову змінено на українську!',
        'profile_my_title': '👤 Мой профиль',
        'profile_my_id': '🆔 ID:',
        'profile_my_name': '📛 Имя:',
        'profile_my_username': '🔗 Username:',
        'profile_my_registered': '📅 Зарегистрирован:',
        'profile_my_language': '🌍 Язык:',
        'profile_my_role': '👔 Роль:',
        'profile_my_role_user': '👤 Пользователь',
        'profile_my_role_worker': '👷 Воркер',
        'profile_my_stats': '📊 Статистика',
        'profile_my_profiles_count': '📋 Создано анкет:',
        'profile_my_views': '👁️ Просмотров:',
        'profile_my_rating': '⭐ Рейтинг:',
        'profile_my_edit_name': '✏️ Изменить имя',
        'profile_my_edit_name_step': '✏️ Введите новое имя\n\nИмя будет отображаться в вашем профиле.',
        'profile_my_name_changed': '✅ Имя успешно изменено на:',
        'profile_my_edit_cancel': '❌ Отмена',
        'profile_my_back': '🔙 Назад в профиль',
        'order_button': '📅 Оформить встречу',
        'order_title': '📅 Оформление встречи',
        'order_select_date': '📆 Выберите дату\n\nВведите дату в формате:\nДД.ММ.ГГГГ\n\nНапример: 25.12.2025',
        'order_select_time': '⏰ Выберите время\n\nВведите время в формате:\nЧЧ:ММ\n\nНапример: 18:30',
        'order_confirm_title': '✅ Подтверждение встречи',
        'order_confirm_button': '✅ Подтвердить',
        'order_cancel_button': '❌ Отменить',
        'order_sent_to_support': '❌ Уважаемый клиент, наша система не смогла автоматически подобрать индивидуальные реквизиты для оплаты данной суммы.\n\nПожалуйста, обратитесь в поддержку для предоставления актуальных реквизитов.\n\n👨‍💻 Тех. поддержка: @MistSupports',
        'order_support_message': '🆕 Новая заявка на встречу!\n\n👤 Пользователь: {user_name} (ID: {user_id})\n🌸 Девушка: {girl_name}\n📅 Дата: {date}\n⏰ Время: {time}\n🔑 Код анкеты: {profile_code}',
        'order_canceled': '❌ Оформление заказа отменено.',
        'order_invalid_date': '❌ Неверный формат! Введите дату в формате:\nДД.ММ.ГГГГ\n\nНапример: 25.12.2025',
        'order_invalid_time': '❌ Неверный формат! Введите время в формате:\nЧЧ:ММ\n\nНапример: 18:30',
        'profile_create': '➕ Создать анкету',
        'profile_list': '📋 Список анкет',
        'profile_find': '🔍 Найти анкету по коду',
        'worker_panel_title': '👷 Панель управления воркера',
        'worker_panel_desc': 'Добро пожаловать в панель воркера!\nЗдесь вы можете управлять мамонтами и анкетами.',
        'no_profiles': '📋 Список анкет\n\nУ вас пока нет анкет.\nСоздайте первую анкету!',
        'profiles_list_title': '📋 Список анкет\n\n',
        'profile_find_title': '🔍 Поиск анкеты по коду\n\nВведите уникальный код анкеты:',
        'profile_not_found': '❌ Анкета с таким кодом не найдена!\nПроверьте код и попробуйте снова.',
        'profile_code': '🔑 Уникальный код:',
        'profile_created': '🎉 Анкета создана!',
        'profile_photos_step': '📸 Создание анкеты\n\nШаг 1 из 8: Загрузите фото девушки\n\n📌 Отправьте от 1 до 5 фотографий.\nПосле отправки всех фото нажмите кнопку "Готово".',
        'profile_name_step': '📝 Создание анкеты\n\nШаг 2 из 8: Введите ИМЯ девушки\n\nНапример: Алиса, Мария, Анна',
        'profile_age_step': '🎂 Создание анкеты\n\nШаг 3 из 8: Введите ВОЗРАСТ девушки\n\nВведите число (например: 21)',
        'profile_height_step': '📏 Создание анкеты\n\nШаг 4 из 8: Введите РОСТ девушки (см)\n\nНапример: 165, 170, 175',
        'profile_weight_step': '⚖️ Создание анкеты\n\nШаг 5 из 8: Введите ВЕС девушки (кг)\n\nНапример: 55, 60, 65',
        'profile_city_step': '📍 Создание анкеты\n\nШаг 6 из 8: Введите ГОРОД\n\nНапример: Киев, Одесса, Харьков',
        'profile_description_step': '📝 Создание анкеты\n\nШаг 7 из 8: Введите ОПИСАНИЕ\n\nНапишите краткое описание девушки, её услуги, особенности.',
        'profile_price_1h_step': '💰 Создание анкеты\n\nШаг 8 из 8: Введите ЦЕНЫ\n\nСначала введите цену за 1 час (в гривнах):',
        'profile_price_night_step': '🌙 Создание анкеты\n\nТеперь введите цену за ночь (в гривнах):\n\nНапример: 15000, 20000, 30000',
        'profile_preview': '📋 ПРЕДПРОСМОТР АНКЕТЫ',
        'profile_confirm_save': '✅ Сохранить',
        'profile_confirm_cancel': '❌ Отменить',
        'profile_saved': '✅ Анкета успешно создана!',
        'profile_canceled': '❌ Создание анкеты отменено.',
        'profile_photo_limit': '❌ Вы загрузили максимум 5 фото!',
        'profile_photo_count': '✅ Фото {}/5 загружено!\nОтправьте еще или нажмите "Готово".',
        'profile_no_photos': '❌ Загрузите хотя бы одно фото!',
        'profile_name': '👤 Имя:',
        'profile_age': '🎂 Возраст:',
        'profile_height': '📏 Рост:',
        'profile_weight': '⚖️ Вес:',
        'profile_city': '📍 Город:',
        'profile_description': '📝 Описание:',
        'profile_prices': '💰 Цены:',
        'profile_1h': '• 1 час:',
        'profile_night': '• Ночь:',
        'profile_photos': '📸 Фото:',
        'profile_created_at': '📅 Создана:',
        'profile_status_draft': '📝 Черновик',
        'profile_status_published': '✅ Опубликована',
        'profile_status_archived': '📦 Архив',
        'settings_title': '⚙️ Настройки',
        'settings_photo_status': '🖼 Фото в главном меню:',
        'settings_photo_installed': '✅ Установлено',
        'settings_photo_not_installed': '❌ Не установлено',
        'settings_change_photo': '🖼 Загрузить фото',
        'settings_remove_photo': '🗑 Удалить фото',
        'settings_photo_upload': '🖼 Загрузка фото\n\n📤 Отправьте фото для главного меню.\nФото будет отображаться у всех пользователей.',
        'settings_photo_success': '✅ Фото успешно установлено!\n\nТеперь оно будет отображаться в главном меню у всех пользователей.',
        'settings_photo_removed': '✅ Фото удалено!\n\nГлавное меню теперь будет без фото.',
        'settings_not_photo': '❌ Это не фото! Отправьте изображение.',
        'settings_photo_error': '❌ Отправьте фото!',
        'settings_access_denied': '⛔ Доступ запрещен!',
        'settings_access_denied_worker': '⛔ Доступ запрещен! Вы не являетесь воркером.',
        'settings_invalid_age': '❌ Возраст должен быть от 18 до 60 лет!',
        'settings_invalid_height': '❌ Рост должен быть от 140 до 200 см!',
        'settings_invalid_weight': '❌ Вес должен быть от 40 до 120 кг!',
        'settings_invalid_price': '❌ Цена должна быть от 1000 до 100000 грн!',
        'settings_invalid_price_night': '❌ Цена должна быть от 5000 до 200000 грн!',
        'settings_invalid_number': '❌ Введите число!',
        'settings_invalid_text': '❌ Введите текст!',
        'profiles_total': 'Всего анкет:',
        'profile_delete': '🗑 Удалить анкету',
        'profile_publish': '📤 Опубликовать',
        'profile_deleted': '✅ Анкета удалена!',
        'profile_published': '✅ Анкета опубликована!',
        'search_mammoth': '🔍 Поиск мамонта (заглушка)',
        'bind_mammoth': '🔗 Привязка мамонта (заглушка)',
        'my_mammoths': '👥 Мои мамонты (заглушка)',
        'mailing': '📨 Рассылка (заглушка)',
        'notifications': '🔔 Настройка уведомлений (заглушка)',
        'vip_placeholder': '⭐ VIP модели\n\nДанный раздел будет доступен после первого заказа.\n\nОформите встречу с девушкой и получите доступ к VIP анкетам!',
        'search_placeholder': '🔎 Поиск девушки (заглушка)',
        'submit_placeholder': '🔥 Ищем талантливых девушек для нашего агентства!\n\nЕсли ты хочешь стать частью команды — напиши в техподдержку.\n\n👨‍💻 Тех. поддержка: @MistSupports',
        'choose_language': '🌍 Выберите язык:',
        'language_ru': '🇷🇺 Русский',
        'language_uk': '🇺🇦 Українська',
        'find_girl_title': '🔎 Поиск девушки по коду\n\nВведите уникальный код анкеты девушки:\n\nНапример: 2580\n\n💡 Код можно получить у модели.',
        'find_girl_placeholder': 'Например: 2580',
        'find_girl_not_found': '❌ Девушка с таким кодом не найдена!\nПроверьте код и попробуйте снова.',
        'find_girl_found': '🌸 Анкета девушки',
        'find_girl_contact': '📩 Для связи с девушкой, пожалуйста, обратитесь к администратору.',
        'find_girl_code_label': '🔑 Код анкеты:',
        'search_by_code': '🔍 Поиск по коду',
        'choose_language_start': '🌍 Выберите язык для продолжения\n\nОберіть мову для продовження'
    },
    'uk': {
        'main_menu': '🌐 Головне меню',
        'vip_models': '⭐ VIP Моделі',
        'profile': '👤 Мій профіль',
        'search': '🔎 Знайти дівчину',
        'submit': '📩 Подати анкету',
        'worker_panel': '⚙️ Панель працівника',
        'settings': '⚙️ Налаштування',
        'language': '🌍 Мова',
        'back': '🔙 Назад',
        'back_to_main': '🔙 Головне меню',
        'change_language': '🌍 Виберіть мову',
        'language_changed': '✅ Мову змінено на українську!',
        'language_changed_uk': '✅ Мову змінено на українську!',
        'profile_my_title': '👤 Мій профіль',
        'profile_my_id': '🆔 ID:',
        'profile_my_name': '📛 Ім\'я:',
        'profile_my_username': '🔗 Username:',
        'profile_my_registered': '📅 Зареєстрований:',
        'profile_my_language': '🌍 Мова:',
        'profile_my_role': '👔 Роль:',
        'profile_my_role_user': '👤 Користувач',
        'profile_my_role_worker': '👷 Працівник',
        'profile_my_stats': '📊 Статистика',
        'profile_my_profiles_count': '📋 Створено анкет:',
        'profile_my_views': '👁️ Переглядів:',
        'profile_my_rating': '⭐ Рейтинг:',
        'profile_my_edit_name': '✏️ Змінити ім\'я',
        'profile_my_edit_name_step': '✏️ Введіть нове ім\'я\n\nІм\'я буде відображатися у вашому профілі.',
        'profile_my_name_changed': '✅ Ім\'я успішно змінено на:',
        'profile_my_edit_cancel': '❌ Скасувати',
        'profile_my_back': '🔙 Назад у профіль',
        'order_button': '📅 Оформити зустріч',
        'order_title': '📅 Оформлення зустрічі',
        'order_select_date': '📆 Виберіть дату\n\nВведіть дату у форматі:\nДД.ММ.РРРР\n\nНаприклад: 25.12.2025',
        'order_select_time': '⏰ Виберіть час\n\nВведіть час у форматі:\nГГ:ХХ\n\nНаприклад: 18:30',
        'order_confirm_title': '✅ Підтвердження зустрічі',
        'order_confirm_button': '✅ Підтвердити',
        'order_cancel_button': '❌ Скасувати',
        'order_sent_to_support': '❌ Шановний клієнте, наша система не змогла автоматично підібрати індивідуальні реквізити для оплати даної суми.\n\nБудь ласка, зверніться до підтримки для надання актуальних реквізитів.\n\n👨‍💻 Тех. підтримка: @MistSupports',
        'order_support_message': '🆕 Нова заявка на зустріч!\n\n👤 Користувач: {user_name} (ID: {user_id})\n🌸 Дівчина: {girl_name}\n📅 Дата: {date}\n⏰ Час: {time}\n🔑 Код анкети: {profile_code}',
        'order_canceled': '❌ Оформлення замовлення скасовано.',
        'order_invalid_date': '❌ Невірний формат! Введіть дату у форматі:\nДД.ММ.РРРР\n\nНаприклад: 25.12.2025',
        'order_invalid_time': '❌ Невірний формат! Введіть час у форматі:\nГГ:ХХ\n\nНаприклад: 18:30',
        'profile_create': '➕ Створити анкету',
        'profile_list': '📋 Список анкет',
        'profile_find': '🔍 Знайти анкету за кодом',
        'worker_panel_title': '👷 Панель управління працівника',
        'worker_panel_desc': 'Ласкаво просимо до панелі працівника!\nТут ви можете керувати мамонтами та анкетами.',
        'no_profiles': '📋 Список анкет\n\nУ вас поки немає анкет.\nСтворіть першу анкету!',
        'profiles_list_title': '📋 Список анкет\n\n',
        'profile_find_title': '🔍 Пошук анкети за кодом\n\nВведіть унікальний код анкети:',
        'profile_not_found': '❌ Анкету з таким кодом не знайдено!\nПеревірте код і спробуйте ще раз.',
        'profile_code': '🔑 Унікальний код:',
        'profile_created': '🎉 Анкету створено!',
        'profile_photos_step': '📸 Створення анкети\n\nКрок 1 з 8: Завантажте фото дівчини\n\n📌 Надішліть від 1 до 5 фотографій.\nПісля надсилання всіх фото натисніть кнопку "Готово".',
        'profile_name_step': '📝 Створення анкети\n\nКрок 2 з 8: Введіть ІМ\'Я дівчини\n\nНаприклад: Аліса, Марія, Анна',
        'profile_age_step': '🎂 Створення анкети\n\nКрок 3 з 8: Введіть ВІК дівчини\n\nВведіть число (наприклад: 21)',
        'profile_height_step': '📏 Створення анкети\n\nКрок 4 з 8: Введіть ЗРІСТ дівчини (см)\n\nНаприклад: 165, 170, 175',
        'profile_weight_step': '⚖️ Створення анкети\n\nКрок 5 з 8: Введіть ВАГУ дівчини (кг)\n\nНаприклад: 55, 60, 65',
        'profile_city_step': '📍 Створення анкети\n\nКрок 6 з 8: Введіть МІСТО\n\nНаприклад: Київ, Одеса, Харків',
        'profile_description_step': '📝 Створення анкети\n\nКрок 7 з 8: Введіть ОПИС\n\nНапишіть короткий опис дівчини, її послуги, особливості.',
        'profile_price_1h_step': '💰 Створення анкети\n\nКрок 8 з 8: Введіть ЦІНИ\n\nСпочатку введіть ціну за 1 годину (в гривнях):',
        'profile_price_night_step': '🌙 Створення анкети\n\nТепер введіть ціну за ніч (в гривнях):\n\nНаприклад: 15000, 20000, 30000',
        'profile_preview': '📋 ПОПЕРЕДНІЙ ПЕРЕГЛЯД АНКЕТИ',
        'profile_confirm_save': '✅ Зберегти',
        'profile_confirm_cancel': '❌ Скасувати',
        'profile_saved': '✅ Анкету успішно створено!',
        'profile_canceled': '❌ Створення анкети скасовано.',
        'profile_photo_limit': '❌ Ви завантажили максимум 5 фото!',
        'profile_photo_count': '✅ Фото {}/5 завантажено!\nНадішліть ще або натисніть "Готово".',
        'profile_no_photos': '❌ Завантажте хоча б одне фото!',
        'profile_name': '👤 Ім\'я:',
        'profile_age': '🎂 Вік:',
        'profile_height': '📏 Зріст:',
        'profile_weight': '⚖️ Вага:',
        'profile_city': '📍 Місто:',
        'profile_description': '📝 Опис:',
        'profile_prices': '💰 Ціни:',
        'profile_1h': '• 1 година:',
        'profile_night': '• Ніч:',
        'profile_photos': '📸 Фото:',
        'profile_created_at': '📅 Створено:',
        'profile_status_draft': '📝 Чернетка',
        'profile_status_published': '✅ Опубліковано',
        'profile_status_archived': '📦 Архів',
        'settings_title': '⚙️ Налаштування',
        'settings_photo_status': '🖼 Фото в головному меню:',
        'settings_photo_installed': '✅ Встановлено',
        'settings_photo_not_installed': '❌ Не встановлено',
        'settings_change_photo': '🖼 Завантажити фото',
        'settings_remove_photo': '🗑 Видалити фото',
        'settings_photo_upload': '🖼 Завантаження фото\n\n📤 Надішліть фото для головного меню.\nФото буде відображатися у всіх користувачів.',
        'settings_photo_success': '✅ Фото успішно встановлено!\n\nТепер воно буде відображатися в головному меню у всіх користувачів.',
        'settings_photo_removed': '✅ Фото видалено!\n\nГоловне меню тепер буде без фото.',
        'settings_not_photo': '❌ Це не фото! Надішліть зображення.',
        'settings_photo_error': '❌ Надішліть фото!',
        'settings_access_denied': '⛔ Доступ заборонено!',
        'settings_access_denied_worker': '⛔ Доступ заборонено! Ви не є працівником.',
        'settings_invalid_age': '❌ Вік повинен бути від 18 до 60 років!',
        'settings_invalid_height': '❌ Зріст повинен бути від 140 до 200 см!',
        'settings_invalid_weight': '❌ Вага повинна бути від 40 до 120 кг!',
        'settings_invalid_price': '❌ Ціна повинна бути від 1000 до 100000 грн!',
        'settings_invalid_price_night': '❌ Ціна повинна бути від 5000 до 200000 грн!',
        'settings_invalid_number': '❌ Введіть число!',
        'settings_invalid_text': '❌ Введіть текст!',
        'profiles_total': 'Всього анкет:',
        'profile_delete': '🗑 Видалити анкету',
        'profile_publish': '📤 Опублікувати',
        'profile_deleted': '✅ Анкету видалено!',
        'profile_published': '✅ Анкету опубліковано!',
        'search_mammoth': '🔍 Пошук мамонта (заглушка)',
        'bind_mammoth': '🔗 Прив\'язка мамонта (заглушка)',
        'my_mammoths': '👥 Мої мамонти (заглушка)',
        'mailing': '📨 Розсилка (заглушка)',
        'notifications': '🔔 Налаштування сповіщень (заглушка)',
        'vip_placeholder': '⭐ VIP моделі\n\nДаний розділ буде доступний після першого замовлення.\n\nОформіть зустріч з дівчиною та отримайте доступ до VIP анкет!',
        'search_placeholder': '🔎 Пошук дівчини (заглушка)',
        'submit_placeholder': '🔥 Шукаємо талановитих дівчат для нашого агентства!\n\nЯкщо ти хочеш стати частиною команди — напиши в техпідтримку.\n\n👨‍💻 Тех. підтримка: @MistSupports',
        'choose_language': '🌍 Виберіть мову:',
        'language_ru': '🇷🇺 Російська',
        'language_uk': '🇺🇦 Українська',
        'find_girl_title': '🔎 Пошук дівчини за кодом\n\nВведіть унікальний код анкети дівчини:\n\nНаприклад: 2580\n\n💡 Код можна отримати у моделі.',
        'find_girl_placeholder': 'Наприклад: 2580',
        'find_girl_not_found': '❌ Дівчину з таким кодом не знайдено!\nПеревірте код і спробуйте ще раз.',
        'find_girl_found': '🌸 Анкета дівчини',
        'find_girl_contact': '📩 Для зв\'язку з дівчиною, будь ласка, зверніться до адміністратора.',
        'find_girl_code_label': '🔑 Код анкети:',
        'search_by_code': '🔍 Пошук за кодом',
        'choose_language_start': '🌍 Виберіть мову для продовження\n\nОберіть мову для продовження'
    }
}

# ===== СОСТОЯНИЯ =====
class SettingsStates(StatesGroup):
    waiting_for_photo = State()

class WorkerStates(StatesGroup):
    waiting_for_mammoth_id = State()

class CreateProfileStates(StatesGroup):
    waiting_for_photos = State()
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_city = State()
    waiting_for_description = State()
    waiting_for_price_1h = State()
    waiting_for_price_night = State()
    waiting_for_confirm = State()

class UserSearchStates(StatesGroup):
    waiting_for_girl_code = State()

class EditProfileStates(StatesGroup):
    waiting_for_name = State()

class OrderStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_confirm = State()

class PhotoStates(StatesGroup):
    waiting_for_main = State()
    waiting_for_profile = State()
    waiting_for_search = State()

# ===== ФУНКЦИИ =====
def get_text(user_id: int, key: str) -> str:
    lang = USER_LANGUAGE.get(user_id, 'ru')
    return TEXTS.get(lang, TEXTS['ru']).get(key, key)

def get_lang(user_id: int) -> str:
    return USER_LANGUAGE.get(user_id, 'ru')

def generate_profile_code():
    return str(random.randint(1000, 9999))

def generate_order_id():
    return f"ORD_{datetime.now().strftime('%Y%m%d')}_{random.randint(1000, 9999)}"

def save_profile(profile_data):
    profile_id = generate_profile_code()
    profile_data['id'] = profile_id
    profile_data['created_at'] = datetime.now().isoformat()
    profile_data['status'] = 'draft'
    PROFILES[profile_id] = profile_data
    return profile_id

def get_photo(photo_type='main'):
    if photo_type == 'main' and PHOTO_MAIN:
        return PHOTO_MAIN
    elif photo_type == 'profile' and PHOTO_PROFILE:
        return PHOTO_PROFILE
    elif photo_type == 'search' and PHOTO_SEARCH:
        return PHOTO_SEARCH
    return None

def is_worker(user_id: int) -> bool:
    return user_id in WORKER_IDS

def is_support(user_id: int) -> bool:
    return user_id in SUPPORT_IDS

def get_user_name(user_id: int) -> str:
    return USER_NAMES.get(user_id, "Пользователь")

def get_user_registered(user_id: int) -> str:
    return USER_REGISTERED.get(user_id, datetime.now().strftime("%d.%m.%Y"))

def get_user_profiles_count(user_id: int) -> int:
    count = 0
    for profile in PROFILES.values():
        if profile.get('created_by') == user_id:
            count += 1
    return count

# ===== КЛАВИАТУРЫ =====
def main_menu(user_id: int):
    text = get_text
    buttons = [
        [InlineKeyboardButton(text=text(user_id, 'vip_models'), callback_data="vip_models")],
        [InlineKeyboardButton(text=text(user_id, 'profile'), callback_data="show_profile"),
         InlineKeyboardButton(text=text(user_id, 'search'), callback_data="user_search_girl")],
        [InlineKeyboardButton(text=text(user_id, 'submit'), callback_data="submit")]
    ]
    buttons.append([InlineKeyboardButton(text=text(user_id, 'settings'), callback_data="user_settings")])
    if user_id in WORKER_IDS:
        buttons.append([InlineKeyboardButton(text=text(user_id, 'worker_panel'), callback_data="worker_panel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def language_start_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_start_ru")],
        [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_start_uk")]
    ])

def profile_menu(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'profile_my_edit_name'), callback_data="profile_edit_name")],
        [InlineKeyboardButton(text=text(user_id, 'back_to_main'), callback_data="back_to_main")]
    ])

def profile_edit_cancel(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'profile_my_edit_cancel'), callback_data="profile_edit_cancel")]
    ])

def worker_panel_menu(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Поиск мамонта", callback_data="worker_search_mammoth")],
        [InlineKeyboardButton(text="🔗 Привязать по ID", callback_data="worker_bind_mammoth")],
        [InlineKeyboardButton(text="👥 Мои мамонты", callback_data="worker_my_mammoths")],
        [InlineKeyboardButton(text="📋 Мои анкеты", callback_data="worker_my_profiles")],
        [InlineKeyboardButton(text="📨 Рассылка", callback_data="worker_mailing")],
        [InlineKeyboardButton(text="🔔 Настройка уведомлений", callback_data="worker_notifications")],
        [InlineKeyboardButton(text="🖼 Настройки фото", callback_data="worker_photos_settings")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="worker_settings")],
        [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")]
    ])

def photos_settings_menu(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖼 Главное меню", callback_data="photo_set_main")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="photo_set_profile")],
        [InlineKeyboardButton(text="🔎 Поиск девушки", callback_data="photo_set_search")],
        [InlineKeyboardButton(text="🗑 Удалить все", callback_data="photo_remove_all")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="worker_panel")]
    ])

def profiles_menu(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'profile_create'), callback_data="profile_create")],
        [InlineKeyboardButton(text=text(user_id, 'profile_list'), callback_data="profile_list")],
        [InlineKeyboardButton(text=text(user_id, 'profile_find'), callback_data="profile_find")],
        [InlineKeyboardButton(text=text(user_id, 'back'), callback_data="worker_panel")]
    ])

def user_settings_menu(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'language'), callback_data="change_language")],
        [InlineKeyboardButton(text=text(user_id, 'back_to_main'), callback_data="back_to_main")]
    ])

def language_menu(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_uk")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="user_settings")]
    ])

def confirm_keyboard(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'profile_confirm_save'), callback_data="profile_confirm_save"),
         InlineKeyboardButton(text=text(user_id, 'profile_confirm_cancel'), callback_data="profile_confirm_cancel")]
    ])

def back_to_profiles(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'back'), callback_data="worker_my_profiles")]
    ])

def back_to_worker_panel_inline(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'back'), callback_data="back_to_worker_panel")]
    ])

def settings_menu(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'settings_change_photo'), callback_data="settings_change_photo")],
        [InlineKeyboardButton(text=text(user_id, 'settings_remove_photo'), callback_data="settings_remove_photo")],
        [InlineKeyboardButton(text=text(user_id, 'back'), callback_data="worker_panel")]
    ])

def back_to_main_menu(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'back_to_main'), callback_data="back_to_main")]
    ])

def back_to_profile_inline(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'profile_my_back'), callback_data="show_profile")]
    ])

def order_cancel_keyboard(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'order_cancel_button'), callback_data="order_cancel")]
    ])

def order_confirm_keyboard(user_id: int):
    text = get_text
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text(user_id, 'order_confirm_button'), callback_data="order_confirm")],
        [InlineKeyboardButton(text=text(user_id, 'order_cancel_button'), callback_data="order_cancel")]
    ])

# ===== ОБРАБОТЧИКИ =====
@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} запустил бота")
    
    if user_id not in USER_LANGUAGE:
        await message.answer(
            TEXTS['ru']['choose_language_start'],
            reply_markup=language_start_menu()
        )
        return
    
    if user_id not in USER_NAMES:
        USER_NAMES[user_id] = message.from_user.first_name or "Пользователь"
    if user_id not in USER_REGISTERED:
        USER_REGISTERED[user_id] = datetime.now().strftime("%d.%m.%Y")
    
    photo = get_photo('main')
    text = get_text(user_id, 'main_menu')
    
    if photo:
        await message.answer_photo(photo=photo, caption=text, reply_markup=main_menu(user_id))
    else:
        await message.answer(text, reply_markup=main_menu(user_id))

@dp.callback_query(lambda c: c.data.startswith("lang_start_"))
async def set_start_language(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = call.data.split("_")[2]
    
    USER_LANGUAGE[user_id] = lang
    USER_NAMES[user_id] = call.from_user.first_name or "Пользователь"
    USER_REGISTERED[user_id] = datetime.now().strftime("%d.%m.%Y")
    
    text = "✅ Язык установлен! Добро пожаловать!" if lang == 'ru' else "✅ Мову встановлено! Ласкаво просимо!"
    
    photo = get_photo('main')
    menu_text = get_text(user_id, 'main_menu')
    
    await call.message.delete()
    if photo:
        await call.message.answer_photo(photo=photo, caption=f"{text}\n\n{menu_text}", reply_markup=main_menu(user_id))
    else:
        await call.message.answer(f"{text}\n\n{menu_text}", reply_markup=main_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "show_profile")
async def show_profile(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = call.from_user
    
    photo = get_photo('profile')
    profile_text = f"""
{get_text(user_id, 'profile_my_title')}

{get_text(user_id, 'profile_my_id')} {user_id}
{get_text(user_id, 'profile_my_name')} {get_user_name(user_id)}
{get_text(user_id, 'profile_my_username')} @{user.username or 'Не указан'}
{get_text(user_id, 'profile_my_registered')} {get_user_registered(user_id)}
{get_text(user_id, 'profile_my_language')} {'Русский' if get_lang(user_id) == 'ru' else 'Українська'}
{get_text(user_id, 'profile_my_role')} {get_text(user_id, 'profile_my_role_worker') if is_worker(user_id) else get_text(user_id, 'profile_my_role_user')}

{get_text(user_id, 'profile_my_stats')}
{get_text(user_id, 'profile_my_profiles_count')} {get_user_profiles_count(user_id)}
{get_text(user_id, 'profile_my_views')} 0
{get_text(user_id, 'profile_my_rating')} ⭐⭐⭐⭐⭐
    """
    
    await call.message.delete()
    if photo:
        await call.message.answer_photo(photo=photo, caption=profile_text, reply_markup=profile_menu(user_id))
    else:
        await call.message.answer(profile_text, reply_markup=profile_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "profile_edit_name")
async def profile_edit_name(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'profile_my_edit_name_step'), reply_markup=profile_edit_cancel(user_id))
    await state.set_state(EditProfileStates.waiting_for_name)
    await call.answer()

@dp.message(EditProfileStates.waiting_for_name)
async def profile_save_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not message.text:
        await message.answer(get_text(user_id, 'settings_invalid_text'))
        return
    USER_NAMES[user_id] = message.text.strip()
    await message.answer(
        f"{get_text(user_id, 'profile_my_name_changed')} {message.text.strip()}",
        reply_markup=back_to_profile_inline(user_id)
    )
    await state.clear()

@dp.callback_query(lambda c: c.data == "profile_edit_cancel")
async def profile_edit_cancel(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await state.clear()
    await call.message.delete()
    await show_profile(call)

@dp.callback_query(lambda c: c.data == "user_search_girl")
async def user_search_girl(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await call.message.delete()
    await call.message.answer(
        get_text(user_id, 'find_girl_title'),
        reply_markup=back_to_main_menu(user_id)
    )
    await state.set_state(UserSearchStates.waiting_for_girl_code)
    await call.answer()

@dp.message(UserSearchStates.waiting_for_girl_code)
async def process_girl_search(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    code = message.text.strip()
    
    if code not in PROFILES:
        await message.answer(get_text(user_id, 'find_girl_not_found'), reply_markup=back_to_main_menu(user_id))
        await state.clear()
        return
    
    data = PROFILES[code]
    await state.update_data(profile_code=code)
    
    caption = f"""
{get_text(user_id, 'find_girl_found')}

{get_text(user_id, 'profile_name')} {data.get('name', 'Не указано')}
{get_text(user_id, 'profile_age')} {data.get('age', '?')} лет
{get_text(user_id, 'profile_height')} {data.get('height', '?')} см
{get_text(user_id, 'profile_weight')} {data.get('weight', '?')} кг
{get_text(user_id, 'profile_city')} {data.get('city', 'Не указан')}

{get_text(user_id, 'profile_description')}
{data.get('description', 'Нет описания')}

{get_text(user_id, 'profile_prices')}
{get_text(user_id, 'profile_1h')} {data.get('price_1h', '?')} грн
{get_text(user_id, 'profile_night')} {data.get('price_night', '?')} грн

{get_text(user_id, 'find_girl_code_label')} {code}

{get_text(user_id, 'find_girl_contact')}
    """
    
    photo = get_photo('search')
    order_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(user_id, 'order_button'), callback_data=f"order_start_{code}")],
        [InlineKeyboardButton(text=get_text(user_id, 'back_to_main'), callback_data="back_to_main")]
    ])
    
    if data.get('photos'):
        if photo:
            await message.answer_photo(photo=photo, caption=caption, reply_markup=order_keyboard)
        else:
            await message.answer_photo(photo=data['photos'][0], caption=caption, reply_markup=order_keyboard)
        for photo_id in data['photos'][1:]:
            await message.answer_photo(photo=photo_id)
    else:
        if photo:
            await message.answer_photo(photo=photo, caption=caption, reply_markup=order_keyboard)
        else:
            await message.answer(caption, reply_markup=order_keyboard)
    
    await state.clear()

@dp.callback_query(lambda c: c.data.startswith("order_start_"))
async def order_start(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    profile_code = call.data.split("_")[2]
    await state.update_data(profile_code=profile_code)
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'order_select_date'), reply_markup=order_cancel_keyboard(user_id))
    await state.set_state(OrderStates.waiting_for_date)
    await call.answer()

@dp.message(OrderStates.waiting_for_date)
async def order_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    date = message.text.strip()
    if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
        await message.answer(get_text(user_id, 'order_invalid_date'), reply_markup=order_cancel_keyboard(user_id))
        return
    await state.update_data(date=date)
    await message.answer(get_text(user_id, 'order_select_time'), reply_markup=order_cancel_keyboard(user_id))
    await state.set_state(OrderStates.waiting_for_time)

@dp.message(OrderStates.waiting_for_time)
async def order_time(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    time = message.text.strip()
    if not re.match(r'^\d{2}:\d{2}$', time):
        await message.answer(get_text(user_id, 'order_invalid_time'), reply_markup=order_cancel_keyboard(user_id))
        return
    await state.update_data(time=time)
    data = await state.get_data()
    
    profile_code = data.get('profile_code')
    profile_data = PROFILES.get(profile_code, {})
    girl_name = profile_data.get('name', 'Не указано')
    date = data.get('date')
    time = data.get('time')
    
    confirm_text = f"""
{get_text(user_id, 'order_confirm_title')}

{get_text(user_id, 'profile_name')} {girl_name}
📅 Дата: {date}
⏰ Время: {time}

✅ Всё верно? Нажмите "Подтвердить"
    """
    await message.answer(confirm_text, reply_markup=order_confirm_keyboard(user_id))
    await state.set_state(OrderStates.waiting_for_confirm)

@dp.callback_query(lambda c: c.data == "order_confirm")
async def order_confirm(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    data = await state.get_data()
    
    profile_code = data.get('profile_code')
    profile_data = PROFILES.get(profile_code, {})
    girl_name = profile_data.get('name', 'Не указано')
    date = data.get('date')
    time = data.get('time')
    
    support_text = f"""
{get_text(user_id, 'order_support_message').format(
    user_name=get_user_name(user_id),
    user_id=user_id,
    girl_name=girl_name,
    date=date,
    time=time,
    profile_code=profile_code
)}
    """
    
    for support_id in SUPPORT_IDS:
        try:
            await bot.send_message(support_id, support_text)
        except:
            pass
    
    order_id = generate_order_id()
    ORDERS[order_id] = {
        'user_id': user_id,
        'profile_code': profile_code,
        'girl_name': girl_name,
        'date': date,
        'time': time,
        'created_at': datetime.now().isoformat()
    }
    
    await call.message.delete()
    await call.message.answer(
        get_text(user_id, 'order_sent_to_support'),
        reply_markup=None
    )
    
    await state.clear()
    await call.answer()

@dp.callback_query(lambda c: c.data == "order_cancel")
async def order_cancel(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await state.clear()
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'order_canceled'), reply_markup=back_to_main_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "user_settings")
async def user_settings(call: types.CallbackQuery):
    user_id = call.from_user.id
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'settings_title'), reply_markup=user_settings_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "change_language")
async def change_language(call: types.CallbackQuery):
    user_id = call.from_user.id
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'choose_language'), reply_markup=language_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("lang_") and not c.data.startswith("lang_start_"))
async def set_language(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = call.data.split("_")[1]
    USER_LANGUAGE[user_id] = lang
    text = get_text(user_id, 'language_changed') if lang == 'ru' else get_text(user_id, 'language_changed_uk')
    await call.message.delete()
    await call.message.answer(text, reply_markup=user_settings_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "worker_panel")
async def worker_panel(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied_worker'), show_alert=True)
        return
    text = f"""{get_text(user_id, 'worker_panel_title')}

{get_text(user_id, 'worker_panel_desc')}

📊 Ваша реферальная ссылка:
https://t.me/Aura_Agency_bot?start={user_id}"""
    await call.message.delete()
    await call.message.answer(text, reply_markup=worker_panel_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "back_to_worker_panel")
async def back_to_worker_panel(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    text = f"""{get_text(user_id, 'worker_panel_title')}

{get_text(user_id, 'worker_panel_desc')}

📊 Ваша реферальная ссылка:
https://t.me/Aura_Agency_bot?start={user_id}"""
    await call.message.delete()
    await call.message.answer(text, reply_markup=worker_panel_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(call: types.CallbackQuery):
    user_id = call.from_user.id
    await call.message.delete()
    photo = get_photo('main')
    text = get_text(user_id, 'main_menu')
    if photo:
        await call.message.answer_photo(photo=photo, caption=text, reply_markup=main_menu(user_id))
    else:
        await call.message.answer(text, reply_markup=main_menu(user_id))
    await call.answer()

# ===== НАСТРОЙКИ ФОТО В ПАНЕЛИ ВОРКЕРА =====
@dp.callback_query(lambda c: c.data == "worker_photos_settings")
async def worker_photos_settings(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    
    status = f"""
🖼 Управление фото:

Главное меню: {'✅' if PHOTO_MAIN else '❌'}
Профиль: {'✅' if PHOTO_PROFILE else '❌'}
Поиск девушки: {'✅' if PHOTO_SEARCH else '❌'}
    """
    await call.message.delete()
    await call.message.answer(status, reply_markup=photos_settings_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "photo_set_main")
async def photo_set_main(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer("📤 Отправьте фото для Главного меню", reply_markup=back_to_worker_panel_inline(user_id))
    await state.set_state(PhotoStates.waiting_for_main)
    await call.answer()

@dp.callback_query(lambda c: c.data == "photo_set_profile")
async def photo_set_profile(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer("📤 Отправьте фото для Профиля", reply_markup=back_to_worker_panel_inline(user_id))
    await state.set_state(PhotoStates.waiting_for_profile)
    await call.answer()

@dp.callback_query(lambda c: c.data == "photo_set_search")
async def photo_set_search(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer("📤 Отправьте фото для Поиска девушки", reply_markup=back_to_worker_panel_inline(user_id))
    await state.set_state(PhotoStates.waiting_for_search)
    await call.answer()

@dp.message(PhotoStates.waiting_for_main)
async def save_photo_main(message: types.Message, state: FSMContext):
    global PHOTO_MAIN
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        await state.clear()
        return
    if not message.photo:
        await message.answer("❌ Отправьте фото!")
        return
    PHOTO_MAIN = message.photo[-1].file_id
    await message.answer("✅ Фото для Главного меню сохранено!", reply_markup=back_to_worker_panel_inline(user_id))
    await state.clear()

@dp.message(PhotoStates.waiting_for_profile)
async def save_photo_profile(message: types.Message, state: FSMContext):
    global PHOTO_PROFILE
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        await state.clear()
        return
    if not message.photo:
        await message.answer("❌ Отправьте фото!")
        return
    PHOTO_PROFILE = message.photo[-1].file_id
    await message.answer("✅ Фото для Профиля сохранено!", reply_markup=back_to_worker_panel_inline(user_id))
    await state.clear()

@dp.message(PhotoStates.waiting_for_search)
async def save_photo_search(message: types.Message, state: FSMContext):
    global PHOTO_SEARCH
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        await state.clear()
        return
    if not message.photo:
        await message.answer("❌ Отправьте фото!")
        return
    PHOTO_SEARCH = message.photo[-1].file_id
    await message.answer("✅ Фото для Поиска девушки сохранено!", reply_markup=back_to_worker_panel_inline(user_id))
    await state.clear()

@dp.callback_query(lambda c: c.data == "photo_remove_all")
async def photo_remove_all(call: types.CallbackQuery):
    global PHOTO_MAIN, PHOTO_PROFILE, PHOTO_SEARCH
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    PHOTO_MAIN = None
    PHOTO_PROFILE = None
    PHOTO_SEARCH = None
    await call.message.delete()
    await call.message.answer("🗑 Все фото удалены!", reply_markup=photos_settings_menu(user_id))
    await call.answer()

# ===== МОИ АНКЕТЫ =====
@dp.callback_query(lambda c: c.data == "worker_my_profiles")
async def worker_my_profiles(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    text = f"""{get_text(user_id, 'profile_list')}

{get_text(user_id, 'profiles_total')} {len(PROFILES)}"""
    await call.message.delete()
    await call.message.answer(text, reply_markup=profiles_menu(user_id))
    await call.answer()

# ===== СОЗДАНИЕ АНКЕТЫ =====
@dp.callback_query(lambda c: c.data == "profile_create")
async def profile_create(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await state.clear()
    await state.update_data(photos=[], created_by=user_id)
    await call.message.delete()
    await call.message.answer(
        get_text(user_id, 'profile_photos_step'),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Готово", callback_data="profile_photos_done")]
        ])
    )
    await state.set_state(CreateProfileStates.waiting_for_photos)
    await call.answer()

@dp.message(CreateProfileStates.waiting_for_photos)
async def profile_photos(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        return
    if not message.photo:
        await message.answer(get_text(user_id, 'settings_not_photo'))
        return
    data = await state.get_data()
    photos = data.get('photos', [])
    if len(photos) >= 5:
        await message.answer(get_text(user_id, 'profile_photo_limit'))
        return
    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)
    await message.answer(get_text(user_id, 'profile_photo_count').format(len(photos)))

@dp.callback_query(lambda c: c.data == "profile_photos_done")
async def profile_photos_done(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    data = await state.get_data()
    if len(data.get('photos', [])) == 0:
        await call.answer(get_text(user_id, 'profile_no_photos'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'profile_name_step'))
    await state.set_state(CreateProfileStates.waiting_for_name)
    await call.answer()

@dp.message(CreateProfileStates.waiting_for_name)
async def profile_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        return
    if not message.text:
        await message.answer(get_text(user_id, 'settings_invalid_text'))
        return
    await state.update_data(name=message.text.strip())
    await message.answer(get_text(user_id, 'profile_age_step'))
    await state.set_state(CreateProfileStates.waiting_for_age)

@dp.message(CreateProfileStates.waiting_for_age)
async def profile_age(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        return
    try:
        age = int(message.text)
        if age < 18 or age > 60:
            await message.answer(get_text(user_id, 'settings_invalid_age'))
            return
        await state.update_data(age=age)
    except ValueError:
        await message.answer(get_text(user_id, 'settings_invalid_number'))
        return
    await message.answer(get_text(user_id, 'profile_height_step'))
    await state.set_state(CreateProfileStates.waiting_for_height)

@dp.message(CreateProfileStates.waiting_for_height)
async def profile_height(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        return
    try:
        height = int(message.text)
        if height < 140 or height > 200:
            await message.answer(get_text(user_id, 'settings_invalid_height'))
            return
        await state.update_data(height=height)
    except ValueError:
        await message.answer(get_text(user_id, 'settings_invalid_number'))
        return
    await message.answer(get_text(user_id, 'profile_weight_step'))
    await state.set_state(CreateProfileStates.waiting_for_weight)

@dp.message(CreateProfileStates.waiting_for_weight)
async def profile_weight(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        return
    try:
        weight = int(message.text)
        if weight < 40 or weight > 120:
            await message.answer(get_text(user_id, 'settings_invalid_weight'))
            return
        await state.update_data(weight=weight)
    except ValueError:
        await message.answer(get_text(user_id, 'settings_invalid_number'))
        return
    await message.answer(get_text(user_id, 'profile_city_step'))
    await state.set_state(CreateProfileStates.waiting_for_city)

@dp.message(CreateProfileStates.waiting_for_city)
async def profile_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        return
    if not message.text:
        await message.answer(get_text(user_id, 'settings_invalid_text'))
        return
    await state.update_data(city=message.text.strip())
    await message.answer(get_text(user_id, 'profile_description_step'))
    await state.set_state(CreateProfileStates.waiting_for_description)

@dp.message(CreateProfileStates.waiting_for_description)
async def profile_description(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        return
    if not message.text:
        await message.answer(get_text(user_id, 'settings_invalid_text'))
        return
    await state.update_data(description=message.text.strip())
    await message.answer(get_text(user_id, 'profile_price_1h_step'))
    await state.set_state(CreateProfileStates.waiting_for_price_1h)

@dp.message(CreateProfileStates.waiting_for_price_1h)
async def profile_price_1h(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        return
    try:
        price = int(message.text)
        if price < 1000 or price > 100000:
            await message.answer(get_text(user_id, 'settings_invalid_price'))
            return
        await state.update_data(price_1h=price)
    except ValueError:
        await message.answer(get_text(user_id, 'settings_invalid_number'))
        return
    await message.answer(get_text(user_id, 'profile_price_night_step'))
    await state.set_state(CreateProfileStates.waiting_for_price_night)

@dp.message(CreateProfileStates.waiting_for_price_night)
async def profile_price_night(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        return
    try:
        price = int(message.text)
        if price < 5000 or price > 200000:
            await message.answer(get_text(user_id, 'settings_invalid_price_night'))
            return
        await state.update_data(price_night=price)
    except ValueError:
        await message.answer(get_text(user_id, 'settings_invalid_number'))
        return
    
    data = await state.get_data()
    await state.set_state(CreateProfileStates.waiting_for_confirm)
    
    preview = f"""
{get_text(user_id, 'profile_preview')}

{get_text(user_id, 'profile_name')} {data['name']}
{get_text(user_id, 'profile_age')} {data['age']} лет
{get_text(user_id, 'profile_height')} {data['height']} см
{get_text(user_id, 'profile_weight')} {data['weight']} кг
{get_text(user_id, 'profile_city')} {data['city']}

{get_text(user_id, 'profile_description')}
{data['description']}

{get_text(user_id, 'profile_prices')}
{get_text(user_id, 'profile_1h')} {data['price_1h']} грн
{get_text(user_id, 'profile_night')} {data['price_night']} грн

{get_text(user_id, 'profile_photos')} {len(data['photos'])} шт.

✅ Всё верно? Сохраните анкету.
    """
    await message.answer(preview, reply_markup=confirm_keyboard(user_id))

@dp.callback_query(lambda c: c.data == "profile_confirm_save")
async def profile_confirm_save(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    data = await state.get_data()
    profile_id = save_profile(data)
    
    if data.get('photos'):
        caption = f"""
{get_text(user_id, 'profile_created')}

📋 ID анкеты: {profile_id}

{get_text(user_id, 'profile_name')} {data['name']}
{get_text(user_id, 'profile_age')} {data['age']} лет
{get_text(user_id, 'profile_height')} {data['height']} см
{get_text(user_id, 'profile_weight')} {data['weight']} кг
{get_text(user_id, 'profile_city')} {data['city']}

{get_text(user_id, 'profile_prices')}
{get_text(user_id, 'profile_1h')} {data['price_1h']} грн
{get_text(user_id, 'profile_night')} {data['price_night']} грн

{get_text(user_id, 'profile_code')} {profile_id}
        """
        await call.message.delete()
        await call.message.answer_photo(photo=data['photos'][0], caption=caption)
    
    await state.clear()
    await call.answer(get_text(user_id, 'profile_saved'))

@dp.callback_query(lambda c: c.data == "profile_confirm_cancel")
async def profile_confirm_cancel(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await state.clear()
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'profile_canceled'), reply_markup=profiles_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "profile_list")
async def profile_list(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    if not PROFILES:
        await call.message.delete()
        await call.message.answer(get_text(user_id, 'no_profiles'), reply_markup=profiles_menu(user_id))
        await call.answer()
        return
    text = get_text(user_id, 'profiles_list_title')
    for profile_id, data in list(PROFILES.items())[:10]:
        status_emoji = "✅" if data.get('status') == 'published' else "📝"
        text += f"{status_emoji} {profile_id} - {data.get('name', 'Без имени')} ({data.get('age', '?')} лет)\n"
    if len(PROFILES) > 10:
        text += f"\n... и ещё {len(PROFILES) - 10} анкет"
    text += f"\n\n{get_text(user_id, 'profile_find')}"
    await call.message.delete()
    await call.message.answer(text, reply_markup=profiles_menu(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "profile_find")
async def profile_find_start(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'profile_find_title'), reply_markup=back_to_profiles(user_id))
    await state.set_state(WorkerStates.waiting_for_mammoth_id)
    await call.answer()

@dp.message(WorkerStates.waiting_for_mammoth_id)
async def profile_find_by_code(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        await state.clear()
        return
    code = message.text.strip()
    if code not in PROFILES:
        await message.answer(get_text(user_id, 'profile_not_found'), reply_markup=back_to_profiles(user_id))
        await state.clear()
        return
    data = PROFILES[code]
    if data.get('photos'):
        await message.answer_photo(
            photo=data['photos'][0],
            caption=f"""
📋 Анкета #{code}

{get_text(user_id, 'profile_name')} {data.get('name', 'Не указано')}
{get_text(user_id, 'profile_age')} {data.get('age', '?')} лет
{get_text(user_id, 'profile_height')} {data.get('height', '?')} см
{get_text(user_id, 'profile_weight')} {data.get('weight', '?')} кг
{get_text(user_id, 'profile_city')} {data.get('city', 'Не указан')}

{get_text(user_id, 'profile_description')}
{data.get('description', 'Нет описания')}

{get_text(user_id, 'profile_prices')}
{get_text(user_id, 'profile_1h')} {data.get('price_1h', '?')} грн
{get_text(user_id, 'profile_night')} {data.get('price_night', '?')} грн

{get_text(user_id, 'profile_created_at')} {data.get('created_at', 'Неизвестно')}
            """
        )
    await message.answer("🔙 Для возврата используйте кнопку ниже", reply_markup=back_to_profiles(user_id))
    await state.clear()

# ===== ЗАГЛУШКИ =====
@dp.callback_query(lambda c: c.data == "worker_search_mammoth")
async def worker_search_mammoth(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'search_mammoth'), reply_markup=back_to_worker_panel_inline(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "worker_bind_mammoth")
async def worker_bind_mammoth(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'bind_mammoth'), reply_markup=back_to_worker_panel_inline(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "worker_my_mammoths")
async def worker_my_mammoths(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'my_mammoths'), reply_markup=back_to_worker_panel_inline(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "worker_mailing")
async def worker_mailing(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'mailing'), reply_markup=back_to_worker_panel_inline(user_id))
    await call.answer()

@dp.callback_query(lambda c: c.data == "worker_notifications")
async def worker_notifications(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'notifications'), reply_markup=back_to_worker_panel_inline(user_id))
    await call.answer()

# ===== НАСТРОЙКИ ВОРКЕРА =====
@dp.callback_query(lambda c: c.data == "worker_settings")
async def worker_settings(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    photo_status = get_text(user_id, 'settings_photo_installed') if PHOTO_MAIN else get_text(user_id, 'settings_photo_not_installed')
    await call.message.delete()
    await call.message.answer(
        f"""{get_text(user_id, 'settings_title')}

{get_text(user_id, 'settings_photo_status')} {photo_status}

Выберите действие:""",
        reply_markup=settings_menu(user_id)
    )
    await call.answer()

@dp.callback_query(lambda c: c.data == "settings_change_photo")
async def settings_change_photo(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'settings_photo_upload'), reply_markup=back_to_worker_panel_inline(user_id))
    await state.set_state(SettingsStates.waiting_for_photo)
    await call.answer()

@dp.message(SettingsStates.waiting_for_photo)
async def process_photo_upload(message: types.Message, state: FSMContext):
    global PHOTO_MAIN
    user_id = message.from_user.id
    if not is_worker(user_id):
        await message.answer(get_text(user_id, 'settings_access_denied'))
        await state.clear()
        return
    if not message.photo:
        await message.answer(get_text(user_id, 'settings_photo_error'), reply_markup=back_to_worker_panel_inline(user_id))
        return
    photo = message.photo[-1]
    PHOTO_MAIN = photo.file_id
    await message.answer(get_text(user_id, 'settings_photo_success'), reply_markup=back_to_worker_panel_inline(user_id))
    await state.clear()

@dp.callback_query(lambda c: c.data == "settings_remove_photo")
async def settings_remove_photo(call: types.CallbackQuery):
    global PHOTO_MAIN
    user_id = call.from_user.id
    if not is_worker(user_id):
        await call.answer(get_text(user_id, 'settings_access_denied'), show_alert=True)
        return
    PHOTO_MAIN = None
    await call.message.delete()
    await call.message.answer(get_text(user_id, 'settings_photo_removed'), reply_markup=settings_menu(user_id))
    await call.answer()

# ===== VIP МОДЕЛИ =====
@dp.callback_query(lambda c: c.data == "vip_models")
async def vip_models(call: types.CallbackQuery):
    user_id = call.from_user.id
    await call.message.delete()
    await call.message.answer(
        get_text(user_id, 'vip_placeholder'),
        reply_markup=back_to_main_menu(user_id)
    )
    await call.answer()

# ===== SUBMIT =====
@dp.callback_query(lambda c: c.data == "submit")
async def submit(call: types.CallbackQuery):
    user_id = call.from_user.id
    await call.message.delete()
    await call.message.answer(
        get_text(user_id, 'submit_placeholder'),
        reply_markup=back_to_main_menu(user_id)
    )
    await call.answer()

# ===== ОБРАБОТКА ОШИБОК =====
@dp.errors()
async def errors_handler(update: types.Update, exception: Exception):
    logging.error(f"Ошибка: {exception}")
    return True

# ===== ЗАПУСК =====
async def main():
    logging.info("🤖 Бот запущен!")
    logging.info(f"👤 Воркеры: {WORKER_IDS}")
    logging.info(f"📊 Анкет в базе: {len(PROFILES)}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())