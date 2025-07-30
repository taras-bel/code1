# Инструкция по подключению AI (OpenRouter) для NoaMetrics

## 1. Регистрация и получение API-ключа
- Перейдите на https://openrouter.ai/
- Зарегистрируйтесь и войдите в аккаунт.
- Перейдите в раздел [API Keys](https://openrouter.ai/keys) и создайте новый ключ.
- Скопируйте ключ (например, `sk-or-v1-...`).

## 2. Выбор модели
- Рекомендуемая бесплатная модель: `mistralai/mistral-small-3.2-24b-instruct:free`
- Можно выбрать любую другую модель из [списка поддерживаемых](https://openrouter.ai/docs#models) (платные — без маскировки вывода).

## 3. Настройка переменных окружения
В файле `backend/.env` добавьте:
```
OPENROUTER_API_KEY=ваш_ключ
```

## 4. Настройка backend
В файле `main.py` должно быть:
```python
AI_MODEL = "mistralai/mistral-small-3.2-24b-instruct:free"
```

## 5. Тестирование AI-интеграции
Создайте файл `test_openrouter.py`:
```python
import requests

API_KEY = "ваш_ключ"
MODEL = "mistralai/mistral-small-3.2-24b-instruct:free"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": MODEL,
    "messages": [
        {"role": "user", "content": "Привет! Оцени это резюме по 100-балльной шкале: Иван Иванов, Python Developer, опыт 5 лет..."}
    ]
}

response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
response.raise_for_status()
print(response.json()["choices"][0]["message"]["content"])
```
Запустите:
```
python test_openrouter.py
```

## 6. Использование в проекте
- После настройки ключа и модели backend будет автоматически отправлять текст CV в AI для оценки и рекомендаций.
- Для production рекомендуется использовать платную модель (без маскировки вывода).

---

**Теперь AI-интеграция полностью готова!** 