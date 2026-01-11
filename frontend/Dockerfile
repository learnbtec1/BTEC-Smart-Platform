# builder stage
FROM node:25-alpine AS builder
WORKDIR /app

# copy only package files first to leverage cache
COPY package*.json ./
RUN npm ci

# copy rest and build
COPY . .
RUN npm run build

# production image
FROM node:25-alpine
WORKDIR /app
ENV NODE_ENV=production

# copy built assets and node_modules from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./

EXPOSE 3000
CMD ["npm", "start"]