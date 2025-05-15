1. create s3 bucket to store the buckets in our case "k8s-vault-backup"
![alt text](image.png)

2. Create iam role and iam policy for accessing s3 bucket this will be used by service account using pod identity plugin more information how it works see example (After creating the service account in the namespace we will use a special command to annotate the service account with the iamrole created on step 4)
https://github.com/IngotTech/infra_k8s_config/tree/develop/Amazon%20EKS%20Pod%20Identity%20Agent%20-%20For%20accessing%20other%20AWs%20resources


In the following policies we are creating 2 policies and 2 roles one for the development and production.

s3-access-k8s-vault-backup-dev

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:PutBucketVersioning",
                    "s3:GetObjectVersion"
                ],
                "Resource": [
                    "arn:aws:s3:::k8s-vault-backup",
                    "arn:aws:s3:::k8s-vault-backup/dev/*"
                ]
            }
        ]
    }

s3-access-k8s-vault-backup-prod

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:PutBucketVersioning",
                    "s3:GetObjectVersion"
                ],
                "Resource": [
                    "arn:aws:s3:::k8s-vault-backup",
                    "arn:aws:s3:::k8s-vault-backup/prod/*"
                ]
            }
        ]
    }


IAMROLE using the following trusted entity + policy created on previous step 

s3-access-k8s-vault-backup-role-DEV

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "pods.eks.amazonaws.com"
                },
                "Action": [
                    "sts:AssumeRole",
                    "sts:TagSession",
                    "sts:SetContext"
                ],
                "Condition": {
                    "StringEquals": {
                        "aws:SourceAccount": "637423636753"
                    },
                    "ArnEquals": {
                        "aws:SourceArn": "arn:aws:eks:eu-west-1:637423636753:cluster/eks_cluster_dev"
                    }
                }
            }
        ]
    }

s3-access-k8s-vault-backup-role-PROD

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "pods.eks.amazonaws.com"
                },
                "Action": [
                    "sts:AssumeRole",
                    "sts:TagSession",
                    "sts:SetContext"
                ],
                "Condition": {
                    "StringEquals": {
                        "aws:SourceAccount": "637423636753"
                    },
                    "ArnEquals": {
                        "aws:SourceArn": "arn:aws:eks:eu-central-1:637423636753:cluster/eks_cluster_prod"
                    }
                }
            }
        ]
    }

2. create namespace for storing the cronjob e.g "vault-backup" and also create a service account

    kubectl create namespace vault-backup
    kubectl create sa vault-backup-sa -n vault-backup

3.  Create Pod identity association

    aws eks create-pod-identity-association --cluster-name eks_cluster_dev --namespace vault-backup --service-account vault-backup-sa --role-arn arn:aws:iam::637423636753:role/s3-access-k8s-vault-backup-role-DEV --region eu-west-1 --profile ingot-tech

3. create a username and password for the backup user either from cli or ui 
![alt text](image-1.png)
in our example "vault-backup"

4. Create a new policy for allowing backup policies
Create new Policy based on backup_policy.hcl
![alt text](image-3.png)

5. Apply the policy into the user via cli
![alt text](image-2.png)

vault write auth/userpass/users/vault_backup/policies policies="backup_policy"

6. Store Username and password into kubernetes generic secrets for this namespace example secret.yml
Example

    kubectl  apply -f .\secret.yml 

    apiVersion: v1
    kind: Secret
    metadata:
    name: vault_backup_creds
    type: Opaque
    data:
    username: YWRtaW4=  # base64 encoded value of 'admin'
    password: cGFzc3dvcmQ=  # base64 encoded value of 'password'

7.  Apply the cronjob  adjust accordingly

    kubectl apply backup.yml
