FROM node:22-slim AS build

WORKDIR /app
ENV LANG=C
ENV LC_ALL=C

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:22-slim AS runtime

WORKDIR /app
ENV NODE_ENV=production
ENV LANG=C
ENV LC_ALL=C

COPY --from=build /app/package*.json ./
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist-ts ./dist-ts
COPY --from=build /app/schemas ./schemas
COPY --from=build /app/scripts ./scripts

CMD ["node", "dist-ts/verifier.js"]
