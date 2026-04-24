import requests
from urllib.parse import urlparse
import ipaddress

M3U_URL = "https://garyshare.sharewithyou.dpdns.org/mylist.m3u"

def is_ip(host):
    try:
        ipaddress.ip_address(host)
        return True
    except:
        return False

def get_root_domain(host):
    parts = host.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host

def main():
    text = requests.get(M3U_URL, timeout=15).text

    domains = set()
    ips = set()

    for line in text.splitlines():
        line = line.strip()
        if line.startswith("http"):
            try:
                host = urlparse(line).hostname
                if not host:
                    continue

                if is_ip(host):
                    ips.add(host)
                else:
                    domains.add(get_root_domain(host))
            except:
                pass

    rules = []

    for d in sorted(domains):
        rules.append(f"DOMAIN-SUFFIX,{d}")

    for ip in sorted(ips):
        rules.append(f"IP-CIDR,{ip}/32")

    with open("iptv.list", "w") as f:
        f.write("\n".join(rules))

if __name__ == "__main__":
    main()
