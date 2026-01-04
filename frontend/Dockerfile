FROM node:20-alpine

WORKDIR /app

# تثبيت المكتبات
COPY package*.json ./
RUN npm install --legacy-peer-deps

# نسخ الكود
COPY . .

# بدل 'next start'، سنستخدم 'next dev' للتشغيل المباشر والحي
EXPOSE 3000
CMD ["npm", "run", "dev"]