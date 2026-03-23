FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm install -g serve
RUN npm install react-scripts
RUN npx react-scripts build

EXPOSE 3000

CMD ["serve", "-s", "src", "-l", "3000"]
