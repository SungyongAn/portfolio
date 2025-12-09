# Nginx で静的ファイルを配信
FROM nginx:stable-alpine

# フロントの HTML と JS を Nginx 配下にコピー
COPY . /usr/share/nginx/html

# ポート 80 を expose
EXPOSE 80

# Nginx をフォアグラウンドで起動
CMD ["nginx", "-g", "daemon off;"]
