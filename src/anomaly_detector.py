"""
Anomaly Detector Module
Detects anomalies in device metrics using threshold-based detection
"""

import logging

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detect anomalies in network device metrics"""
    
    def __init__(self, cpu_warning=75, cpu_critical=90, 
                 memory_warning=75, memory_critical=85,
                 interface_warning=70, interface_critical=85):
        """
        Initialize anomaly detector with thresholds
        
        Args:
            cpu_warning (float): CPU warning threshold %
            cpu_critical (float): CPU critical threshold %
            memory_warning (float): Memory warning threshold %
            memory_critical (float): Memory critical threshold %
            interface_warning (float): Interface warning threshold %
            interface_critical (float): Interface critical threshold %
        """
        
        self.thresholds = {
            'cpu': {'warning': cpu_warning, 'critical': cpu_critical},
            'memory': {'warning': memory_warning, 'critical': memory_critical},
            'interface': {'warning': interface_warning, 'critical': interface_critical}
        }
        
        logger.info("✅ Anomaly detector initialized with thresholds")
        logger.debug(f"   CPU: {cpu_warning}% warn, {cpu_critical}% critical")
        logger.debug(f"   Memory: {memory_warning}% warn, {memory_critical}% critical")
    
    def check_cpu(self, cpu_usage):
        """Check if CPU usage is abnormal"""
        if cpu_usage >= self.thresholds['cpu']['critical']:
            return {'level': 'CRITICAL', 'message': f'CPU at {cpu_usage}% (critical)'}
        elif cpu_usage >= self.thresholds['cpu']['warning']:
            return {'level': 'WARNING', 'message': f'CPU at {cpu_usage}% (warning)'}
        else:
            return {'level': 'OK', 'message': f'CPU at {cpu_usage}% (normal)'}
    
    def check_memory(self, memory_usage):
        """Check if memory usage is abnormal"""
        if memory_usage >= self.thresholds['memory']['critical']:
            return {'level': 'CRITICAL', 'message': f'Memory at {memory_usage}% (critical)'}
        elif memory_usage >= self.thresholds['memory']['warning']:
            return {'level': 'WARNING', 'message': f'Memory at {memory_usage}% (warning)'}
        else:
            return {'level': 'OK', 'message': f'Memory at {memory_usage}% (normal)'}
    
    def check_interfaces(self, interfaces):
        """Check if any interface utilization is abnormal"""
        alerts = []
        
        for interface, stats in interfaces.items():
            utilization = stats.get('utilization', 0)
            
            if utilization >= self.thresholds['interface']['critical']:
                alerts.append({
                    'interface': interface,
                    'level': 'CRITICAL',
                    'utilization': utilization,
                    'message': f'{interface} at {utilization}% (critical)'
                })
            elif utilization >= self.thresholds['interface']['warning']:
                alerts.append({
                    'interface': interface,
                    'level': 'WARNING',
                    'utilization': utilization,
                    'message': f'{interface} at {utilization}% (warning)'
                })
        
        return alerts
    
    def detect_anomalies(self, metrics):
        """
        Detect all anomalies in device metrics
        
        Args:
            metrics (dict): Device metrics to check
        
        Returns:
            dict: Anomalies found (if any)
        """
        
        anomalies = {
            'device': metrics.get('device'),
            'timestamp': metrics.get('timestamp'),
            'alerts': []
        }
        
        # Check CPU
        cpu_alert = self.check_cpu(metrics.get('cpu_usage', 0))
        if cpu_alert['level'] != 'OK':
            anomalies['alerts'].append(cpu_alert)
            logger.warning(f"⚠️ {cpu_alert['message']}")
        
        # Check Memory
        memory_alert = self.check_memory(metrics.get('memory_usage', 0))
        if memory_alert['level'] != 'OK':
            anomalies['alerts'].append(memory_alert)
            logger.warning(f"⚠️ {memory_alert['message']}")
        
        # Check Interfaces
        interface_alerts = self.check_interfaces(metrics.get('interfaces', {}))
        if interface_alerts:
            anomalies['alerts'].extend(interface_alerts)
            for alert in interface_alerts:
                logger.warning(f"⚠️ {alert['message']}")
        
        if anomalies['alerts']:
            logger.error(f"🚨 {len(anomalies['alerts'])} anomalies detected!")
        
        return anomalies
