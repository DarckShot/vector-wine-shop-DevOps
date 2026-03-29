FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --platform=linux --arch=x64

COPY index.html ./
COPY tsconfig.json tsconfig.app.json tsconfig.node.json ./
COPY vite.config.ts ./
COPY public ./public
COPY src ./src

RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]