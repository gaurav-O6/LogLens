import geoip2.database
import ipaddress
from pathlib import Path


class GeoIPService:
    """
    Service responsible for IP geolocation lookups.
    """

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

            # Private/local IPs cannot be geolocated
            if ip.is_private:
                return {
                    "country": "Local Network",
                    "city": "Private IP",
                    "latitude": None,
                    "longitude": None
                }


            response = self.reader.city(ip_address)

            return {
                "country": response.country.name,
                "city": response.city.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude
            }


        except Exception:
            return {
                "country": "Unknown",
                "city": "Unknown",
                "latitude": None,
                "longitude": None
            }


    def close(self):
        """
        Close database reader.
        """

        self.reader.close()