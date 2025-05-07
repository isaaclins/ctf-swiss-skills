FROM node:alpine

WORKDIR /app

RUN apk add --no-cache net-tools procps

COPY app/package.json ./
RUN npm install

COPY app ./
COPY ./flag.txt /flag.txt

EXPOSE 5003

CMD ["npm", "start"]