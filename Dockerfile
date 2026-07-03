FROM node:22-slim

WORKDIR /app
ENV NODE_ENV=production
ENV LANG=C
ENV LC_ALL=C

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "witness:verify", "--", ".runtime/witnesses/latest.json"]
