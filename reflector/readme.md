# Using Emberstack Helm Chart for Reflector

## Add Emberstack Helm Repository

To begin, you need to add the Emberstack Helm repository to your local Helm setup. Run the following command:

```bash
helm repo add emberstack https://emberstack.github.io/helm-charts
```

After adding the repository, make sure to update your local Helm repositories using:

```bash
helm repo update
```

## Create Kubernetes Namespace

Before installing Reflector, you'll need to create a Kubernetes namespace for it. Run the following command to create a namespace named "reflector":

```bash
kubectl create namespace reflector
```

## Install Reflector

Now, you're ready to install Reflector using the Helm chart provided by Emberstack. Run the following command, adjusting the path to your reflector-values.yml file if necessary:

```bash
helm upgrade --install reflector emberstack/reflector -f ./reflector-values.yml -n reflector
```

This command will install Reflector into the "reflector" namespace using the configuration specified in your reflector-values.yml file.

## Additional Configuration

Make sure to customize the values in your reflector-values.yml file according to your specific requirements before installing Reflector.

For more information on configuring Reflector or troubleshooting installation issues, refer to the [official documentation](https://github.com/emberstack/kubernetes-reflector).
