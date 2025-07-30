import json
import os
from typing import Dict, Any

_LOCALES_CACHE: Dict[str, Dict[str, Any]] = {}
SUPPORTED_LANGUAGES = ["en", "ru", "es"]
DEFAULT_LANGUAGE = "en"
LOCALES_DIR = os.path.join(os.path.dirname(__file__), "../locales")


def load_locale(lang: str) -> Dict[str, Any]:
    lang = lang.lower()
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    if lang in _LOCALES_CACHE:
        return _LOCALES_CACHE[lang]
    path = os.path.join(LOCALES_DIR, f"{lang}.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            _LOCALES_CACHE[lang] = data
            return data
    except Exception:
        if lang != DEFAULT_LANGUAGE:
            return load_locale(DEFAULT_LANGUAGE)
        return {}

def translate(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """Получить перевод по ключу (например, 'errors.invalid_token') и языку."""
    locale = load_locale(lang)
    parts = key.split('.')
    value = locale
    for part in parts:
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return key  # fallback: вернуть ключ
    if isinstance(value, str):
        return value.format(**kwargs)
    return str(value) 