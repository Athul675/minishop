FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "src", "-l", "3000"]
