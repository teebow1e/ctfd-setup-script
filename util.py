import re

PROXIES = {
    'http': '192.168.1.1:8080',
    'https': '192.168.1.1:8080'
}

CSRF_REGEX = re.compile(r"'csrfNonce': *\"([a-fA-F0-9]*)\"")