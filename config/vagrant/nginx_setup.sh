#!/usr/bin/env bash

basedir = `dirname $0`
echo "copy nginx config into place"
echo "$basedir/nginx.conf /etc/nginx/sites-enabled/default"
cp $basedir/nginx.conf /etc/nginx/sites-enabled/default

service nginx restart
