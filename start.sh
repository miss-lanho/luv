#!/bin/bash
# Render cung cấp biến môi trường $PORT → dùng cho Nginx
PORT=${PORT:-10000}

# Thay cổng mặc định 80 thành $PORT
sed -i "s/80/$PORT/g" /etc/nginx/conf.d/default.conf

# Khởi động PHP-FPM và Nginx
service php-fpm start
nginx -g "daemon off;"
