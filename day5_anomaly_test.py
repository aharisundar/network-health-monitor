"""
Day 5: Anomaly Detection Test
Tests threshold-based anomaly detection
"""

import logging
from datetime import datetime
from anomaly_detector import AnomalyDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_test_metrics(device_name, vendor, cpu, memory, interfaces):
    """Create test metrics"""
    return {
        'device': device_name,
        'vendor': vendor,
        'cpu_usage': cpu,
        'memory_usage': memory,
        'interfaces': interfaces,
        'timestamp': datetime.utcnow().isoformat() + "Z"
    }


def test_normal_metrics():
    """Test normal metrics (no anomalies)"""
    logger.info("\n" + "="*70)
    logger.info("✅ TEST 1: NORMAL METRICS (No Anomalies)")
    logger.info("="*70)
    
    detector = AnomalyDetector()
    
    metrics = create_test_metrics(
        device_name="catalyst-01",
        vendor="cisco",
        cpu=45.0,
        memory=62.8,
        interfaces={"Gi0/0/1": {"status": "up"}, "Gi0/0/2": {"status": "up"}}
    )
    
    logger.info(f"📊 Testing device: {metrics['device']}")
    logger.info(f"   CPU: {metrics['cpu_usage']}%")
    logger.info(f"   Memory: {metrics['memory_usage']}%")
    
    anomalies = detector.detect_anomalies(metrics)
    
    if not anomalies['alerts']:
        logger.info("✅ TEST PASSED: No anomalies detected (as expected)")
    else:
        logger.error("❌ TEST FAILED: Unexpected anomalies detected")
    
    return len(anomalies['alerts']) == 0


def test_cpu_warning():
    """Test CPU warning threshold"""
    logger.info("\n" + "="*70)
    logger.info("⚠️  TEST 2: CPU WARNING THRESHOLD")
    logger.info("="*70)
    
    detector = AnomalyDetector()
    
    metrics = create_test_metrics(
        device_name="asr-01",
        vendor="cisco",
        cpu=78.0,
        memory=62.8,
        interfaces={"Gi0/0/1": {"status": "up"}}
    )
    
    logger.info(f"📊 Testing device: {metrics['device']}")
    logger.info(f"   CPU: {metrics['cpu_usage']}% (warning threshold: 75%)")
    
    anomalies = detector.detect_anomalies(metrics)
    
    if anomalies['alerts'] and anomalies['alerts'][0]['level'] == 'WARNING':
        logger.info("✅ TEST PASSED: CPU warning detected correctly")
    else:
        logger.error("❌ TEST FAILED: CPU warning not detected")
    
    return anomalies['alerts'] and anomalies['alerts'][0]['level'] == 'WARNING'


def test_cpu_critical():
    """Test CPU critical threshold"""
    logger.info("\n" + "="*70)
    logger.info("🚨 TEST 3: CPU CRITICAL THRESHOLD")
    logger.info("="*70)
    
    detector = AnomalyDetector()
    
    metrics = create_test_metrics(
        device_name="nexus-01",
        vendor="cisco",
        cpu=95.0,
        memory=62.8,
        interfaces={"Eth1/1": {"status": "up"}}
    )
    
    logger.info(f"📊 Testing device: {metrics['device']}")
    logger.info(f"   CPU: {metrics['cpu_usage']}% (critical threshold: 90%)")
    
    anomalies = detector.detect_anomalies(metrics)
    
    if anomalies['alerts'] and anomalies['alerts'][0]['level'] == 'CRITICAL':
        logger.info("✅ TEST PASSED: CPU critical alert detected correctly")
    else:
        logger.error("❌ TEST FAILED: CPU critical alert not detected")
    
    return anomalies['alerts'] and anomalies['alerts'][0]['level'] == 'CRITICAL'


def test_memory_warning():
    """Test memory warning threshold"""
    logger.info("\n" + "="*70)
    logger.info("⚠️  TEST 4: MEMORY WARNING THRESHOLD")
    logger.info("="*70)
    
    detector = AnomalyDetector()
    
    metrics = create_test_metrics(
        device_name="ex-switch-01",
        vendor="juniper",
        cpu=45.0,
        memory=80.0,
        interfaces={"ge-0/0/0": {"status": "up"}}
    )
    
    logger.info(f"📊 Testing device: {metrics['device']}")
    logger.info(f"   Memory: {metrics['memory_usage']}% (warning threshold: 75%)")
    
    anomalies = detector.detect_anomalies(metrics)
    
    if anomalies['alerts'] and anomalies['alerts'][0]['level'] == 'WARNING':
        logger.info("✅ TEST PASSED: Memory warning detected correctly")
    else:
        logger.error("❌ TEST FAILED: Memory warning not detected")
    
    return anomalies['alerts'] and anomalies['alerts'][0]['level'] == 'WARNING'


def test_interface_down():
    """Test interface down detection"""
    logger.info("\n" + "="*70)
    logger.info("🚨 TEST 5: INTERFACE DOWN DETECTION")
    logger.info("="*70)
    
    detector = AnomalyDetector()
    
    metrics = create_test_metrics(
        device_name="aruba-6300",
        vendor="aruba",
        cpu=22.0,
        memory=38.0,
        interfaces={
            "1/1": {"status": "up"},
            "1/2": {"status": "down"},
            "1/3": {"status": "up"}
        }
    )
    
    logger.info(f"📊 Testing device: {metrics['device']}")
    logger.info(f"   Interfaces: 3 total (1 down)")
    
    anomalies = detector.detect_anomalies(metrics)
    
    has_down_alert = any(alert['level'] == 'CRITICAL' for alert in anomalies['alerts'])
    if has_down_alert:
        logger.info("✅ TEST PASSED: Interface down alert detected correctly")
    else:
        logger.error("❌ TEST FAILED: Interface down alert not detected")
    
    return has_down_alert


def main():
    """Run all anomaly detection tests"""
    logger.info("\n")
    logger.info("╔════════════════════════════════════════════════════════════════╗")
    logger.info("║        DAY 5: ANOMALY DETECTION ENGINE                         ║")
    logger.info("║     Threshold-based anomaly detection                          ║")
    logger.info("╚════════════════════════════════════════════════════════════════╝")
    
    results = []
    
    try:
        # Run all tests
        results.append(("Normal Metrics", test_normal_metrics()))
        results.append(("CPU Warning", test_cpu_warning()))
        results.append(("CPU Critical", test_cpu_critical()))
        results.append(("Memory Warning", test_memory_warning()))
        results.append(("Interface Down", test_interface_down()))
        
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
            logger.info("\n✅ Anomaly detection engine working perfectly!")
            logger.info("✅ All thresholds detecting correctly!")
            logger.info("✅ Ready for alert generation in Day 6!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False
    
    return passed_count == total_count


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
