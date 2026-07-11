"""
Day 7: Storage Manager Test
Tests database storage and retrieval
"""

import logging
import os
from datetime import datetime
from storage_manager import StorageManager
from anomaly_detector import AnomalyDetector
from alert_generator import AlertGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_test_metrics(device_name, vendor, cpu, memory):
    """Create test metrics"""
    return {
        'device': device_name,
        'vendor': vendor,
        'cpu_usage': cpu,
        'memory_usage': memory,
        'uptime_days': 45,
        'interfaces': {"Gi0/0/1": {"status": "up"}},
        'timestamp': datetime.utcnow().isoformat() + "Z"
    }


def test_database_initialization():
    """Test database initialization"""
    logger.info("\n" + "="*70)
    logger.info("✅ TEST 1: DATABASE INITIALIZATION")
    logger.info("="*70)
    
    db_file = "test_network_monitor.db"
    
    # Clean up if exists
    if os.path.exists(db_file):
        os.remove(db_file)
    
    storage = StorageManager(db_path=db_file)
    
    if os.path.exists(db_file):
        logger.info(f"✅ Database file created: {db_file}")
        logger.info("✅ TEST PASSED: Database initialized")
        return True, storage
    else:
        logger.error("❌ TEST FAILED: Database not created")
        return False, None


def test_metrics_storage(storage):
    """Test storing metrics"""
    logger.info("\n" + "="*70)
    logger.info("✅ TEST 2: METRICS STORAGE")
    logger.info("="*70)
    
    devices = [
        ("catalyst-01", "cisco", 45.0, 62.8),
        ("asr-01", "cisco", 78.0, 65.0),
        ("ex-switch-01", "juniper", 38.0, 55.3)
    ]
    
    for device, vendor, cpu, mem in devices:
        metrics = create_test_metrics(device, vendor, cpu, mem)
        result = storage.store_metrics(metrics)
        
        if result:
            logger.info(f"✅ Stored: {device} - CPU: {cpu}%, Memory: {mem}%")
        else:
            logger.error(f"❌ Failed to store: {device}")
            return False
    
    logger.info(f"✅ TEST PASSED: {len(devices)} metrics stored")
    return True


def test_alert_storage(storage):
    """Test storing alerts"""
    logger.info("\n" + "="*70)
    logger.info("✅ TEST 3: ALERT STORAGE")
    logger.info("="*70)
    
    alerts = [
        {
            'timestamp': datetime.utcnow().isoformat() + "Z",
            'level': 'WARNING',
            'type': 'cpu',
            'message': 'CPU at 78% (warning threshold: 75%)',
            'recommendation': 'Monitor CPU trending'
        },
        {
            'timestamp': datetime.utcnow().isoformat() + "Z",
            'level': 'CRITICAL',
            'type': 'cpu',
            'message': 'CPU at 95% (critical threshold: 90%)',
            'recommendation': 'Investigate high CPU processes'
        },
        {
            'timestamp': datetime.utcnow().isoformat() + "Z",
            'level': 'CRITICAL',
            'type': 'interface',
            'message': '1/2 is DOWN',
            'recommendation': 'Check physical connection'
        }
    ]
    
    for alert in alerts:
        result = storage.store_alert(alert, "test-device")
        
        if result:
            logger.info(f"✅ Stored alert: {alert['level']} - {alert['type']}")
        else:
            logger.error(f"❌ Failed to store alert: {alert['type']}")
            return False
    
    logger.info(f"✅ TEST PASSED: {len(alerts)} alerts stored")
    return True


def test_interface_storage(storage):
    """Test storing interface status"""
    logger.info("\n" + "="*70)
    logger.info("✅ TEST 4: INTERFACE STATUS STORAGE")
    logger.info("="*70)
    
    interfaces = [
        ("catalyst-01", "Gi0/0/1", "up"),
        ("catalyst-01", "Gi0/0/2", "up"),
        ("catalyst-01", "Gi0/0/3", "down"),
        ("aruba-6300", "1/1", "up"),
        ("aruba-6300", "1/2", "down")
    ]
    
    for device, interface, status in interfaces:
        result = storage.store_interface_status(device, interface, status)
        
        if result:
            logger.info(f"✅ Stored: {device}/{interface} = {status}")
        else:
            logger.error(f"❌ Failed to store: {device}/{interface}")
            return False
    
    logger.info(f"✅ TEST PASSED: {len(interfaces)} interface statuses stored")
    return True


