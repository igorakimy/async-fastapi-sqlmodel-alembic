FROM node:16-alpine

WORKDIR /frontend

COPY package*.json /frontend/

RUN npm install

COPY ./ /frontend/

ARG FRONTEND_ENV=development

ENV VUE_APP_ENV=${FRONTEND_ENV}

CMD ["npm", "run", "serve"]
