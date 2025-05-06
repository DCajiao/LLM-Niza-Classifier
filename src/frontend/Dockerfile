FROM node:18 AS builder

WORKDIR /app

COPY package*.json ./
COPY vite.config.js ./
COPY . .

RUN npm install
RUN npm run build

FROM httpd:2.4
COPY --from=builder /app/dist /usr/local/apache2/htdocs/
EXPOSE 80
