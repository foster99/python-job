#!/bin/bash

# Permissions of var folder
chown -R www-data:www-data /var/www/var
mkdir -p /var/www/var/cache
cd /var/www/var/cache
umask 000
chmod 777 -R /var/www/var/cache /var/www/var/logs

# Composer install
cd /var/www
/usr/bin/php composer install

# Other Dockerfile directives are still valid
/usr/sbin/apache2ctl -D FOREGROUND

