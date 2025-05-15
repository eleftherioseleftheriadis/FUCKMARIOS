# aws ec2 create-security-group --group-name "Cloudflare WAF IPs" --description "Security group for Cloudflare WAF IPs" --vpc-id vpc-0d924ecc9c8e05b86 --profile ingot-old --region eu-central-1

$groupId = "sg-007539335fcd12f0a"

$cloudflareIPv4 = @(
"173.245.48.0/20",
"103.21.244.0/22",
"103.22.200.0/22",
"103.31.4.0/22",
"141.101.64.0/18",
"108.162.192.0/18",
"190.93.240.0/20",
"188.114.96.0/20",
"197.234.240.0/22",
"198.41.128.0/17",
"162.158.0.0/15",
"104.16.0.0/13",
"104.24.0.0/14",
"172.64.0.0/13",
"131.0.72.0/22",
"2400:cb00::/32",
"2606:4700::/32",
"2803:f800::/32",
"2405:b500::/32",
"2405:8100::/32",
"2a06:98c0::/29",
"2c0f:f248::/32"
)

# IPv6 Cloudflare IP ranges
$cloudflareIPv6 = @(
    "2400:cb00::/32",
    "2606:4700::/32",
    "2803:f800::/32",
    "2405:b500::/32",
    "2405:8100::/32",
    "2a06:98c0::/29",
    "2c0f:f248::/32"
)

foreach ($ip in $cloudflareIPv6) {
 aws ec2 authorize-security-group-ingress --group-id $groupId --ip-permissions IpProtocol=tcp,FromPort=443,ToPort=443,Ipv6Ranges="[{CidrIpv6=$ip}]" --profile ingot-old --region eu-central-1
 aws ec2 authorize-security-group-ingress --group-id $groupId --ip-permissions IpProtocol=tcp,FromPort=80,ToPort=80,Ipv6Ranges="[{CidrIpv6=$ip}]" --profile ingot-old --region eu-central-1
}

#IPV4
foreach ($ip in $cloudflareIPv4) {
    aws ec2 authorize-security-group-ingress --group-id $groupId --protocol tcp --port 80 --cidr $ip --profile ingot-old --region eu-central-1
    aws ec2 authorize-security-group-ingress --group-id $groupId --protocol tcp --port 443 --cidr $ip --profile ingot-old --region eu-central-1
}

