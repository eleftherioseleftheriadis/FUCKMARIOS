## Documentation
https://karpenter.sh/docs/getting-started/


## Prerequists 

Before installing Karpenter you need to configure AWS IAM roles,Pod idenity for the service account and SQS that Karpenter will subscribe for interuption events

You  have two options here 1 use terraform or cloud formation provided these are official and provided by AWS

https://karpenter.sh/docs/reference/cloudformation/

https://github.com/terraform-aws-modules/terraform-aws-eks/tree/master/modules/karpenter

In our example we have installed all componenets using module and used Pod identity Plugin
Example config https://github.com/IngotTech/terraform-infra/blob/develop/eks_development/main.tf

check module section

Example resources created
![alt text](image.png)

# Prepare Helm values
```bash
helm install karpenter oci://public.ecr.aws/karpenter/karpenter --version 0.37.0  --namespace kube-system -f values.yaml
```
It is best practice to create a separate Node group  for Karpenter

 

# How to upgrade example


Read https://karpenter.sh/docs/upgrading/upgrade-guide/ and perform upgrade based on this command


helm upgrade karpenter-crd oci://public.ecr.aws/karpenter/karpenter-crd --version "1.0.8" --namespace kube-system


helm upgrade karpenter oci://public.ecr.aws/karpenter/karpenter --version 1.0.8  --namespace kube-system -f values-prod.yaml 
