import geoip2.database
import ipaddress
from pathlib import Path


class GeoIPService:
    """
    Service responsible for IP geolocation lookups.

    GeoIP results are cached by IP address so repeated detections
    from the same source IP do not repeatedly hit the MaxMind
    database.
    """

    # Demo location for private/internal IP addresses
    # (Center of India)
    PRIVATE_LATITUDE = 20.5937
    PRIVATE_LONGITUDE = 78.9629

    # Prevent unbounded memory growth if a huge log contains
    # an extremely large number of unique source IPs.
    MAX_CACHE_SIZE = 10_000

    def __init__(self):

        db_path = (
            Path(__file__)
            .resolve()
            .parent
            .parent
            / "geoip"
            / "GeoLite2-City.mmdb"
        )

        self.reader = geoip2.database.Reader(
            str(db_path)
        )

        self._cache = {}

        self.cache_hits = 0
        self.cache_misses = 0

    def lookup(
        self,
        ip_address,
    ):
        """
        Return geographic information for an IP address.

        Results are cached by IP address to avoid repeating
        the same MaxMind lookup for every detection.
        """

        ip_address = str(
            ip_address or ""
        ).strip()

        if not ip_address:

            return {
                "country": "Unknown",
                "city": "Unknown",
                "latitude": None,
                "longitude": None,
                "is_private_ip": False,
            }

        # ---------------------------------------------------------
        # CACHE LOOKUP
        # ---------------------------------------------------------

        cached = self._cache.get(
            ip_address
        )

        if cached is not None:

            self.cache_hits += 1

            return cached

        self.cache_misses += 1

        # ---------------------------------------------------------
        # IP VALIDATION
        # ---------------------------------------------------------

        try:

            ip = ipaddress.ip_address(
                ip_address
            )

        except ValueError:

            result = {
                "country": "Unknown",
                "city": "Unknown",
                "latitude": None,
                "longitude": None,
                "is_private_ip": False,
            }

            self._cache_result(
                ip_address,
                result,
            )

            return result

        # ---------------------------------------------------------
        # PRIVATE / INTERNAL IP
        # ---------------------------------------------------------

        if ip.is_private:

            result = {
                "country": "Local Network",
                "city": "Internal Network",
                "latitude": self.PRIVATE_LATITUDE,
                "longitude": self.PRIVATE_LONGITUDE,
                "is_private_ip": True,
            }

            self._cache_result(
                ip_address,
                result,
            )

            return result

        # ---------------------------------------------------------
        # PUBLIC IP â†’ MAXMIND
        # ---------------------------------------------------------

        try:

            response = self.reader.city(
                ip_address
            )

            result = {
                "country":
                    response.country.name
                    or "Unknown",

                "city":
                    response.city.name
                    or "Unknown",

                "latitude":
                    response.location.latitude,

                "longitude":
                    response.location.longitude,

                "is_private_ip":
                    False,
            }

        except Exception:

            result = {
                "country": "Unknown",
                "city": "Unknown",
                "latitude": None,
                "longitude": None,
                "is_private_ip": False,
            }

        self._cache_result(
            ip_address,
            result,
        )

        return result

    def _cache_result(
        self,
        ip_address,
        result,
    ):
        """
        Store a GeoIP result while keeping the cache bounded.
        """

        if len(self._cache) >= self.MAX_CACHE_SIZE:

            # Simple bounded-cache strategy.
            # Remove the oldest inserted entry.
            oldest_key = next(
                iter(self._cache)
            )

            del self._cache[
                oldest_key
            ]

        self._cache[
            ip_address
        ] = result

    def get_cache_stats(self):
        """
        Return cache statistics for profiling/debugging.
        """

        total = (
            self.cache_hits
            + self.cache_misses
        )

        hit_rate = (
            self.cache_hits / total
            if total
            else 0.0
        )

        return {
            "cache_size":
                len(self._cache),

            "cache_hits":
                self.cache_hits,

            "cache_misses":
                self.cache_misses,

            "hit_rate":
                hit_rate,
        }

    def clear_cache(self):
        """
        Clear cached GeoIP results.
        """

        self._cache.clear()

        self.cache_hits = 0
        self.cache_misses = 0

    def close(self):
        """
        Close database reader.
        """

        self.reader.close()
