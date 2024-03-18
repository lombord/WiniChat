FROM node:lts-alpine as builder

WORKDIR /usr/src/app

COPY package*.json ./

RUN --mount=type=cache,target=/usr/src/app/.npm \
    npm set cache /usr/src/app/.npm && \
    npm ci

COPY . .

RUN npm run build

FROM nginxinc/nginx-unprivileged:1-alpine3.18-slim

COPY ./proxy/proxy_params ./proxy/default.conf.tpl /etc/nginx/
COPY ./proxy/start.sh ./
COPY --link --from=builder /usr/src/app/dist/ /usr/share/nginx/html

USER root

# ensure that default.conf exists
RUN touch /etc/nginx/conf.d/default.conf && \ 
    # create static directory and make it accessible 
    mkdir -p /vol/web/ && chmod 755 -R /vol/web && \
    # change owner of default.conf to non-root user
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    # enable execution for start.sh script
    chmod +x /start.sh

ENV LISTEN_PORT=8080

USER nginx
EXPOSE 8080

ENTRYPOINT [ "sh", "-c", "/start.sh" ]