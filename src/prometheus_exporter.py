"""
Prometheus Exporter Module
Export metrics in Prometheus format
"""

from prometheus_client import Counter, Gauge, Histogram
import logging

logger = logging.getLogger(__name__)

# Define Prometheus metrics
device_cpu_usage = Gauge('device_cpu_usage_percent', 'CPU usage percentage', ['device', 'vendor'])
device_memory_usage = Gauge('device_memory_usage_percent', 'Memory usage percentage', ['device', 'vendor'])
interface_utilization = Gauge('interface_utilization_percent', 'Interface utilization', ['device', 'interface', 'vendor'])

metrics_collected = Counter('metrics_collected_total', 'Total metrics collected', ['vendor'])
metrics_errors = Counter('metrics_errors_total', 'Total metrics collection errors', ['vendor'])


def export_device_metrics(device_name, vendor, cpu, memory, interfaces):
    """
    Export device metrics to Prometheus
    
    Args:
        device_name (str): Device name
        vendor (str): Device vendor
        cpu (float): CPU usage %
        memory (float): Memory usage %
        interfaces (dict): Interface stats
    """
    
    try:
        device_cpu_usage.labels(device=device_name, vendor=vendor).set(cpu)
        device_memory_usage.labels(device=device_name, vendor=vendor).set(memory)
        
        for interface, stats in interfaces.items():
            utilization = stats.get('utilization', 0)
            interface_utilization.labels(device=device_name, interface=interface, vendor=vendor).set(utilization)
        
        metrics_collected.labels(vendor=vendor).inc()
        logger.info(f"✅ Exported metrics for {device_name}")
        
    except Exception as e:
        metrics_errors.labels(vendor=vendor).inc()
        logger.error(f"❌ Failed to export metrics: {str(e)}")
