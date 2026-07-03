"""
Juniper Device Connector
Supports: EX, SRX
"""

from device_collector import BaseDeviceConnector
import logging

logger = logging.getLogger(__name__)


class JuniperConnector(BaseDeviceConnector):
    """Juniper-specific connector"""
    pass
