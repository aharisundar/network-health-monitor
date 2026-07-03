"""
Metrics Processor Module
Processes raw device metrics into standardized format
"""

from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MetricsProcessor:
    """Process raw metrics from devices into standardized format"""

    def __init__(self):
        """Initialize metrics processor"""
        self.processed_metrics = []

    def process_device_metrics(self, device_name, vendor, cpu, memory, interfaces):
        """
        Process metrics from a device

        Args:
            device_name (str): Device name/identifier
            vendor (str): Device vendor (Cisco, Juniper, etc)
            cpu (float): CPU usage percentage
            memory (float): Memory usage percentage
            interfaces (dict): Interface statistics

        Returns:
            dict: Processed metrics in standardized format
        """

        processed = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "device": device_name,
            "vendor": vendor,
            "cpu_usage": cpu,
            "memory_usage": memory,
            "interfaces": interfaces,
            "status": "active"
        }

        logger.info(f"✅ Processed metrics for {device_name}")
        logger.debug(f"   CPU: {cpu}%, Memory: {memory}%")

        self.processed_metrics.append(processed)
        return processed

    def validate_metrics(self, metrics):
        """
        Validate metrics are in correct format

        Args:
            metrics (dict): Metrics to validate

        Returns:
            bool: True if valid, False otherwise
        """

        required_fields = ['timestamp', 'device', 'vendor', 'cpu_usage', 'memory_usage']

        for field in required_fields:
            if field not in metrics:
                logger.error(f"❌ Missing required field: {field}")
                return False

        # Validate ranges
        if not (0 <= metrics['cpu_usage'] <= 100):
            logger.error(f"❌ Invalid CPU usage: {metrics['cpu_usage']}")
            return False

        if not (0 <= metrics['memory_usage'] <= 100):
            logger.error(f"❌ Invalid memory usage: {metrics['memory_usage']}")
            return False

        return True

    def get_processed_metrics(self):
        """Get all processed metrics"""
        return self.processed_metrics
