FROM node:20

WORKDIR /app

COPY . .
RUN npm install --production

RUN mkdir -p /app/uploads

EXPOSE 3000

CMD ["node", "src/server.js"]
