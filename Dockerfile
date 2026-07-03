FROM node:22-slim

WORKDIR /app
ENV LANG=C
ENV LC_ALL=C

COPY package*.json ./
RUN npm install --include=dev

COPY . .

ENV NODE_ENV=production
CMD ["npm", "run", "witness:verify", "--", ".runtime/witnesses/latest.json"]
