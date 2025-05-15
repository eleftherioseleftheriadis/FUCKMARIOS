# Pre-requests
PodAmazon EKS Pod Identity Agent must be installed on the cluster. By default when using terraform this is already deployed as a daemon set inside the cluster.

![image](plugin.png)

You can check if this is running using the following command
```bash
aws eks describe-addon --cluster-name eks_cluster_dev --region eu-west-1 --addon-name eks-pod-identity-agent --profile ingot-tech
```
![image](plugin_describe.png)


##  Example scenario you have a Pod and you wish to allow readonly access to S3 bucket

1. Create a new IAMROLE that will be used by your service account and then assosiated by the Pod/Deployment


You can use this through the IAM user interface or using the following command, You will need to add the following trust-relation-ship as specified inside the eks-pod-idenity-trust-policy.json


```bash
aws iam create-role --role-name s3-app-eks-pod-identity-role  --assume-role-policy-document file://eks-pod-identity-trust-policy.json  --output text --query 'Role.Arn' --profile ingot-tech
```
Example resulted policy
![image](result_iamrole.png)

2. Attach any policies based on your request in our example read only access to s3 bucket , you can do this through ui or using cli

```bash
aws iam attach-role-policy --role-name s3-app-eks-pod-identity-role --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess  --profile ingot-tech
```


3. Now that the role is ready we can create-pod-idenity association this can be done either through UI or through cli

navigate to EKS and Access and click create pod identity associations and add the iamrole created /namespace and service account. If you cant find service account or namespace you will need to create them.

![image](pod_identity_associations_create.png)

![alt text](identity_details.png)

```bash
aws eks create-pod-identity-association --cluster-name eks_cluster_dev --namespace test --service-account s3-app-sa-test --role-arn arn:aws:iam::637423636753:role/s3-app-eks-pod-identity-role --region eu-west-1 --profile ingot-tech
```

4. Example deployment.yml

create namespace test , service account and a Pod that will be allowed access to s3. 
For testing purposes the Pod is doing infinite loop so you can ssh on it using Lens or kubectl and execute aws s3 ls for testing purposes.

if you comment out serviceAccountName: s3-app-sa-test on the Pod will see that S3 is no longer accessible.

