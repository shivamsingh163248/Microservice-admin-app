#!/bin/bash

cd microservice-admin-app

echo "📦 Building Docker images..."
docker-compose build

echo "🚀 Starting services (MySQL → Backend → Frontend)..."
docker-compose up -d

echo "✅ All containers are up and running!"
echo "🌐 Access frontend at: http://localhost:8080"
