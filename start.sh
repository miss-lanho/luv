#!/usr/bin/env bash
# Cài đặt và khởi động PHP + Nginx trên Render

# Cấu hình PHP-FPM
php-fpm -D

# Chạy Nginx foreground để container không dừng
nginx -g 'daemon off;'
