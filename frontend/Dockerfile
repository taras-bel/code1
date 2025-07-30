# Используем официальный Node.js 20 Alpine образ
FROM node:20-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и lock-файл
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем только необходимые файлы
COPY nuxt.config.ts ./
COPY tailwind.config.js ./
COPY tsconfig.json ./
COPY app.vue ./
COPY assets/ ./assets/
COPY components/ ./components/
COPY composables/ ./composables/
COPY config/ ./config/
COPY layouts/ ./layouts/
COPY pages/ ./pages/
COPY public/ ./public/
COPY server/ ./server/
COPY utils/ ./utils/

# Копируем воркер pdf.js (ESM)
RUN cp node_modules/pdfjs-dist/build/pdf.worker.min.mjs public/pdf.worker.min.mjs

# Собираем production-версию
RUN npm run build

# Открываем порт 3000
EXPOSE 3000

# Запускаем приложение
CMD ["npm", "run", "start"] 