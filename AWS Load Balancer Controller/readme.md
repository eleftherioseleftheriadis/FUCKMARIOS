https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.8/

https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.8/deploy/installation/




# Create a new Policy for Load balancer deployment
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.8.2/docs/install/iam_policy.json" -OutFile "iam-policy.json"

aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam-policy.json --profile ingot-tech

# Create a new Role  "aws-load-balancer-controller-prod" with the following trust relationship in our example production oidc

![alt text](image.png)

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
					"oidc.eks.eu-central-1.amazonaws.com/id/5B7A111E31C92589A14C12972D8021B4:sub": "system:serviceaccount:kube-system:aws-load-balancer-controller"
				}
			}
		}
	]
}


helm repo add eks https://aws.github.io/eks-charts

helm show values eks/aws-load-balancer-controller > values.yml

only following values have been changed inside the load balancer.

--set clusterName=eks_cluster_prod--set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller

helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system  -f .\values.yml


https://github.com/aws/eks-charts/tree/master/stable/aws-load-balancer-controller

