map ${DOLLAR}http_upgrade ${DOLLAR}connection_upgrade {
    default upgrade;
    '' close;
}

upstream django { 
    server ${DJ_HOST}:${DJ_PORT};
}

# Redirect www to HTTPS non-www
server {
    listen 8080;
    listen 443 ssl;
    server_name www.${WEB_DOMAIN};
    return 301 https://${DOLLAR}host${DOLLAR}request_uri;
}

# Redirect HTTP non-www to HTTPS non-www
server {
    listen 8080;
    server_name ${WEB_DOMAIN};
    return 301 https://${DOLLAR}host${DOLLAR}request_uri;
}

server {
    listen 443 ssl default_server;
    server_name ${WEB_DOMAIN};
    client_max_body_size  400M;
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    # Docker internal dns server
    resolver 127.0.0.11;


    location /static {
        autoindex on;
        alias /vol/web;
    }

    location /api {
        try_files ${DOLLAR}uri @proxy_api;
    }

    location /django-ws {
        rewrite ^/django-ws/?(.*)${DOLLAR} /ws/${DOLLAR}1 break;
        try_files ${DOLLAR}uri @proxy_api;
    }

    location /admin {
        try_files ${DOLLAR}uri @proxy_api;
    }

    location @proxy_api {
        include     /etc/nginx/proxy_params;
        proxy_pass  http://django;
    }

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files ${DOLLAR}uri ${DOLLAR}uri/ /index.html =404;
    }

    include /etc/nginx/extra-conf.d/*.conf;
}