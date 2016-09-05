#!/usr/bin/env bash

basedir="$( cd "$( dirname "$0" )" && pwd )"

echo "copy nginx config into place"
echo "$basedir/nginx.conf /etc/nginx/sites-enabled/default"
cp nginx.conf /etc/nginx/sites-enabled/default

service nginx restart
