try:
    from future_builtins import filter
except ImportError:
    pass  # Neither available nor necessary on Python 3.
import subprocess
import xml.etree.ElementTree as ET


MAC_ADDRESS = 'CC:3A:61:61:D4:63'
IP_RANGE = '192.168.20.1-110'


def scan_for_hosts(ip_range):
    """Scan the given IP address range using Nmap and return the result
    in XML format.
    """
    nmap_args = ['nmap', '-n', '-sP', '-oX', '-', ip_range]
    return subprocess.check_output(nmap_args)

def find_ip_address_for_mac_address(xml, mac_address):
    """Parse Nmap's XML output, find the host element with the given
    MAC address, and return that host's IP address.
    """
    hosts = ET.fromstring(xml).iter('host')
    host = next(filter(host_has_mac_address, hosts))
    return get_ip_address(host)

def host_has_mac_address(host_elem):
    """Return true if the host has the given MAC address."""
    mac_address_found = get_address_of_type(host_elem, 'mac')
    return mac_address_found.lower() == MAC_ADDRESS.lower()

def get_ip_address(host_elem):
    """Return the host's IP address."""
    return get_address_of_type(host_elem, 'ipv4')

def get_address_of_type(host_elem, type_):
    """Return the host's address of the given type."""
    return host_elem.find('./address[@addrtype="%s"]' % type_).get('addr')

xml = scan_for_hosts(IP_RANGE)
ip_address = find_ip_address_for_mac_address(xml, MAC_ADDRESS)
print('Found IP address %s for MAC address %s.' % (ip_address, MAC_ADDRESS))
