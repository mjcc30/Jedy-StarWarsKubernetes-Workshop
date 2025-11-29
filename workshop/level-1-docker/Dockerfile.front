# Base image
FROM node:24-alpine AS runtime

# Current working directory in the container
WORKDIR /app

# Copy application code
COPY . .

# Install dependencies and build the application
RUN npm install
RUN npm run build

# Set environment variables and expose port
ENV HOST=0.0.0.0
ENV PORT=4321
EXPOSE 4321

# Command to run the application
CMD ["node", "./dist/server/entry.mjs"]