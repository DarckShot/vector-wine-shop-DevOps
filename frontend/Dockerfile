FROM node:20-alpine AS build
WORKDIR /app

# Копируем только package файлы
COPY package*.json ./

# Очищаем кэш и устанавливаем зависимости с указанием платформы
RUN rm -rf node_modules package-lock.json && \
    npm cache clean --force && \
    npm install --platform=linux --arch=x64

# Копируем остальные файлы
COPY . .

# Собираем проект
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]