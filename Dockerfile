FROM node:22-slim

WORKDIR /app
ENV LANG=C
ENV LC_ALL=C
ENV NODE_ENV=production

COPY package*.json ./
RUN npm ci --include=dev

COPY . .

CMD ["node", "server.js"]
