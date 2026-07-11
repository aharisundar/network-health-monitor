"""
Day 6: Alert Generator
Generates actionable alerts from detected anomalies
"""

import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class AlertGenerator:
    """Generate alerts from anomalies"""
    
    def __init__(self, slack_webhook_url=None, email_address=None):
        """
        Initialize alert generator
        
        Args:
            slack_webhook_url: Slack incoming webhook URL
            email_address: Email for alert notifications
        """
        self.slack_webhook_url = slack_webhook_url
        self.email_address = email_address
        self.alerts_generated = 0
        self.alerts_sent = 0
        
        logger.info("✅ Alert generator initialized")
    
    def format_slack_message(self, anomaly, device_name, metric_type, value, threshold):
        """Format anomaly as Slack message"""
        
        severity_emoji = {
            3: "🚨",  # Critical
            2: "⚠️",   # Warning
            0: "✅"    # OK
        }
        
        message = {
            "text": f"{severity_emoji.get(3, '⚠️')} Network Alert: {device_name}",
            "attachments": [
                {
                    "color": "danger" if anomaly.get('level') == 'CRITICAL' else "warning",
                    "fields": [
                        {"title": "Device", "value": device_name, "short": True},
                        {"title": "Alert Level", "value": anomaly.get('level'), "short": True},
                        {"title": "Metric", "value": metric_type, "short": True},
                        {"title": "Current Value", "value": f"{value}%", "short": True},
                        {"title": "Threshold", "value": f"{threshold}%", "short": True},
                        {"title": "Message", "value": anomaly.get('message'), "short": False},
                        {"title": "Recommendation", "value": anomaly.get('recommendation'), "short": False},
                        {"title": "Timestamp", "value": datetime.utcnow().isoformat() + "Z", "short": True}
                    ]
                }
            ]
        }
        
        return message
    
    def format_email_message(self, anomaly, device_name):
        """Format anomaly as email message"""
        
        subject = f"[{anomaly.get('level')}] Network Alert: {device_name}"
        
        body = f"""
Network Health Alert
====================

Device: {device_name}
Alert Level: {anomaly.get('level')}
Message: {anomaly.get('message')}
Recommendation: {anomaly.get('recommendation')}
Timestamp: {datetime.utcnow().isoformat() + "Z"}

Please investigate immediately.

---
Network Health Monitor
        """
        
        return {"subject": subject, "body": body}
    
    def send_slack_alert(self, anomaly, device_name, metric_type, value, threshold):
        """Send alert via Slack"""
        
        if not self.slack_webhook_url:
            logger.warning("⚠️ Slack webhook not configured")
            return False
        
        try:
            message = self.format_slack_message(anomaly, device_name, metric_type, value, threshold)
            
            logger.info(f"📤 Sending Slack alert for {device_name}")
            logger.info(f"   Level: {anomaly.get('level')}")
            logger.info(f"   Message: {anomaly.get('message')}")
            
            # In real implementation, would use requests library
            # response = requests.post(self.slack_webhook_url, json=message)
            
            self.alerts_sent += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send Slack alert: {str(e)}")
            return False
    
    def send_email_alert(self, anomaly, device_name):
        """Send alert via email"""
        
        if not self.email_address:
            logger.warning("⚠️ Email not configured")
            return False
        
        try:
            message = self.format_email_message(anomaly, device_name)
            
            logger.info(f"📧 Sending email alert to {self.email_address}")
            logger.info(f"   Subject: {message['subject']}")
            
            # In real implementation, would use smtplib
            # smtp = smtplib.SMTP()
            # smtp.send_message(message)
            
            self.alerts_sent += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send email alert: {str(e)}")
            return False
    
    def generate_alert(self, anomalies, device_name, vendor):
        """
        Generate alerts from detected anomalies
        
        Args:
            anomalies: List of anomalies from detector
            device_name: Name of device
            vendor: Vendor type
        
        Returns:
            list: Generated alerts
        """
        
        alerts = []
        
        if not anomalies:
            return alerts
        
        logger.info(f"\n🔔 Generating alerts for {device_name}...")
        
        for anomaly in anomalies:
            if anomaly.get('level') in ['WARNING', 'CRITICAL']:
                
                alert = {
                    'timestamp': datetime.utcnow().isoformat() + "Z",
                    'device': device_name,
                    'vendor': vendor,
                    'alert_type': anomaly.get('type', 'unknown'),
                    'level': anomaly.get('level'),
                    'message': anomaly.get('message'),
                    'recommendation': anomaly.get('recommendation'),
                    'sent': False
                }
                
                alerts.append(alert)
                self.alerts_generated += 1
                
                logger.info(f"  ✅ Alert generated:")
                logger.info(f"     Type: {anomaly.get('type')}")
                logger.info(f"     Level: {anomaly.get('level')}")
                logger.info(f"     Message: {anomaly.get('message')}")
        
        return alerts
    
    def process_anomalies_and_alert(self, detector_output, device_name, vendor):
        """
        Process anomalies and send alerts
        
        Args:
            detector_output: Output from anomaly detector
            device_name: Device name
            vendor: Vendor type
        """
        
        logger.info(f"\n🔔 ALERT PROCESSING FOR {device_name}")
        logger.info("="*70)
        
        alerts = detector_output.get('alerts', [])
        
        if not alerts:
            logger.info(f"✅ No alerts to process for {device_name}")
            return
        
        logger.info(f"📊 Processing {len(alerts)} alert(s)...")
        
        for alert in alerts:
            if alert.get('level') in ['WARNING', 'CRITICAL']:
                logger.info(f"\n  🚨 {alert.get('level')} - {alert.get('message')}")
                
                # In real implementation, would send via Slack/Email
                if self.slack_webhook_url:
                    self.send_slack_alert(
                        alert, 
                        device_name,
                        alert.get('type'),
                        alert.get('severity', 'N/A'),
                        'threshold'
                    )
                
                if self.email_address:
                    self.send_email_alert(alert, device_name)
        
        logger.info("\n✅ Alert processing complete")
    
    def get_summary(self):
        """Get alert summary"""
        return {
            'alerts_generated': self.alerts_generated,
            'alerts_sent': self.alerts_sent
        }
