# Ingress-Nginx Helm Chart Installation Guide

## Adding Helm Chart Repository
Visit [Ingress-Nginx Helm Chart](https://github.com/kubernetes/ingress-nginx/tree/main/charts/ingress-nginx) for detailed information.
```shell
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

# Internal nginx ingress controller

## Creating Namespace
```shell
kubectl create ns nginx-internal
```

Installing Helm Chart
To install the Ingress-Nginx Helm Chart with customized values for creating an internal-only ingress / DaemonSet, follow these steps:

Make sure you have the nginx-values.yml file with your desired configurations ready

Run the following command:
```shell
helm install nginx-internal ingress-nginx/ingress-nginx --namespace nginx-internal -f .\nginx-values-internal.yml
helm upgrade nginx-internal ingress-nginx/ingress-nginx --namespace ingress-internal -f .\nginx-values-internal.yml
```

# Public nginx ingress controller

## Creating Namespace
```shell
kubectl create ns nginx-public
```

Installing Helm Chart
To install the Ingress-Nginx Helm Chart with customized values for creating an public-only ingress / DaemonSet, follow these steps:

Make sure you have the nginx-values.yml file with your desired configurations ready

Run the following command:
```shell
helm install nginx-internal ingress-nginx/ingress-nginx --namespace nginx-public -f .\nginx-values-public.yml
```
