
![GitHub Image](/certmanager/images/certmanager_main.png)

# Architecture
![GitHub Image](/certmanager/images/architecture.png)

# Setup AWS Credentials

To configure AWS credentials for your EKS cluster, run the following  example command:

```bash
aws eks update-kubeconfig --region eu-west-1 --name eks_cluster_dev --profile ingot-tech
```

# Create namespace for cert-manager
```bash
kubectl create namespace cert-manager
```

# Create API Token for cloudflare
![GitHub Image](/certmanager/images/cloudflare_token.png)
Create a Cloudflare API token in the selected zone. This token should have permissions for editing,reading DNS records since TXT records will be created via certmanager.
Store the credentials as a Secret in the Kubernetes cluster. You can find an example Secret configuration in lets-encrypt-dev.yml, since we are using stringData we dont need to base64 encode the string it will be done automatically kubectl when we apply.
See example letsencrypt-cf-secret-dev.yaml

```bash
kubectl apply -f  lets-encrypt-cf-secret.yml -n cert-manager
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloudflare-api-credentials
type: Opaque
stringData:
  api: asdfasdfa
```

#  Install certmanager

Adjust cert-manager-values.yaml if any changes to default values

```bash
helm upgrade --install cert-manager jetstack/cert-manager  -f .\cert-manager-values.yaml -n cert-manager
```


# create certificate issuing authority

```bash
kubectl apply -f  lets-encrypt-clusterissuer.yml -n cert-manager
```

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-clusterissuer
spec:
  acme:
    email: devops@IngotBrokers.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-private-key
    solvers:
    - dns01:
        cloudflare:
          email: devops@IngotBrokers.com
          apiTokenSecretRef:
            name: cloudflare-api-credentials
            key: api
```            

Check if Cluster Issuer is created
```bash
kubectl get clusterissuer -n cert-manager
```
Samle output
NAME                        READY   AGE
letsencrypt-clusterissuer   True    3h17m

#  create certificate based on the previous cluster issuer authority

```bash
kubectl apply -f  lets-encrypt-certificate.yml -n cert-manager
```

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: letsencrypt-certificate
  namespace: cert-manager
spec:
  **secretName: letsencrypt-cert**
  issuerRef:
    kind: ClusterIssuer
    name: letsencrypt-clusterissuer
  duration: 2160h # 90d
  renewBefore: 360h # 15d
  dnsNames:
    - "*.ingotbrokers.dev"
  secretTemplate:
    annotations:
      reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
      reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: ""
      reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true"
      reflector.v1.k8s.emberstack.com/reflection-auto-namespaces: ""    
```

Check if Certificate is issued successfull 

```bash
kubectl get cert -n cert-manager -n cert-manager
```

if you get Ready = true then it means that the certificate is ready and stored in the secret named  "letsencrypt-cert"

```bash
kubectl get secrets -n cert-manager
kubectl describe secret letsencrypt-cert -n cert-manager
kubectl edit secret letsencrypt-cert -n cert-manager
```

Whenever you create a new namespace reflector will automatically replicate this secret "letsencrypt-cert" in other workspaces


If you get Ready = false then you will need to debug and find out where is the problem 
Refere to https://cert-manager.io/docs/troubleshooting/ and also check pod logs if there are any errors.



