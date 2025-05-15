#  *Vault Installtion Guide*
Key components:
1. Highly available Vault cluster more than one replica running as statefull.(only 1 is vault is active at a time)
2. Storage backend with Postgresql.
2. Auto-unsealing AWS KMS Symmetric for encryption/decryption.

![GitHub Image](/vault/images/vault_draw.png)

# *Amazon KMS Setup* 
more information https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-conceptual.html
1. *Create a new User in IAM for accessing KMS with username name Example "Vault_dev" dont attach any policies we will attach them on step 2 . Create also programmatic access keys.*
![GitHub Image](/vault/images/iam_user_vault_dev.png)

2.  *Create Symmetric key KMS with default values in your selected region add user created on step 1 as key user so he can access kms , there other ways to do it but this is the most convinient ( if you want you can create iampolicy etc..)*
![GitHub Image](/vault/images/kms-configurekey.png) 

3. *Assign permissions to key users on step 4*
![GitHub Image](/vault/images/kms-keyusers.png)

4. *Create replica keys on another 3 regions eu-central-1,eu-west-2,eu-west-3 etc*
![GitHub Image](/vault/images/replicas_kms.png) 
End result should be similar:
![GitHub Image](/vault/images/kms_end_result.png)

---------------------------------------------------------
# *Creating Postgresql Database*


1. *Create RDS and whitelist nodes*
2. *Create database based on https://developer.hashicorp.com/vault/docs/configuration/storage/postgresql*

```bash
CREATE TABLE vault_kv_store (
  parent_path TEXT COLLATE "C" NOT NULL,
  path        TEXT COLLATE "C",
  key         TEXT COLLATE "C",
  value       BYTEA,
  CONSTRAINT pkey PRIMARY KEY (path, key)
);

CREATE INDEX parent_path_idx ON vault_kv_store (parent_path);
CREATE TABLE vault_ha_locks (
  ha_key                                      TEXT COLLATE "C" NOT NULL,
  ha_identity                                 TEXT COLLATE "C" NOT NULL,
  ha_value                                    TEXT COLLATE "C",
  valid_until                                 TIMESTAMP WITH TIME ZONE NOT NULL,
  CONSTRAINT ha_key PRIMARY KEY (ha_key)
);
```

3. *Create User for postgresql* 

---------------------------------------------------------
# *Installing Vault via Helm chart*

1 *Create Namespace vault*

```bash
kubectl create namespace vault
```

2. *Create k8s Secret that will be used by vault pods for communnicating with KMS (generating iam programmatic access for the user we created  "Vault_dev")*

```bash
kubectl create secret generic -n vault kms-vault-creds --from-literal=AWS_ACCESS_KEY_ID=xxx --from-literal=AWS_SECRET_ACCESS_KEY=xxxx
``` 
3. *Add hashicorp helm repo*

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm show values hashicorp/vault > values.yml
```

4. Update helm values accordingly in values.yml
 - extraSecretEnvironmentVars section
   
```bash
  extraSecretEnvironmentVars:
     - envName: AWS_ACCESS_KEY_ID
       secretName: kms-vault-creds
       secretKey: AWS_ACCESS_KEY_ID
     - envName: AWS_SECRET_ACCESS_KEY
       secretName: kms-vault-creds
       secretKey: AWS_SECRET_ACCESS_KEY    
```   
 - ha section
```bash
   update seal accordingly kms_key_id and region (details can be found on the creation of KMS), enable HA mode and add storage config for POSTRGRESQL

     ha:
    enabled: true
    replicas: 3

    config: |
      ui = true

      listener "tcp" {
        tls_disable = 1
        address = "[::]:8200"
        cluster_address = "[::]:8201"
      }

      seal "awskms" {
          region     = "eu-west-1"
          kms_key_id = "6ef592b8-5da1-49d5-a96b-d6b573be079c"
      }

      storage "postgresql" {
      connection_url = "postgres://POSTGRES_USER:POSTGRES_PASSWORD@postgre-dev-rds-ew1-01.czwe8eg2u3zm.eu-west-1.rds.amazonaws.com:5432/vault",
      table="vault_kv_store",
      ha_enabled=true,
      ha_table="vault_ha_locks" 
      }      
```
 - Storage Class for dataStorage disabled
 ```bash  
  dataStorage:
    enabled: false
```          
 - Ingress section
```bash  
  ingress:
    enabled: true
    labels: {}
      # traffic: external
      # |
      # kubernetes.io/ingress.class: nginx
      # kubernetes.io/tls-acme: "true"
      #   or
      # kubernetes.io/ingress.class: nginx
      # kubernetes.io/tls-acme: "true"

    # Optionally use ingressClassName instead of deprecated annotation.
    # See: https://kubernetes.io/docs/concepts/services-networking/ingress/#deprecated-annotation
    ingressClassName: "nginx-internal"

    # As of Kubernetes 1.19, all Ingress Paths must have a pathType configured. The default value below should be sufficient in most cases.
    # See: https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types for other possible values.
    pathType: Prefix

    # When HA mode is enabled and K8s service registration is being used,
    # configure the ingress to point to the Vault active service.
    activeService: true
    hosts:
      - host: vault.ingotbrokers.dev
        paths: []
    ## Extra paths to prepend to the host configuration. This is useful when working with annotation based services.
    extraPaths: []
    # - path: /*
    #   backend:
    #     service:
    #       name: ssl-redirect
    #       port:
    #         number: use-annotation
    tls: 
      - secretName: letsencrypt-cert
        hosts:
          - "*.ingotbrokers.dev" 
```       
5. Install vault via helm
```bash
helm install vault hashicorp/vault -n vault -f values.yml
```
6. Init vault, the first you launch vault you will need to unseal it manually

First check if pods are in runnings

```bash
kubectl get pods -n vault
```
init vault the first time Save this information into 1password or keepas 
```bash
kubectl -n vault exec -n vault -ti vault-0 -- vault operator init
```

```bash
sample output 

Recovery Key 1: xxxx
Recovery Key 2: xxxx
Recovery Key 3: xxxx
Recovery Key 4: xxxx
Recovery Key 5: xxxx

Initial Root Token: hvs.xxxx

Success! Vault is initialized
```

5. Un-seal vault , Run the below command three times with trhee unseal keys.
```bash
kubectl exec -ti vault-0 -n vault -- vault operator unseal
```

8. Enable Prometheus Metrics (Optional)
If  prometheus Operator is installed you can add monitoring 