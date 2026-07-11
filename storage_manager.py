"""
Day 7: Storage Manager
Stores metrics and alerts in SQLite database for historical tracking
"""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class StorageManager:
    """Manage database storage for metrics and alerts"""
    
    def __init__(self, db_path="network_monitor.db"):
        """
        Initialize storage manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.metrics_stored = 0
        self.alerts_stored = 0
        
        self.init_database()
        logger.info(f"✅ Storage manager initialized with DB: {db_path}")
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    device TEXT NOT NULL,
                    vendor TEXT NOT NULL,
                    cpu_usage REAL,
                    memory_usage REAL,
                    uptime_days INTEGER,
                    interface_count INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    device TEXT NOT NULL,
                    alert_level TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    recommendation TEXT,
                    sent BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Interfaces table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interfaces (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device TEXT NOT NULL,
                    interface_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("✅ Database tables initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {str(e)}")
    
    def store_metrics(self, metrics):
        """
        Store device metrics in database
        
        Args:
            metrics: Metrics dict from MetricsParser
        
        Returns:
            bool: Success status
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO metrics 
                (timestamp, device, vendor, cpu_usage, memory_usage, uptime_days, interface_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                metrics.get('timestamp'),
                metrics.get('device'),
                metrics.get('vendor'),
                metrics.get('cpu_usage'),
                metrics.get('memory_usage'),
                metrics.get('uptime_days'),
                len(metrics.get('interfaces', {}))
            ))
            
            conn.commit()
            conn.close()
            
            self.metrics_stored += 1
            logger.info(f"✅ Metrics stored for {metrics.get('device')}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store metrics: {str(e)}")
            return False
    
    def store_alert(self, alert, device_name):
        """
        Store alert in database
        
        Args:
            alert: Alert dict from AlertGenerator
            device_name: Device name
        
        Returns:
            bool: Success status
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alerts
                (timestamp, device, alert_level, alert_type, message, recommendation, sent)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert.get('timestamp'),
                device_name,
                alert.get('level'),
                alert.get('type'),
                alert.get('message'),
                alert.get('recommendation'),
                0
            ))
            
            conn.commit()
            conn.close()
            
            self.alerts_stored += 1
            logger.info(f"✅ Alert stored for {device_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store alert: {str(e)}")
            return False
    
    def store_interface_status(self, device_name, interface_name, status):
        """
        Store interface status in database
        
        Args:
            device_name: Device name
            interface_name: Interface name
            status: Interface status (up/down)
        
        Returns:
            bool: Success status
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO interfaces
                (device, interface_name, status, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (
                device_name,
                interface_name,
                status,
                datetime.utcnow().isoformat() + "Z"
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Interface status stored: {device_name}/{interface_name} = {status}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store interface status: {str(e)}")
            return False
    
    def get_device_metrics(self, device_name, days=7):
        """
        Retrieve device metrics history
        
        Args:
            device_name: Device name
            days: Number of days to retrieve
        
        Returns:
            list: Historical metrics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, cpu_usage, memory_usage 
                FROM metrics 
                WHERE device = ? AND created_at >= datetime('now', '-' || ? || ' days')
                ORDER BY timestamp DESC
                LIMIT 100
            ''', (device_name, days))
            
            results = cursor.fetchall()
            conn.close()
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve metrics: {str(e)}")
            return []
    
    def get_device_alerts(self, device_name, days=7):
        """
        Retrieve device alerts history
        
        Args:
            device_name: Device name
            days: Number of days to retrieve
        
        Returns:
            list: Historical alerts
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, alert_level, alert_type, message
                FROM alerts
                WHERE device = ? AND created_at >= datetime('now', '-' || ? || ' days')
                ORDER BY timestamp DESC
                LIMIT 100
            ''', (device_name, days))
            
            results = cursor.fetchall()
            conn.close()
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve alerts: {str(e)}")
            return []
    
    def get_statistics(self):
        """
        Get database statistics
        
        Returns:
            dict: Statistics summary
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM metrics')
            metrics_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM alerts')
            alerts_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT device) FROM metrics')
            unique_devices = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM alerts WHERE alert_level = "CRITICAL"')
            critical_alerts = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_metrics': metrics_count,
                'total_alerts': alerts_count,
                'unique_devices': unique_devices,
                'critical_alerts': critical_alerts
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get statistics: {str(e)}")
            return {}
    
    def cleanup_old_data(self, days=30):
        """
        Delete old data from database
        
        Args:
            days: Delete records older than this many days
        
        Returns:
            bool: Success status
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM metrics 
                WHERE created_at < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            cursor.execute('''
                DELETE FROM alerts 
                WHERE created_at < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Cleaned up data older than {days} days")
            return True
            
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {str(e)}")
            return False
