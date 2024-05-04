# Use a slim image of Nginx
FROM nginx:alpine

# Copy the HTML file into the nginx directory
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80
CMD service nginx start