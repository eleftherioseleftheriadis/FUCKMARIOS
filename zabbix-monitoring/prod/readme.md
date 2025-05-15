All the details about installtion can be found here
https://www.zabbix.com/integrations/kubernetes


## Install zabbix helm chart using the folowing commands

kubectl create namespace monitoring
helm repo add zabbix-chart-7.0  https://cdn.zabbix.com/zabbix/integrations/kubernetes-helm/7.0

helm install -f zabbix_values.yaml -n monitoring zabbix zabbix-chart-7.0/zabbix-helm-chrt

Once the helm chart is deployed you need to create a new proxy , the proxy name must match the same name of zabbixProxy.env.ZBX_HOSTNAME so communication can happen (Agent is comunicating with Zabbix Server)

You will then need to create 2 new hosts in zabbix and add Kubernetes Nodes / Cluster templates , follow the guides based on  https://www.zabbix.com/integrations/kubernetes and add the token for authentication in the macros.