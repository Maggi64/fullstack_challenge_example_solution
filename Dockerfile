# Python 3.12 base image
FROM python:3.12

# Install curl and gnupg
RUN apt-get update && apt-get install -y \
  curl \
  gnupg \
  && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 LTS
RUN curl -sL https://deb.nodesource.com/setup_22.x | bash -
RUN apt-get install -y nodejs

# Install backend dependencies
COPY ./backend/requirements.txt /app/backend/requirements.txt
RUN pip install -r /app/backend/requirements.txt --no-cache-dir

# Copy dev startup script
COPY ./run_dev.sh /app/run_dev.sh

# Install frontend dependencies
COPY ./frontend/package.json /app/frontend/package.json
COPY ./frontend/package-lock.json /app/frontend/package-lock.json

WORKDIR /app/frontend
RUN npm ci
