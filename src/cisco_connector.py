"""
Cisco Device Connector
Supports: Catalyst, ASR, Nexus
"""

from device_collector import BaseDeviceConnector
import logging

logger = logging.getLogger(__name__)


class CiscoConnector(BaseDeviceConnector):
    """Cisco-specific connector"""
    pass
