# create namespace
kubectl create namespace data-engineering
# create service account
kubectl apply -f service-account.yml
# create configmaps
kubectl apply -f mt4_appsettings_cm.yml
kubectl apply -f mt5_appsettings_cm.yml
# create secrets for storing database connections
You will need to create three since we are going to run 3 cronjob for each mt instance
# create cronbjos
kubectl apply -f mt5_statement_parser_job.yml / mt4_statement_parser_job.yml / mt5_2_statement_parser_job.yml


# Explanation

1. Main Container (statement-parser-mt4/mt5/mt5_2):

- Runs the main container C# parser.
- Volume mounts and environment variables are set as required.
  
2. Sidecar Container (timeout-manager):

- Runs a simple script that sleeps for 300 seconds (5 minutes) and then sends a SIGTERM signal to the main container.
- Uses the kill -TERM 1 command to send the SIGTERM signal to the main container, where PID 1 is typically the main process in a container.
3. Init Container (init-s3-download):

- Syncs files from the specified S3 bucket to the local /mt-statements directory before the main container starts.
- Volume mounts are set as required.
4. Volumes:

- s3-files: An empty directory used to store files downloaded from S3.
- appsettings: A ConfigMap used to store application settings.
5. Tolerations:
- Ensures the job is scheduled on nodes with the specified tolerations, spot instances
