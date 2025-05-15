
# Create SG for  EFS storage

Use UI or Commands as shown bellow adjust accordingly

aws ec2 create-security-group --description 'efs-storage for kubernetes' --group-name 'efs-eks_dev-sg' --vpc-id 'vpc-0c1209161bc53de03' --profile ingot-tech --region eu-west-1

# Add an NFS inbound rule so that resources in your VPC can communicate with your Amazon EFS file system:
    
    aws ec2 authorize-security-group-ingress --group-id sg-0753ed1f3139dcc44 --protocol tcp --port 2049 --cidr 10.101.50.0/24 --profile ingot-tech --region eu-west-1
    aws ec2 authorize-security-group-ingress --group-id sg-0753ed1f3139dcc44 --protocol tcp --port 2049 --cidr 10.101.51.0/24 --profile ingot-tech --region eu-west-1
    aws ec2 authorize-security-group-ingress --group-id sg-0753ed1f3139dcc44 --protocol tcp --port 2049 --cidr 10.101.52.0/24 --profile ingot-tech --region eu-west-1
    aws ec2 authorize-security-group-ingress --group-id sg-0753ed1f3139dcc44 --protocol tcp --port 2049 --cidr 10.101.224.0/19 --profile ingot-tech --region eu-west-1
    aws ec2 authorize-security-group-ingress --group-id sg-0753ed1f3139dcc44 --protocol tcp --port 2049 --cidr 10.101.160.0/19 --profile ingot-tech --region eu-west-1
    aws ec2 authorize-security-group-ingress --group-id sg-0753ed1f3139dcc44 --protocol tcp --port 2049 --cidr 10.101.192.0/19 --profile ingot-tech --region eu-west-1
    
# Create an Amazon EFS file system - Customized
![alt text](image-2.png)

For Network access select CORP ZONE subnets and the sg group create on previous step
![alt text](image-3.png)
end result
![alt text](image-4.png)

take note of the File system ID "fs-06ef731f908e8b3fa"

Example deployments can be found here
https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/dynamic_provisioning/specs/storageclass.yaml

also you can check deployment_efs.yaml example
