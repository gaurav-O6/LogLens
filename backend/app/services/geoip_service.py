import geoip2.database
import ipaddress
from pathlib import Path


class GeoIPService:
    """
    Service responsible for IP geolocation lookups.
    """

    # Demo location for private/internal IP addresses
    # (Center of India)
    PRIVATE_LATITUDE = 20.5937
    PRIVATE_LONGITUDE = 78.9629

    def __init__(self):
        db_path = (
            Path(__file__)
            .resolve()
            .parent
            .parent
            / "geoip"
            / "GeoLite2-City.mmdb"
        )

        self.reader = geoip2.database.Reader(str(db_path))

    def lookup(self, ip_address):
        """
        Return geographic information for an IP address.
        """

        try:

            ip = ipaddress.ip_address(ip_address)

            # Private/local IPs
            if ip.is_private:

                return {
                    "country": "Local Network",
                    "city": "Internal Network",
                    "latitude": self.PRIVATE_LATITUDE,
                    "longitude": self.PRIVATE_LONGITUDE,
                    "is_private_ip": True,
                }

            response = self.reader.city(ip_address)

            return {
                "country": response.country.name or "Unknown",
                "city": response.city.name or "Unknown",
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "is_private_ip": False,
            }

        except Exception:

            return {
                "country": "Unknown",
                "city": "Unknown",
                "latitude": None,
                "longitude": None,
                "is_private_ip": False,
            }

    def close(self):
        """
        Close database reader.
        """

        self.reader.close()