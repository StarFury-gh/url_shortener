# Собираем проект
FROM node:20-alpine AS build
WORKDIR /app 
# Установка пакетов
COPY ./package*.json . 
RUN npm ci 
COPY . . 
# Собираем
RUN npm run build
# Сжимаем 
RUN node compress.js 
# Запускаем проект
FROM fholzer/nginx-brotli:v1.28.0
# Собранная статика
COPY --from=build /app/dist /usr/share/nginx/html 
# Nginx конфиг
COPY ./default.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080