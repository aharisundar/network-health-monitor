"""
Day 4: Metrics Parser & Processor
Transforms raw device output into structured metrics
"""

import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class MetricsParser:
    """Parse and normalize metrics from different vendors"""
    
    @staticmethod
    def parse_cisco_metrics(device_name, output_dict):
        """
        Parse Cisco device outputs into structured metrics
        
        Args:
            device_name: Name of device
            output_dict: Dict with device outputs like:
                {
                    'show version': '...',
                    'show processes cpu': '...',
                    'show interfaces brief': '...'
                }
        """
        
        metrics = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "device": device_name,
            "vendor": "cisco",
            "cpu_usage": None,
            "memory_usage": None,
            "uptime_days": None,
            "interfaces": {},
            "status": "unknown"
        }
        
        try:
            # Parse CPU from "show processes cpu"
            cpu_output = output_dict.get('show processes cpu', '')
            if 'CPU utilization' in cpu_output:
                # Extract: "45%; one minute: 42%; five minutes: 40%"
                for line in cpu_output.split('\n'):
                    if 'CPU utilization for five seconds' in line:
                        cpu_str = line.split(':')[1].split(';')[0].strip().rstrip('%')
                        metrics['cpu_usage'] = float(cpu_str)
                        break
            
            # Parse uptime from "show version"
            version_output = output_dict.get('show version', '')
            if 'uptime is' in version_output:
                for line in version_output.split('\n'):
                    if 'uptime is' in line:
                        # Extract: "45 days, 3 hours, 22 minutes"
                        if 'days' in line:
                            days_str = line.split('uptime is')[1].split('days')[0].strip()
                            metrics['uptime_days'] = int(days_str)
                        break
            
            # Parse interfaces from "show interfaces brief"
            int_output = output_dict.get('show interfaces brief', '')
            interface_count = 0
            up_count = 0
            for line in int_output.split('\n'):
                if 'GigabitEthernet' in line or 'Ethernet' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        interface_name = parts[0]
                        status = parts[-2] if len(parts) >= 2 else 'unknown'
                        
                        metrics['interfaces'][interface_name] = {
                            "status": status,
                            "description": None
                        }
                        interface_count += 1
                        if status == 'up':
                            up_count += 1
            
            if interface_count > 0:
                metrics['status'] = 'active'
            
            logger.info(f"✅ Parsed Cisco metrics for {device_name}")
            logger.debug(f"   CPU: {metrics['cpu_usage']}%, Interfaces: {interface_count}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error parsing Cisco metrics: {str(e)}")
            return metrics
    
    
    @staticmethod
    def parse_juniper_metrics(device_name, output_dict):
        """Parse Juniper device outputs into structured metrics"""
        
        metrics = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "device": device_name,
            "vendor": "juniper",
            "cpu_usage": None,
            "memory_usage": None,
            "uptime_days": None,
            "interfaces": {},
            "status": "unknown"
        }
        
        try:
            # Parse uptime from "show system uptime"
            uptime_output = output_dict.get('show system uptime', '')
            if 'System booted' in uptime_output:
                for line in uptime_output.split('\n'):
                    if 'System booted' in line and 'days' in line:
                        days_str = line.split('(')[1].split('days')[0].strip()
                        metrics['uptime_days'] = int(days_str)
                        break
            
            # Parse CPU from top command
            top_output = output_dict.get("request shell execute 'top -bn1 | grep Cpu'", '')
            if '%Cpu(s)' in top_output:
                for line in top_output.split('\n'):
                    if '%Cpu(s)' in line:
                        # Extract CPU idle percentage and calculate usage
                        parts = line.split(',')
                        for part in parts:
                            if 'id' in part:
                                idle = float(part.split()[0])
                                metrics['cpu_usage'] = 100 - idle
                                break
            
            # Parse interfaces from "show interfaces brief"
            int_output = output_dict.get('show interfaces brief', '')
            interface_count = 0
            for line in int_output.split('\n'):
                if 'ge-' in line or 'xe-' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        interface_name = parts[0]
                        admin_status = parts[1] if len(parts) > 1 else 'unknown'
                        link_status = parts[2] if len(parts) > 2 else 'unknown'
                        
                        metrics['interfaces'][interface_name] = {
                            "admin": admin_status,
                            "link": link_status
                        }
                        interface_count += 1
            
            if interface_count > 0:
                metrics['status'] = 'active'
            
            logger.info(f"✅ Parsed Juniper metrics for {device_name}")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error parsing Juniper metrics: {str(e)}")
            return metrics
    
    
    @staticmethod
    def parse_aruba_metrics(device_name, output_dict):
        """Parse Aruba device outputs into structured metrics"""
        
        metrics = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "device": device_name,
            "vendor": "aruba",
            "cpu_usage": None,
            "memory_usage": None,
            "uptime_days": None,
            "interfaces": {},
            "status": "unknown"
        }
        
        try:
            # Parse CPU from "show cpu"
            cpu_output = output_dict.get('show cpu', '')
            if 'Current CPU' in cpu_output:
                for line in cpu_
