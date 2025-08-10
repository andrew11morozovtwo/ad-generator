
# 🚀 Генератор контента для социальных сетей (учебный проект)

**Flask-приложение для автоматического создания постов на основе анализа веб-сайтов**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI_API-Compatible-yellow.svg)](https://platform.openai.com/)

## 🌟 Особенности

- Анализ контента любого веб-сайта по URL
- Автоматическая генерация 6 аналитических отчетов
- Создание готового поста для соцсетей
- Поддержка моделей GPT-3.5 и GPT-4
- Минималистичный веб-интерфейс

## 📦 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/andrew11morozovtwo/DZ_40.git
cd DZ_40
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env`:
```env
OPENAI_API_KEY=your_api_key_here
# Опционально:
OPENAI_BASE_URL=https://ваш_прокси_сервер
```

## 🖥 Запуск

```bash
python app.py
```

Приложение будет доступно по адресу:  
[http://localhost:5000](http://localhost:5000)

## 🛠 Технологии

- **Python 3.8+**
- **Flask** - веб-фреймворк
- **OpenAI API** - генерация контента
- **BeautifulSoup4** - парсинг веб-страниц
- **Requests** - HTTP-запросы

## 📌 Структура проекта

```
DZ_40/
├── app.py               # Основное Flask-приложение
├── openai_module.py     # Логика работы с OpenAI
├── requirements.txt     # Зависимости
├── .env.example         # Пример конфигурации
└── templates/           # Шаблоны HTML
    ├── index.html       # Главная страница
    ├── processing.html  # Страница загрузки
    ├── results.html     # Результаты анализа
    └── error.html       # Ошибки
```

## 🤖 Как это работает

1. Пользователь вводит URL сайта
2. Система:
   - Скачивает и очищает контент страницы
   - Генерирует 6 аналитических запросов
   - Получает результаты по каждому пункту
   - Формирует готовый пост
3. Результаты отображаются в веб-интерфейсе

## 📸 Скриншоты

![Главная страница](https://example.com/screenshot1.jpg)  
*(Пример: форма ввода URL)*

![Результаты](https://example.com/screenshot2.jpg)  
*(Пример: готовый пост)*

## ⚠️ Важно

- Не публикуйте ваш `.env` файл с API-ключами
- Для коммерческого использования проверьте лимиты OpenAI API
- Приложение требует стабильного интернет-соединения

## 📜 Лицензия

MIT License. Подробнее см. в файле [LICENSE](LICENSE).

---

Разработано [Andrew Morozov](https://github.com/andrew11morozovtwo)  
2023 | Генератор контента для соцсетей

