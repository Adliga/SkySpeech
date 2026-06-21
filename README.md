# SkySpeech

Интерфейс для синтеза и клонирования голоса на основе XTTS-v2.

## Требования

- Node.js >= 20
- Python 3.12

## Быстрый старт

### 1. Фронтенд

```sh
npm install
npm run dev        # http://localhost:5173
npm run build      # production-сборка
```

### 2. Бэкенд

```sh
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
python run.py              # http://localhost:8000
```

### 3. Всё сразу

```sh
npm run dev:all      # фронтенд + бэкенд одной командой
```

## Стек

### Фронтенд
- Vue 3 (Composition API, `<script setup>`)
- Pinia — сторы
- Axios — запросы к бэкенду
- Vite — сборка

### Бэкенд
- FastAPI + Uvicorn
- XTTS-v2 (Coqui TTS) — синтез и клонирование голоса
- Librosa — обработка аудио
- SoundFile — чтение/запись WAV
