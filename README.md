# Video to MP3 Conversion Microservices Architecture

## Overview

This project demonstrates a Kubernetes-based microservices architecture for converting videos to MP3 files. The architecture uses RabbitMQ for asynchronous messaging and MongoDB for data storage.

---

## Components

### 1. **Client**
   - Users interact with the system by uploading video files via the API Gateway.

### 2. **API Gateway**
   - Entry point for all client requests.
   - Validates incoming requests and forwards them to other services.

### 3. **Queue Service**
   - **RabbitMQ** is used for task queuing, enabling asynchronous processing.

### 4. **Video-to-MP3 Service**
   - Extracts audio from videos and converts it into MP3 format.
   - Stores the converted files and metadata in **MongoDB**.

### 5. **Storage Database**
   - **MongoDB** is used to store MP3 metadata and binary data.

---

## Technologies Used

- **RabbitMQ**: Manages task queues.
- **MongoDB**: Stores application data.
- **Kubernetes**: Orchestrates containerized services.
- **Docker**: Containerizes services.
- **Python**: Backend services built with FastAPI.

---

## Deployment Steps

### Prerequisites
- Minikube or a Kubernetes cluster
- Docker installed locally

### Files Overview
The directory includes:
- `gateway-deployment.yaml` and `gateway-service.yaml`: Defines the API Gateway.
- `converter-deployment.yaml` and `converter-service.yaml`: Defines the Video-to-MP3 service.
- `rabbitmq-deployment.yaml` and `rabbitmq-service.yaml`: Deploy RabbitMQ.
- `mongodb-deployment.yaml` and `mongodb-service.yaml`: Deploy MongoDB.
- `apply.sh`: Automates the deployment of all services.
- `delete.sh`: Automates the teardown of all services.

---

### Deployment Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build Docker Images**:
   ```bash
   docker build -t gateway ./gateway
   docker build -t converter ./converter
   ```

3. **Start Kubernetes Cluster**:
   ```bash
   minikube start
   ```

4. **Deploy the Services**:
   Use the `apply.sh` script to deploy all services:
   ```bash
   chmod +x apply.sh
   ./apply.sh
   ```
   Alternatively, manually apply the YAML files:
   ```bash
   kubectl apply -f rabbitmq-deployment.yaml
   kubectl apply -f rabbitmq-service.yaml
   kubectl apply -f mongodb-deployment.yaml
   kubectl apply -f mongodb-service.yaml
   kubectl apply -f gateway-deployment.yaml
   kubectl apply -f gateway-service.yaml
   kubectl apply -f converter-deployment.yaml
   kubectl apply -f converter-service.yaml
   ```

5. **Verify Deployment**:
   Check the status of your Kubernetes resources:
   ```bash
   kubectl get pods
   kubectl get services
   ```

6. **Access the Application**:
   - Forward the API Gateway service to your local machine:
     ```bash
     kubectl port-forward svc/<gateway-service-name> 8080:80
     ```
   - Interact with the API at `http://localhost:8080`.

---

### Teardown Instructions

To remove all deployed resources, run the `delete.sh` script:
```bash
chmod +x delete.sh
./delete.sh
```

---

## API Endpoints

### API Gateway
- **POST /upload**: Upload a video file for conversion.
- **GET /status/{id}**: Check the status of a conversion request.

---

## Future Improvements
- Add logging and monitoring for debugging and scaling.
- Optimize resource usage for RabbitMQ and MongoDB.
