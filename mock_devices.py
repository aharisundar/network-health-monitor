"""
Mock Network Device Simulator
Simulates real device responses for testing Netmiko code
"""

import logging

logger = logging.getLogger(__name__)


class MockCiscoDevice:
    """Simulates Cisco IOS-XE device responses"""
    
    def __init__(self, hostname="catalyst-9300", ios_version="16.12.04"):
        self.hostname = hostname
        self.ios_version = ios_version
    
    def send_command(self, command):
        """Simulate device responding to commands"""
        
        if command == "show version":
            return f"""
Cisco IOS XE Software, Version 16.12.04
Cisco IOS Software [Amsterdam], Catalyst L3 Switch Software
Copyright (c) 1986-2020 by Cisco Systems, Inc.
Compiled Wed 04-Mar-20 20:59 PST by mcpre

ROM: IOS-XE ROMMON

{self.hostname} uptime is 45 days, 3 hours, 22 minutes
System returned to ROM by power-on
System image file is "bootflash:cat9k_iosxe.16.12.04.SPA.bin"
Last reload reason: PowerOn

License Level: network-advantage
License Type: Subscription
Next reload license Level: network-advantage

Smart Licensing Status: Registration Pending

Configuration register is 0x2102
            """
        
        elif command == "show processes cpu":
            return """
CPU utilization for five seconds: 45%; one minute: 42%; five minutes: 40%
            """
        
        elif command == "show memory":
            return """
Head  Of Free Memory    : 0x5C8D8B0
Tail  Of Free Memory    : 0x1000000
Free Memory             : 2080436 bytes (1MB)
            """
        
        elif command == "show interfaces brief":
            return """
Interface                      IP-Address      Status                Protocol
GigabitEthernet0/0/0           10.1.1.1        up                    up
GigabitEthernet0/0/1           unassigned      up                    up
GigabitEthernet0/0/2           unassigned      down                  down
GigabitEthernet0/0/3           unassigned      up                    up
            """
        
        else:
            return f"Unknown command: {command}"


class MockJuniperDevice:
    """Simulates Juniper JUNOS device responses"""
    
    def __init__(self, hostname="ex-switch-01"):
        self.hostname = hostname
    
    def send_command(self, command):
        """Simulate Juniper device responding"""
        
        if command == "show version":
            return """
Hostname: ex-switch-01
Model: ex9200-48x-6qsfp28
JUNOS Software Release [20.4R1]
Built on Mar 25 2020 21:21:23 UTC
Kernel Version 5.10.0
            """
        
        elif command == "show system uptime":
            return """
Current time: 2026-07-10 12:44:49 UTC
System booted: 2026-05-26 09:22:27 UTC (45 days, 3 hours, 22 minutes ago)
            """
        
        elif command == "request shell execute 'top -bn1 | grep Cpu'":
            return """
%Cpu(s): 38.0 us,  5.2 sy,  0.0 ni, 56.8 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
            """
        
        elif command == "show interfaces brief":
            return """
Interface               Admin Link Proto    Local                 Remote
ge-0/0/0                up    up   aenet    --> ge-0/0/1
ge-0/0/1                up    up   aenet    --> ge-0/0/0
ge-0/0/2                up    up
ge-0/0/3                down  down
            """
        
        else:
            return f"Unknown command: {command}"


class MockArubaDevice:
    """Simulates Aruba ArubaOS device responses"""
    
    def __init__(self, hostname="aruba-6300"):
        self.hostname = hostname
    
    def send_command(self, command):
        """Simulate Aruba device responding"""
        
        if command == "show system":
            return """
System Information
  System Name            : aruba-6300
  System Type            : Aruba 6300
  Serial Number          : ABC123DEF456
  System uptime          : 45 days 3 hours 22 minutes
  System time            : 2026-07-10 12:44:49 UTC
            """
        
        elif command == "show cpu":
            return """
CPU Utilization
  Current CPU           : 22%
  CPU 5-minute average  : 20%
            """
        
        elif command == "show memory":
            return """
Memory Information
  Total Memory          : 2048 MB
  Used Memory           : 780 MB (38%)
  Free Memory           : 1268 MB (62%)
            """
        
        elif command == "show interface brief":
            return """
Port     Name      Type      Status    Speed       Duplex
1/1                1G-Copper UP        1000 Mb/s   Full
1/2                1G-Copper UP        1000 Mb/s   Full
1/3                1G-Copper DOWN      Not connected
            """
        
        else:
            return f"Unknown command: {command}"


class MockAristaDevice:
    """Simulates Arista EOS device responses"""
    
    def __init__(self, hostname="arista-7050"):
        self.hostname = hostname
    
    def send_command(self, command):
        """Simulate Arista device responding"""
        
        if command == "show version":
            return """
Arista DCS-7050S
Uptime: 45 days, 3 hours, 22 minutes
System uptime: 45 days, 3 hours, 22 minutes
Software image version: 4.26.0
            """
        
        elif command == "show processes top":
            return """
CPU usage: 41%
Memory usage: 59%
            """
        
        elif command == "show interfaces status brief":
            return """
Port       Name             Status       Vlan       Duplex Speed Type
Et1                         connected    1          full   1000M EbraCommitted
Et2                         connected    1          full   1000M EbraCommitted
Et3                         notconnect   1          full   1000M EbraCommitted
            """
        
        else:
            return f"Unknown command: {command}"
