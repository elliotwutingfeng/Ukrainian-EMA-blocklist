"""Extract fraudulent URLs found at https://www.ema.com.ua/citizens/blacklist
and write them to a .txt blocklist
"""
import ipaddress
import itertools
import logging
import re
import socket
from datetime import datetime

import requests
import tldextract

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(message)s")


def current_datetime_str() -> str:
    """Current time's datetime string in UTC

    Returns:
        str: Timestamp in strftime format "%d_%b_%Y_%H_%M_%S-UTC".
    """
    return datetime.utcnow().strftime("%d_%b_%Y_%H_%M_%S-UTC")


def clean_url(url: str) -> str:
    """Remove zero width spaces, leading/trailing whitespaces, trailing slashes,
    and URL prefixes from a URL

    Args:
        url (str): URL.

    Returns:
        str: URL without zero width spaces, leading/trailing whitespaces, trailing slashes,
    and URL prefixes.
    """
    removed_zero_width_spaces = re.sub(r"[\u200B-\u200D\uFEFF]", "", url)
    removed_leading_and_trailing_whitespaces = removed_zero_width_spaces.strip()
    removed_trailing_slashes = removed_leading_and_trailing_whitespaces.rstrip("/")
    removed_https = re.sub(r"^[Hh][Tt][Tt][Pp][Ss]:\/\/", "", removed_trailing_slashes)
    removed_http = re.sub(r"^[Hh][Tt][Tt][Pp]:\/\/", "", removed_https)

    return removed_http


def extract_urls() -> set[str]:
    """Extract fraudulent URLs found at www.ema.com.ua

    Returns:
        set[str]: Unique fraudulent URLs.
    """
    try:
        res: requests.Response = requests.get(
            "https://www.ema.com.ua/wp-json/api/blacklist-query?count=1000000",
            timeout=30,
        )
        res.raise_for_status()
        body = res.json()

        # Manual cleaning
        all_items = body.get("data", list())
        raw_urls = [x["url"].strip(" \t\v\n\r\f.") for x in all_items if "url" in x]
        lines = (re.sub("\\s+", " ", line) for line in raw_urls)
        urls = set(
            y
            for x in itertools.chain.from_iterable(line.split(" ") for line in lines)
            if (y := clean_url(x.strip(" \t\v\n\r\f."))) and y != "www"
        )

        return urls
    except Exception as error:
        logger.error(error)
        return set()


if __name__ == "__main__":
    urls: set[str] = extract_urls()
    ips: set[str] = set()
    non_ips: set[str] = set()
    fqdns: set[str] = set()
    if urls:
        for url in urls:
            res = tldextract.extract(url)
            domain, fqdn = res.domain, res.fqdn
            if domain and not fqdn:
                # Possible IPv4 Address
                try:
                    socket.inet_pton(socket.AF_INET, domain)
                    ips.add(domain)
                except socket.error:
                    # Is invalid URL and invalid IP -> skip
                    pass
            elif fqdn:
                non_ips.add(url)
                fqdns.add(fqdn)

    if not non_ips and not ips:
        logger.error("No content available for blocklists.")
    else:
        non_ips_timestamp: str = current_datetime_str()
        non_ips_filename = "urls.txt"
        with open(non_ips_filename, "w") as f:
            f.writelines("\n".join(sorted(non_ips)))
            logger.info(
                "%d non-IPs written to %s at %s",
                len(non_ips),
                non_ips_filename,
                non_ips_timestamp,
            )

        ips_timestamp: str = current_datetime_str()
        ips_filename = "ips.txt"
        with open(ips_filename, "w") as f:
            f.writelines("\n".join(sorted(ips, key=ipaddress.IPv4Address)))
            logger.info(
                "%d IPs written to %s at %s", len(ips), ips_filename, ips_timestamp
            )

        fqdns_timestamp: str = current_datetime_str()
        fqdns_filename = "urls-pihole.txt"
        with open(fqdns_filename, "w") as f:
            f.writelines("\n".join(sorted(fqdns)))
            logger.info(
                "%d FQDNs written to %s at %s",
                len(fqdns),
                fqdns_filename,
                fqdns_timestamp,
            )
