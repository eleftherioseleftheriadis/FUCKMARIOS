## Retrieve an authentication token and authenticate your Docker client to your registry. Use the AWS CLI:

```bash
aws ecr get-login-password --region eu-central-1 --profile <awsConfigProfileName> | docker login --username AWS --password-stdin 637423636753.dkr.ecr.eu-central-1.amazonaws.com
```

## Build your Docker image using the following command in the same folder with the tar file.

```bash
docker build -t flutter .
```


## After the build completes, tag your image so you can push the image to this repository:

```bash
docker tag flutter:latest 637423636753.dkr.ecr.eu-central-1.amazonaws.com/flutter:latest
```

## Run the following command to push this image to your newly created AWS repository:

```bash
docker push 637423636753.dkr.ecr.eu-central-1.amazonaws.com/flutter:latest
```
