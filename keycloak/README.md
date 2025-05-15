# Keycloak - Open Source Identity and Access Management

Add authentication to applications and secure services with minimum effort. No need to deal with storing users or authenticating users.

Keycloak provides user federation, strong authentication, user management, fine-grained authorization, and more.

## Check if Bitnami Helm Repository added.

```bash
helm repo list
```

## if Bitnami Helm Repository is not added.

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

## Update your local Helm repositories.

```bash
helm repo update
```

## Update helm values in the default values.yml

1. Change "proxy" to edge from passthrough

![GitHub Image](/keycloak/images/proxy.png)

2. Configure nginx ingress

```bash
ingress:
  enabled: true
  ingressClassName: "nginx-internal"
  pathType: ImplementationSpecific
  apiVersion: ""
  hostname: keycloak.ingotbrokers.dev
  path: "{{ .Values.httpRelativePath }}"
  servicePort: http
  annotations:
   cert-manager.io/issuer: "letsencrypt-clusterissuer"
  labels: {}
  tls: true
  selfSigned: false
  extraHosts: []
  extraPaths: []
  extraTls: []
  secrets: []
  extraRules: []
  ```

3. TLS configuration in Ingress will be wrong. Correct them as below.

```bash
  tls:
    - hosts:
        - '*.ingotbrokers.dev'
      secretName: letsencrypt-cert
```

4. Add your external postgresql.

![GitHub Image](/keycloak/images/postgresql.png)

5. Enable autoscaling.

![GitHub Image](/keycloak/images/autoscaling.png)

6. Specify resources.

![GitHub Image](/keycloak/images/resources.png)

## Create Kubernetes Namespace

Before installing Keycloak, you'll need to create a Kubernetes namespace for it. Run the following command to create a namespace named "keycloak":

```bash
kubectl create namespace keycloak
```

## Install Keycloak

Now, you're ready to install Keycloak. 

1. Run the following command to install Keycloak:

```bash
helm install keycloak bitnami/keycloak --version 24.0.4 -f values-keycloak.yml -n keycloak
```

This command will install keycloak into the "keycloak" namespace.



### Production deployment

```bash
helm upgrade keycloak bitnami/keycloak -f values-prod.yml -n keycloak
```
