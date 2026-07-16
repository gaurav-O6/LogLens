from app.services.geoip_service import GeoIPService


geo = GeoIPService()


test_ips = [
    "8.8.8.8",
    "192.168.1.10"
]


for ip in test_ips:

    result = geo.lookup(ip)

    print(ip)
    print(result)
    print("----------------")