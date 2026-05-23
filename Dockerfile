FROM nginx:1.27-alpine

COPY index.html privacy.html terms.html styles.css /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/

EXPOSE 80
