#!/bin/bash

kubectl delete -f mongodb-deployment.yaml
kubectl delete -f mongodb-service.yaml
kubectl delete -f rabbitmq-deployment.yaml
kubectl delete -f rabbitmq-service.yaml
kubectl delete -f converter-deployment.yaml
kubectl delete -f converter-service.yaml
kubectl delete -f gateway-deployment.yaml
kubectl delete -f gateway-service.yaml
