"""
Device Collector Module
Connects to network devices via SSH and collects metrics
"""

from netmiko import ConnectHandler
import logging

logger = logging.getLogger(__name__)


class BaseDeviceConnector:
    """Base class for all vendor device connectors"""

    def __init__(self, host, username, password, device_type, timeout=10):
        """
        Initialize device connector

        Args:
            host (str): Device IP address
            username (str): SSH username
            password (str): SSH password
            device_type (str): Device type (cisco_ios, juniper_junos, etc)
            timeout (int): SSH timeout in seconds
        """
        self.host = host
        self.username = username
        self.password = password
        self.device_type = device_type
        self.timeout = timeout
        self.connection = None
        self.vendor = None

    def connect(self):
        """Establish SSH connection to device"""
        try:
            self.connection = ConnectHandler(
                device_type=self.device_type,
                host=self.host,
                username=self.username,
                password=self.password,
                timeout=self.timeout
            )
            logger.info(f"✅ Connected to {self.vendor} device: {self.host}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to {self.host}: {str(e)}")
            return False

    def disconnect(self):
        """Close SSH connection"""
        if self.connection:
            self.connection.disconnect()
            logger.info(f"✅ Disconnected from {self.host}")

    def send_command(self, command):
        """Send command to device and return output"""
        if not self.connection:
            logger.error("Not connected to device")
            return None

        try:
            output = self.connection.send_command(command)
            return output
        except Exception as e:
            logger.error(f"Failed to send command: {str(e)}")
            return None

    def get_cpu_usage(self):
        """Get CPU usage - to be implemented in subclass"""
        raise NotImplementedError("Subclass must implement get_cpu_usage()")

    def get_memory_usage(self):
        """Get memory usage - to be implemented in subclass"""
        raise NotImplementedError("Subclass must implement get_memory_usage()")

    def get_interface_stats(self):
        """Get interface statistics - to be implemented in subclass"""
        raise NotImplementedError("Subclass must implement get_interface_stats()")


class CiscoConnector(BaseDeviceConnector):
    """Connector for Cisco devices"""

    def __init__(self, host, username, password, device_type='cisco_ios', timeout=10):
        super().__init__(host, username, password, device_type, timeout)
        self.vendor = "Cisco"

    def get_cpu_usage(self):
        """Get CPU usage from Cisco device"""
        logger.info(f"Collecting CPU metrics from {self.host}")
        # Placeholder - will be implemented in Week 2
        return 45.2

    def get_memory_usage(self):
        """Get memory usage from Cisco device"""
        logger.info(f"Collecting memory metrics from {self.host}")
        # Placeholder - will be implemented in Week 2
        return 62.8

    def get_interface_stats(self):
        """Get interface statistics from Cisco device"""
        logger.info(f"Collecting interface stats from {self.host}")
        # Placeholder - will be implemented in Week 2
        return {"Gi0/0/1": {"state": "up", "utilization": 35.2}}


class JuniperConnector(BaseDeviceConnector):
    """Connector for Juniper devices"""

    def __init__(self, host, username, password, device_type='juniper_junos', timeout=10):
        super().__init__(host, username, password, device_type, timeout)
        self.vendor = "Juniper"

    def get_cpu_usage(self):
        """Get CPU usage from Juniper device"""
        logger.info(f"Collecting CPU metrics from {self.host}")
        return 38.5

    def get_memory_usage(self):
        """Get memory usage from Juniper device"""
        logger.info(f"Collecting memory metrics from {self.host}")
        return 55.3

    def get_interface_stats(self):
        """Get interface statistics from Juniper device"""
        logger.info(f"Collecting interface stats from {self.host}")
        return {"ge-0/0/0": {"state": "up", "utilization": 42.1}}


class ArubaConnector(BaseDeviceConnector):
    """Connector for Aruba devices"""

    def __init__(self, host, username, password, device_type='aruba_os', timeout=10):
        super().__init__(host, username, password, device_type, timeout)
        self.vendor = "Aruba"

    def get_cpu_usage(self):
        """Get CPU usage from Aruba device"""
        logger.info(f"Collecting CPU metrics from {self.host}")
        return 41.2

    def get_memory_usage(self):
        """Get memory usage from Aruba device"""
        logger.info(f"Collecting memory metrics from {self.host}")
        return 58.7

    def get_interface_stats(self):
        """Get interface statistics from Aruba device"""
        logger.info(f"Collecting interface stats from {self.host}")
        return {"1/1": {"state": "up", "utilization": 28.5}}


class AristaConnector(BaseDeviceConnector):
    """Connector for Arista devices"""

    def __init__(self, host, username, password, device_type='arista_eos', timeout=10):
        super().__init__(host, username, password, device_type, timeout)
        self.vendor = "Arista"

    def get_cpu_usage(self):
        """Get CPU usage from Arista device"""
        logger.info(f"Collecting CPU metrics from {self.host}")
        return 39.8

    def get_memory_usage(self):
        """Get memory usage from Arista device"""
        logger.info(f"Collecting memory metrics from {self.host}")
        return 60.2

    def get_interface_stats(self):
        """Get interface statistics from Arista device"""
        logger.info(f"Collecting interface stats from {self.host}")
        return {"Ethernet1": {"state": "up", "utilization": 31.5}}
