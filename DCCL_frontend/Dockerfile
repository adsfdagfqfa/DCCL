# ---------- 阶段 1：编译 ----------
#build产生dist目录
FROM node:18-alpine AS build

WORKDIR /app

# 1. 先单独拷贝 package 相关文件，利用 Docker 缓存
COPY package*.json ./
RUN npm ci 
# --only=production

# 2. 拷贝源码并构建
COPY . .
RUN npm run build          
# 默认输出目录 dist/

# ---------- 阶段 2：运行 ----------
FROM nginx:alpine AS runtime

# 把编译产物拷到 Nginx 默认静态目录
COPY --from=build /app/dist /usr/share/nginx/html

# 可选：用自己写的 nginx.conf（如项目里有就解开下一行）
COPY nginx.conf /etc/nginx/conf.d/nginx.conf

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]