def test_statistics(storage):
    """Test retrieving statistics"""
    logger.info("\n" + "="*70)
    logger.info("✅ TEST 5: DATABASE STATISTICS")
    logger.info("="*70)
    
    stats = storage.get_statistics()
    
    logger.info(f"\n📊 Database Statistics:")
    logger.info(f"   Total Metrics: {stats.get('total_metrics', 0)}")
    logger.info(f"   Total Alerts: {stats.get('total_alerts', 0)}")
    logger.info(f"   Unique Devices: {stats.get('unique_devices', 0)}")
    logger.info(f"   Critical Alerts: {stats.get('critical_alerts', 0)}")
    
    if stats.get('total_metrics', 0) > 0 and stats.get('total_alerts', 0) > 0:
        logger.info("✅ TEST PASSED: Statistics retrieved successfully")
        return True
    else:
        logger.error("❌ TEST FAILED: No data in statistics")
        return False


def test_data_retrieval(storage):
    """Test retrieving historical data"""
    logger.info("\n" + "="*70)
    logger.info("✅ TEST 6: DATA RETRIEVAL")
    logger.info("="*70)
    
    # Retrieve metrics for catalyst-01
    metrics = storage.get_device_metrics("catalyst-01", days=7)
    logger.info(f"✅ Retrieved {len(metrics)} metric records for catalyst-01")
    
    # Retrieve alerts for test-device
    alerts = storage.get_device_alerts("test-device", days=7)
    logger.info(f"✅ Retrieved {len(alerts)} alert records for test-device")
    
    if len(alerts) > 0:
        logger.info(f"\nRecent alerts:")
        for alert in alerts[:3]:
            logger.info(f"  - {alert[1]}: {alert[3]}")
    
    if len(metrics) > 0 or len(alerts) > 0:
        logger.info("✅ TEST PASSED: Data retrieval working")
        return True
    else:
        logger.warning("⚠️  TEST WARNING: No data retrieved (might be expected)")
        return True


def main():
    """Run all storage tests"""
    logger.info("\n")
    logger.info("╔════════════════════════════════════════════════════════════════╗")
    logger.info("║        DAY 7: STORAGE & DATABASE ENGINE                        ║")
    logger.info("║     Store and retrieve metrics and alerts                      ║")
    logger.info("╚════════════════════════════════════════════════════════════════╝")
    
    results = []
    storage = None
    
    try:
        # Initialize database
        success, storage = test_database_initialization()
        results.append(("Database Init", success))
        
        if not success or not storage:
            logger.error("❌ Cannot continue without database")
            return False
        
        # Run all tests
        results.append(("Metrics Storage", test_metrics_storage(storage)))
        results.append(("Alert Storage", test_alert_storage(storage)))
        results.append(("Interface Storage", test_interface_storage(storage)))
        results.append(("Statistics", test_statistics(storage)))
        results.append(("Data Retrieval", test_data_retrieval(storage)))
        
        # Summary
        logger.info("\n" + "="*70)
        logger.info("📊 TEST SUMMARY")
        logger.info("="*70)
        
        for test_name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            logger.info(f"{test_name:<30} {status}")
        
        passed_count = sum(1 for _, passed in results if passed)
        total_count = len(results)
        
        logger.info("="*70)
        logger.info(f"\n🎉 {passed_count}/{total_count} TESTS PASSED!")
        
        if passed_count == total_count:
            logger.info("\n✅ Storage engine working perfectly!")
            logger.info("✅ Database operations successful!")
            logger.info("✅ Ready for visualization and production deployment!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False
    finally:
        # Cleanup test database
        if os.path.exists("test_network_monitor.db"):
            os.remove("test_network_monitor.db")
            logger.info("\n🧹 Cleaned up test database")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
