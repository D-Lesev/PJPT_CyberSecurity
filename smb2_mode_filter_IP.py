#!/usr/bin/python3

"""
This script focuses on identifying potential vulnerabilities associated with SMB Relay attacks on IPs,
where SMB signing is enabled but not mandatory. It effectively filters IPs from a context file,
which should be generated using Nmap.
"""

import re
import argparse
import time


def get_argument():
    """
    define the supplied parameter
    :return: file
    """
    parser = argparse.ArgumentParser(description="Get file with the IP from nmap scan")
    parser.add_argument("-f", "--file", dest="text_file", help="Provide the file with the scan IP from nmap")

    file_IP = parser.parse_args()

    if not file_IP.text_file:
        parser.error("[-] Provide the file with IPs")

    return file_IP


def find_ip(file):
    """
    The supplied file is being filtered only for IPs
    :param file: file from Nmap
    :return: list with all IPs
    """
    reg_ip = r"([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})"

    with open(file, "r") as f:
        print("[+] Reading the given file")
        content = f.read()

    ips = re.findall(reg_ip, content, re.MULTILINE)

    if ips:
        return ips
    else:
        print("[-] No possible IPs found !!")
        exit()


def write_ips(ips):
    """
    Writing the IPs to a new file
    :param ips: list with IPs
    """
    with open("result_nmap.txt", "w") as f2:
        print("[+] Writing IPs to file")
        time.sleep(1)

        f2.write(str('\n'.join(ip for ip in ips)))

        print("[+] Done!! You can open file 'result_nmap.txt'")


def main():
    file = get_argument()
    ip_addr = find_ip(file.text_file)
    write_ips(ip_addr)


main()
