import re

def eth_addr_is_valid(address):
    if not re.match('^0x[a-fA-F0-9]{40}$', address):
        match = False
    else:
        match = True
    return match
