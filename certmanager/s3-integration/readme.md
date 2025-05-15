
## create AWS EKS, OpenID Connect (OIDC) provider ( this step is required only if this is not setup)
1. Go to EKS cluster and copy the OIDC provider URL.
![GitHub Image](/certmanager/s3-integration/images/oidc_1.png)
e.g https://oidc.eks.eu-central-1.amazonaws.com/id/5B7A111E31C92589A14C12972D8021B4
2. Go to AWS IAM and check if there are any IAM OIDC providers in AWS IAM for the given "CLUSTER".
If exists you should see something similar 
![GitHub Image](/certmanager/s3-integration/images/oidc_Exists.png)
3. If it doesn't exist you can create
a. Click On Add provider.
![GitHub Image](/certmanager/s3-integration/images/aws-iam-oidc-provider-add.png)

b. Choose openid connect --> Copy EKS OIDC url into Provider URL and click on *Get Thumbprint --> Enter sts.amazonaws.com into the Audience text box --> click on Add Provider**.
![GitHub Image](/certmanager/s3-integration/images/add-iam-oidc-provider-create.png)


## Create S3 bucket for storing wildcard certificates
e.g ingotbrokers-certs s3
## Create an IAM S3 policy. This policy will be attached to the IAM role. Below are the IAM policy details.

Let us assume you create an S3 with the name ingotbrokers-certs, for dev folder in s3 bucket
```bash
{
   "Statement": [
      {
            "Action": [
               "s3:GetObject",
               "s3:GetObjectVersion",
               "s3:PutBucketVersioning",
               "s3:PutObject"
            ],
            "Effect": "Allow",
            "Resource": [
               "arn:aws:s3:::ingotbrokers-certs",
               "arn:aws:s3:::ingotbrokers-certs/dev/*"
            ]
      }
   ],
   "Version": "2012-10-17"
}
```

## Create Service account that will be used by the executed pod and assum  aws iam role that will be created on next step
```bash
apiVersion: v1
kind: ServiceAccount
metadata:
  name: s3-certs-replicator-service-account
  namespace: cert-manager
```

## Create an IAM role for allowing access for specific service accounts in kubernetes
Choose web identity --> Select the above created OIDC provider from Identity provider drop down ---> Choose sts.amazonaws.com from audience drop down --> Click on Next.
![GitHub Image](/certmanager/s3-integration/images/iamrole.png)

## Add policy created on previous step and Adjust Policy to match the service account created in kubernets for extra security
![GitHub Image](/certmanager/s3-integration/images/iamrole_2.png)
Adjust policy 
```bash
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Principal": {
				"Federated": "arn:aws:iam::637423636753:oidc-provider/oidc.eks.eu-central-1.amazonaws.com/id/5B7A111E31C92589A14C12972D8021B4"
			},
			"Action": "sts:AssumeRoleWithWebIdentity",
			"Condition": {
				"StringEquals": {
					"oidc.eks.eu-central-1.amazonaws.com/id/5B7A111E31C92589A14C12972D8021B4:aud": "sts.amazonaws.com",
					"oidc.eks.eu-central-1.amazonaws.com/id/5B7A111E31C92589A14C12972D8021B4:sub": "system:serviceaccount:cert-manager:s3-certs-replicator-service-account"
				}
			}
		}
	]
}
```
Adjust accordingly namespace and serviceaccount name
Add "oidc.eks.eu-central-1.amazonaws.com/id/5B7A111E31C92589A14C12972D8021B4:sub":"system:serviceaccount:*$namespace*:*$serviceaccount*"
![GitHub Image](/certmanager/s3-integration/images/trust_policy_edit.png)
![GitHub Image](/certmanager/s3-integration/images/trust_policy_edit2.png)

# Anotiate service account
kubectl annotate serviceaccount -n $namespace $service_account eks.amazonaws.com/role-arn=arn:aws:iam::$account_id:role/my-role

Annotations: eks.amazonaws.com/role-arn: arn:aws:iam::637423636753:role/eks-s3-ingotbrokers-certs-rw