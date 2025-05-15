# How to create an S3 Web Hosting


## Create an S3 Bucket with default configurations except "Block all public access". Uncheck the box! Also name the bucket as the website name!

![GitHub Image](/ingotteknoloji.com/images/blockAllPublic.png)

## Once you've created the bucket, go to your Bucket Properties. Scroll all the way down and enable "Static Website Hosting". Enter your html file name.(index.html, web.html). Note that the html file must be under root in the bucket!

![GitHub Image](/ingotteknoloji.com/images/staticWebsiteHosting.png)

## Go to your Bucket Permissions. Add the following bucket policy.

```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicAccess",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<YourBucketName>/*"
        }
    ]
}

```

![GitHub Image](/ingotteknoloji.com/images/bucketPolicy.png)

## Then create an IAM user for auto-deployment from Github. So go to IAM > Users > Create User. Also create a policy for the user. (You can limit the permissions!). Do not enable console access!!

```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowAllS3Actions",
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::<YourBucketName>",
                "arn:aws:s3:::<YourBucketName>/*"
            ]
        }
    ]
}

```

![GitHub Image](/ingotteknoloji.com/images/userPolicy.png)

## Create an access key for your user. IAM > Users > <YourUser> > Security credentials > Access keys > Create access key

![GitHub Image](/ingotteknoloji.com/images/accessKey.png)

## Go to your repository. Create .github/workflows if doesn't exist. Then create workflow yaml file. This project doesn't require to be built so just sync the files under public folder with the bucket. 

```bash

name: S3 WebSite Deploy

on:
  workflow_dispatch:
  push:
    branches:
      - develop
    paths:
      - 'public/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.INGOTTEKNOLOJI_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.INGOTTEKNOLOJI_SECRET_ACCESS_KEY }}
          aws-region: eu-central-1

      - name: Sync files to S3
        run: aws s3 sync public/ s3://<YourBucketName> --delete

```

## Add the "Access Key ID" and "Secret Access Key" to the repository secrets.

![GitHub Image](/ingotteknoloji.com/images/githubSecrets.png)