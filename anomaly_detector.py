"""
Day 5: Anomaly Detection Engine
Detects when metrics cross thresholds and triggers alerts
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detect anomalies in network device metrics"""
    
    def __init__(self, cpu_warning=75, cpu_critical=90,
                 memory_warning=75, memory_critical=85,
                 interface_warning=70, interface_critical=85):
        """
        Initialize anomaly detector with thresholds
        
        Args:
            cpu_warning: CPU warning threshold %
            cpu_critical: CPU critical threshold %
            memory_warning: Memory warning threshold %
            memory_critical: Memory critical threshold %
        """
        
        self.thresholds = {
            'cpu': {'warning': cpu_warning, 'critical': cpu_critical},
            'memory': {'warning': memory_warning, 'critical': memory_critical},
            'interface': {'warning': interface_warning, 'critical': interface_critical}
        }
        
        logger.info("✅ Anomaly detector initialized")
        logger.debug(f"   CPU: {cpu_warning}% warn, {cpu_critical}% critical")
        logger.debug(f"   Memory: {memory_warning}% warn, {memory_critical}% critical")
    
    def check_cpu(self, cpu_usage):
        """Check if CPU usage is abnormal"""
        if cpu_usage is None:
            return {'level': 'UNKNOWN', 'message': 'CPU data unavailable'}
        
        if cpu_usage >= self.thresholds['cpu']['critical']:
            return {
                'level': 'CRITICAL',
                'severity': 3,
                'message': f'CPU at {cpu_usage:.1f}% (critical threshold: {self.thresholds["cpu"]["critical"]}%)',
                'recommendation': 'Investigate high CPU processes immediately'
            }
        elif cpu_usage >= self.thresholds['cpu']['warning']:
            return {
                'level': 'WARNING',
                'severity': 2,
                'message': f'CPU at {cpu_usage:.1f}% (warning threshold: {self.thresholds["cpu"]["warning"]}%)',
                'recommendation': 'Monitor CPU trending'
            }
        else:
            return {
                'level': 'OK',
                'severity': 0,
                'message': f'CPU at {cpu_usage:.1f}% (normal)',
                'recommendation': None
            }
    
    def check_memory(self, memory_usage):
        """Check if memory usage is abnormal"""
        if memory_usage is None:
            return {'level': 'UNKNOWN', 'message': 'Memory data unavailable'}
        
        if memory_usage >= self.thresholds['memory']['critical']:
            return {
                'level': 'CRITICAL',
                'severity': 3,
                'message': f'Memory at {memory_usage:.1f}% (critical threshold: {self.thresholds["memory"]["critical"]}%)',
                'recommendation': 'Clear memory or restart device'
            }
        elif memory_usage >= self.thresholds['memory']['warning']:
            return {
                'level': 'WARNING',
                'severity': 2,
                'message': f'Memory at {memory_usage:.1f}% (warning threshold: {self.thresholds["memory"]["warning"]}%)',
                'recommendation': 'Monitor memory usage'
            }
        else:
            return {
                'level': 'OK',
                'severity': 0,
                'message': f'Memory at {memory_usage:.1f}% (normal)',
                'recommendation': None
            }
    
    def check_interfaces(self, interfaces):
        """Check if any interface is down"""
        alerts = []
        
        if not interfaces:
            return alerts
        
        for interface_name, interface_data in interfaces.items():
            status = interface_data.get('status', 'unknown')
            
            if status == 'down':
                alerts.append({
                    'interface': interface_name,
                    'level': 'CRITICAL',
                    'severity': 3,
                    'message': f'{interface_name} is DOWN',
                    'recommendation': 'Check physical connection and configuration'
                })
            elif status == 'up':
                alerts.append({
                    'interface': interface_name,
                    'level': 'OK',
                    'severity': 0,
                    'message': f'{interface_name} is UP',
                    'recommendation': None
                })
        
        return alerts
    
    def detect_anomalies(self, metrics):
        """
        Detect all anomalies in device metrics
        
        Args:
            metrics: Device metrics dict from MetricsParser
        
        Returns:
            dict: Anomalies found with alerts
        """
        
        anomalies = {
            'device': metrics.get('device'),
            'vendor': metrics.get('vendor'),
            'timestamp': datetime.utcnow().isoformat() + "Z",
            'alerts': [],
            'severity': 0
        }
        
        logger.info(f"\n🔍 Checking anomalies for {metrics.get('device')}...")
        
        # Check CPU
        cpu_check = self.check_cpu(metrics.get('cpu_usage'))
        if cpu_check['level'] != 'OK':
            anomalies['alerts'].append({
                'type': 'cpu',
                **cpu_check
            })
            anomalies['severity'] = max(anomalies['severity'], cpu_check.get('severity', 0))
            logger.warning(f"⚠️  {cpu_check['message']}")
        
        # Check Memory
        memory_check = self.check_memory(metrics.get('memory_usage'))
        if memory_check['level'] != 'OK':
            anomalies['alerts'].append({
                'type': 'memory',
                **memory_check
            })
            anomalies['severity'] = max(anomalies['severity'], memory_check.get('severity', 0))
            logger.warning(f"⚠️  {memory_check['message']}")
        
        # Check Interfaces
        interface_alerts = self.check_interfaces(metrics.get('interfaces', {}))
        for alert in interface_alerts:
            if alert['level'] != 'OK':
                anomalies['alerts'].append(alert)
                anomalies['severity'] = max(anomalies['severity'], alert.get('severity', 0))
                logger.warning(f"⚠️  {alert['message']}")
        
        # Summary
        if anomalies['alerts']:
            logger.error(f"🚨 {len(anomalies['alerts'])} anomalies detected for {metrics.get('device')}!")
        else:
            logger.info(f"✅ No anomalies detected for {metrics.get('device')}")
        
        return anomalies
