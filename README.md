# DnsDigger
# Zone transfer scanner
# author: CyberPurge
# version: 1.0
# date of release: 10/7/2019

DnsDigger is a scanner for servers that allow DNS ZONE TRANSFER, which leaks the DNS records of the server,these records contain some useful information for the attacker, which gives him several entry point for his attacks.

for example www.example.com has other subdomains like cpanel.example.com, root.example.com, admin.example.com
and zone transfer shows exactly that.
