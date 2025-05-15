# Redpanda Console – A UI for Data Streaming

## Add Redpanda Helm Repository

To begin, you need to add the Redpanda Helm repository to your local Helm setup. Run the following command:

```bash
helm repo add redpanda https://charts.redpanda.com
```

After adding the repository, make sure to update your local Helm repositories using:

```bash
helm repo update
```

## Update helm values in the default values.yml

- You can find the default values here [https://artifacthub.io/packages/helm/redpanda-data/console?modal=values]

1. Edit the ingress part:

![GitHub Image](/redpanda-console/images/ingress.png)

2. Console config part:

![GitHub Image](/redpanda-console/images/console-config.png)

## Create Kubernetes Namespace

Before installing Redpanda-Console, you'll need to create a Kubernetes namespace for it. Run the following command to create a namespace named "redpanda":

```bash
kubectl create namespace redpanda
```

## Install Redpanda-Console

Now, you're ready to install Redpanda-Console using the Helm chart provided by Redpanda. Run the following command, adjusting the path to your values.yml file if necessary:

```bash
helm install redpanda/console -f values.yml -n redpanda
```

This command will install Redpanda-Console into the "redpanda" namespace using the configuration specified in your values.yml file.

