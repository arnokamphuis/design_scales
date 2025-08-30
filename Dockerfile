# Use nginx alpine for serving static files
FROM nginx:alpine

# Set maintainer info
LABEL maintainer="Terrain Scaling Calculator"
LABEL description="Modern web application for calculating terrain image scaling factors"

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy webapp files to nginx html directory
COPY webapp/ /usr/share/nginx/html/

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]