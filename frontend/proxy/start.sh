#!/bin/sh

set -e

export DOLLAR='$'

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

nginx -g "daemon off;"
