FROM node:20-alpine as build

WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy source code and build
COPY . .
RUN npm run build

# Serve with nginx
FROM nginx:alpine

# Copy custom nginx config if needed, otherwise use default
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build files to nginx web root
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
