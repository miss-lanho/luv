FROM php:8.2-fpm

# Cài Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Copy mã nguồn
COPY . /opt/render/project/src
WORKDIR /opt/render/project/src

# Copy file Nginx config
COPY nginx.conf /etc/nginx/sites-available/default

# Cấp quyền thực thi cho start.sh
RUN chmod +x /opt/render/project/src/start.sh

EXPOSE 10000
CMD ["./start.sh"]
