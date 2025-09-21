# Docker Cheat Sheet for AI Travel Planner

## Basic Docker Commands

### Building and Running with Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Start services in detached mode (background)
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild a specific service
docker-compose build backend
docker-compose build frontend

# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Individual Docker Commands

```bash
# Build an image
docker build -t travel-planner-backend ./backend
docker build -t travel-planner-frontend ./frontend

# Run containers
docker run -p 8000:8000 --env-file .env travel-planner-backend
docker run -p 3000:80 travel-planner-frontend

# List containers
docker ps          # Running containers
docker ps -a       # All containers

# Stop/Remove containers
docker stop <container_id>
docker rm <container_id>

# List images
docker images

# Remove images
docker rmi <image_id>
```

## Environment Setup

1. Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_key_here
```

2. Build and run:
```bash
docker-compose up --build
```

## AWS Deployment Guide

### Using Amazon ECS (Elastic Container Service)

1. **Push images to Amazon ECR (Elastic Container Registry)**:
```bash
# Login to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <your-ecr-uri>

# Tag images
docker tag travel-planner-backend:latest <your-ecr-uri>/travel-planner-backend:latest
docker tag travel-planner-frontend:latest <your-ecr-uri>/travel-planner-frontend:latest

# Push images
docker push <your-ecr-uri>/travel-planner-backend:latest
docker push <your-ecr-uri>/travel-planner-frontend:latest
```

2. **Create ECS Task Definitions** for both frontend and backend

3. **Create an ECS Cluster** and deploy services

### Using Amazon EC2

1. **Launch an EC2 instance** (Amazon Linux 2 or Ubuntu)

2. **Install Docker and Docker Compose**:
```bash
# For Amazon Linux 2
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Clone your repository and run**:
```bash
git clone <your-repo>
cd ai-travel-planner
# Add your .env file
docker-compose up -d
```

### Using AWS App Runner (Simplest Option)

1. Push your containers to ECR (as shown above)
2. Create an App Runner service for each container
3. Configure environment variables in App Runner console
4. App Runner handles scaling and load balancing automatically

## Troubleshooting

### Common Issues

1. **Port already in use**:
```bash
# Find process using port
lsof -i :8000
lsof -i :3000

# Kill process
kill -9 <PID>
```

2. **Clear Docker cache**:
```bash
docker system prune -a
```

3. **View container logs**:
```bash
docker logs <container_id>
```

4. **Access container shell**:
```bash
docker exec -it <container_id> /bin/bash
```

## Production Considerations

1. **Use environment-specific configs**:
   - `.env.development`
   - `.env.production`

2. **Set up SSL/TLS**:
   - Use AWS Certificate Manager
   - Configure ALB (Application Load Balancer)

3. **Enable monitoring**:
   - AWS CloudWatch for logs
   - Set up alerts for errors

4. **Database considerations**:
   - When adding a database, use Amazon RDS
   - Update docker-compose.yml to include database service

5. **Scaling**:
   - Use ECS with Auto Scaling
   - Configure based on CPU/Memory metrics
