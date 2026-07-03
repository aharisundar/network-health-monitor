"""
Alerter Module
Sends alerts via multiple channels (Slack, Email, etc)
"""

import logging

logger = logging.getLogger(__name__)


class Alerter:
    """Send alerts to multiple channels"""
    
    def __init__(self, slack_webhook_url=None, email_recipients=None):
        """
        Initialize alerter
        
        Args:
            slack_webhook_url (str): Slack webhook URL
            email_recipients (list): Email recipients
        """
        
        self.slack_webhook_url = slack_webhook_url
        self.email_recipients = email_recipients or []
        
        logger.info("✅ Alerter initialized")
    
    def send_slack_alert(self, device, anomalies):
        """
        Send alert to Slack
        
        Args:
            device (str): Device name
            anomalies (dict): Anomaly details
        """
        
        if not self.slack_webhook_url:
            logger.debug("Slack webhook not configured, skipping")
            return
        
        message = f"🚨 Alert from {device}\n"
        for alert in anomalies.get('alerts', []):
            message += f"  • {alert.get('message', 'Unknown alert')}\n"
        
        logger.info(f"📤 Sending Slack alert: {message}")
        
        # TODO: Week 3 - Implement actual Slack API call
        # import requests
        # requests.post(self.slack_webhook_url, json={"text": message})
    
    def send_email_alert(self, device, anomalies):
        """
        Send alert via email
        
        Args:
            device (str): Device name
            anomalies (dict): Anomaly details
        """
        
        if not self.email_recipients:
            logger.debug("Email recipients not configured, skipping")
            return
        
        subject = f"🚨 Network Alert: {device}"
        body = f"Anomalies detected on {device}:\n"
        
        for alert in anomalies.get('alerts', []):
            body += f"  • {alert.get('message', 'Unknown alert')}\n"
        
        logger.info(f"📧 Sending email alert to {len(self.email_recipients)} recipients")
        
        # TODO: Week 3 - Implement actual SMTP sending
    
    def send_alert(self, device, anomalies):
        """
        Send alert via all configured channels
        
        Args:
            device (str): Device name
            anomalies (dict): Anomaly details
        """
        
        if not anomalies.get('alerts'):
            return
        
        logger.warning(f"🚨 Sending alerts for {device}")
        
        self.send_slack_alert(device, anomalies)
        self.send_email_alert(device, anomalies)
