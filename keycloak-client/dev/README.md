## Prerequisites

Before deploying the Keycloak Helm chart, you need to create two Kubernetes secrets along with the postgresql databases(RDS)

1. RDS created
1. RDS Database Secret
2. Keycloak Admin Secret


### Creating the RDS Database Secret

Create a Kubernetes secret for the RDS database credentials this will be used by the helm chart adjust accordingly 

  externalDatabase:
    existingSecret: "keycloak-secrets"
    existingSecretHostKey: "db_host"
    existingSecretPortKey: "db_port"
    existingSecretUserKey: "db_user"
    existingSecretDatabaseKey: "db_name"
    existingSecretPasswordKey: "db_password"
    annotations: {}

```bash
kubectl create secret keycloak-secrets \
  --from-literal=db_host=xxx \
  --from-literal=db_name=xx \
  --from-literal=db_password=xx \
  --from-literal=db_port=xx \
  --from-literal=db_user=axx
```

### Creating the Keycloak Admin Secret
Create a Kubernetes secret for the Keycloak admin credential adjust helm values accordingly

  auth:
    ## @param auth.adminUser Keycloak administrator user
    ##
    adminUser: admin
    ## @param auth.adminPassword Keycloak administrator password for the new user
    ##
    adminPassword: ""
    ## @param auth.existingSecret Existing secret containing Keycloak admin password
    ##
    existingSecret: "keycloak-client"

```bash
kubectl create secret generic keycloak-client --from-literal=admin-password=<your-admin-password>
```

### Adjust ingress 
Adjust ingress sections in helm charts and change envrionemnt variable based on your client ingress.

  extraEnvVars:
  # Override the KEYCLOAK_HOSTNAME to use the base URL only, not the path
  # workaround to override the KEYCLOAK_HOSTNAME value without it being impacted by the ingress path
     - name: KEYCLOAK_HOSTNAME
       value: "https://clientportal-sso.ingotbrokers.app/"  # Base URL without the path  


## Adjust metrics section
Under metrics section adjust monitor url based on the realms
      endpoints:
        - path: '{{ include "keycloak.httpPath" . }}metrics'
        - path: '{{ include "keycloak.httpPath" . }}realms/{{ .Values.adminRealm }}/metrics'
          port: http
        - path: '{{ include "keycloak.httpPath" . }}realms/CustomerAuthRealm/metrics'
          port: http        

## Adjust master realm front end url
After installing keycloak adjust frontend URL for master realm to the admin one  https://keycloak-client-admin.ingotbrokers.app so to restrict access to this realm.


## enable metrics

Under realm settings Events add metrics-listener for exposing metrics per realm this will be used by prometheus.
![alt text](image.png)





