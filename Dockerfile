# Sử dụng image PHP có sẵn Nginx và PHP-FPM
FROM php:8.2-fpm

# Cài đặt Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Tạo thư mục chạy PHP-FPM
RUN mkdir -p /run/php && chmod -R 755 /run/php

# Copy mã nguồn vào container
WORKDIR /var/www/html
COPY . /var/www/html

# Copy file cấu hình Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Mở port (Render sẽ tự đặt $PORT, nhưng khai báo để dev local dễ test)
EXPOSE 10000

# Chạy script start
CMD ["/start.sh"]
