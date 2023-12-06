#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    # Parse command-line arguments
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    
    # Check if required arguments are provided
    if not options.interface:
        # Error handling when interface is missing
        parser.error("[+] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        # Error handling when MAC address is missing
        parser.error("[+] Please specify a MAC address, use --help for more info")
    return options

def change_mac(interface, new_mac):
    # Function to change the MAC address of the specified interface
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    
    # Use subprocess to execute Linux commands to change the MAC address
    subprocess.call(["ip", "link", "set", interface, "down"])
    subprocess.call(["ip", "link", "set", "dev", interface, "address", new_mac])
    subprocess.call(["ip", "link", "set", interface, "up"])

def get_current_mac(interface):
    # Function to retrieve the current MAC address of the specified interface
    ifconfig_result = subprocess.check_output(["ip", "link", "show", interface]).decode('utf-8')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        # Error handling if MAC address cannot be read
        print("[+] Could not read MAC address")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[+] MAC address did not get changed.")
