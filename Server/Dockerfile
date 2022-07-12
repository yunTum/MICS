FROM node:14
WORKDIR /app
COPY ./src ./
RUN npm install
RUN npm install --save ws bufferutil utf-8-validate
RUN npm audit fix
CMD [ "npm", "run", "start" ]