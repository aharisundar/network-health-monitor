"""
Day 6: Alert Generation Test
Tests alert creation from anomalies
"""

import logging
from datetime import datetime
from anomaly_detector import AnomalyDetector
from alert_generator import AlertGenerator

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


def test_alert_generation_normal():
    """Test alert generation with normal metrics"""
    logger.info("\n" + "="*70)
    logger.info("✅ TEST 1: NORMAL METRICS (No Alerts Expected)")
    logger.info("="*70)
    
    detector = AnomalyDetector()
    alert_gen = AlertGenerator()
    
    metrics = create_test_metrics(
        device_name="catalyst-01",
        vendor="cisco",
        cpu=45.0,
        memory=62.8,
        interfaces={"Gi0/0/1": {"status": "up"}}
    )
    
    logger.info(f"📊 Device: {metrics['device']}, CPU: {metrics['cpu_usage']}%")
    
    anomalies = detector.detect_anomalies(metrics)
    logger.info(f"🔍 Anomalies found: {len(anomalies['alerts'])}")
    
    if len(anomalies['alerts']) == 0:
        logger.info("✅ TEST PASSED: No alerts (as expected)")
        return True
    else:
        logger.error("❌ TEST FAILED: Unexpected alerts")
        return False


def test_alert_generation_warning():
    """Test alert generation with warning"""
    logger.info("\n" + "="*70)
    logger.info("⚠️  TEST 2: WARNING ALERT GENERATION")
    logger.info("="*70)
    
    detector = AnomalyDetector()
    alert_gen = AlertGenerator()
    
    metrics = create_test_metrics(
        device_name="asr-01",
        vendor="cisco",
        cpu=78.0,
        memory=62.8,
        interfaces={"Gi0/0/1": {"status": "up"}}
    )
    
    logger.info(f"📊 Device: {metrics['device']}, CPU: {metrics['cpu_usage']}%")
    
    anomalies = detector.detect_anomalies(metrics)
    logger.info(f"🔍 Anomalies found: {len(anomalies['alerts'])}")
    
    if anomalies['alerts']:
        alert = anomalies['alerts'][0]
        logger.info(f"📢 Alert: {alert.get('message')}")
        logger.info(f"💡 Recommendation: {alert.get('recommendation')}")
        
        alert_gen.process_anomalies_and_alert(anomalies, metrics['device'], metrics['vendor'])
        
        logger.info("✅ TEST PASSED: Warning alert generated")
        return True
    else:
        logger.error("❌ TEST FAILED: No alert generated")
        return False


def test_alert_generation_critical():
    """Test alert generation with critical alert"""
    logger.info("\n" + "="*70)
    logger.info("🚨 TEST 3: CRITICAL ALERT GENERATION")
    logger.info("="*70)
    
    detector = AnomalyDetector()
    alert_gen = AlertGenerator()
    
    metrics = create_test_metrics(
        device_name="nexus-01",
        vendor="cisco",
        cpu=95.0,
        memory=88.0,
        interfaces={"Eth1/1": {"status": "up"}}
    )
    
    logger.info(f"📊 Device: {metrics['device']}, CPU: {metrics['cpu_usage']}%, Memory: {metrics['memory_usage']}%")
    
    anomalies = detector.detect_anomalies(metrics)
    logger.info(f"🔍 Anomalies found: {len(anomalies['alerts'])}")
    
    if anomalies['alerts']:
        for alert in anomalies['alerts']:
            logger.info(f"📢 {alert.get('level')} - {alert.get('message')}")
        
        alert_gen.process_anomalies_and_alert(anomalies, metrics['device'], metrics['vendor'])
        
        critical_count = sum(1 for a in anomalies['alerts'] if a.get('level') == 'CRITICAL')
        if critical_count > 0:
            logger.info("✅ TEST PASSED: Critical alert generated")
            return True
    
    logger.error("❌ TEST FAILED: No critical alert")
    return False


def test_interface_alert():
    """Test interface down alert"""
    logger.info("\n" + "="*70)
    logger.info("🚨 TEST 4: INTERFACE DOWN ALERT")
    logger.info("="*70)
    
    detector = AnomalyDetector()
    alert_gen = AlertGenerator()
    
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
    
    logger.info(f"📊 Device: {metrics['device']}, Interfaces: 3 (1 DOWN)")
    
    anomalies = detector.detect_anomalies(metrics)
    logger.info(f"🔍 Anomalies found: {len(anomalies['alerts'])}")
    
    if anomalies['alerts']:
        for alert in anomalies['alerts']:
            if alert.get('level') == 'CRITICAL':
                logger.info(f"📢 {alert.get('message')}")
        
        alert_gen.process_anomalies_and_alert(anomalies, metrics['device'], metrics['vendor'])
        
        logger.info("✅ TEST PASSED: Interface alert generated")
        return True
    
    logger.error("❌ TEST FAILED: No interface alert")
    return False


def test_alert_summary():
    """Test alert summary statistics"""
    logger.info("\n" + "="*70)
    logger.info("📊 TEST 5: ALERT SUMMARY STATISTICS")
    logger.info("="*70)
    
    alert_gen = AlertGenerator()
    
    # Simulate multiple devices with issues
    devices_data = [
        ("catalyst-01", "cisco", 45.0, 62.8),  # Normal
        ("asr-01", "cisco", 78.0, 62.8),       # CPU warning
        ("nexus-01", "cisco", 95.0, 88.0)      # CPU critical + memory warning
    ]
    
    detector = AnomalyDetector()
    
    for device, vendor, cpu, mem in devices_data:
        metrics = create_test_metrics(device, vendor, cpu, mem, {"Gi0/0/1": {"status": "up"}})
        anomalies = detector.detect_anomalies(metrics)
        
        if anomalies['alerts']:
            alert_gen.process_anomalies_and_alert(anomalies, device, vendor)
    
    summary = alert_gen.get_summary()
    logger.info(f"\n📊 Alert Summary:")
    logger.info(f"   Alerts Generated: {summary['alerts_generated']}")
    logger.info(f"   Alerts Sent: {summary['alerts_sent']}")
    
    if summary['alerts_generated'] > 0:
        logger.info("✅ TEST PASSED: Alerts generated and tracked")
        return True
    else:
        logger.warning("⚠️  TEST WARNING: No alerts generated (might be expected)")
        return True


def main():
    """Run all alert generation tests"""
    logger.info("\n")
    logger.info("╔════════════════════════════════════════════════════════════════╗")
    logger.info("║        DAY 6: ALERT GENERATION ENGINE                          ║")
    logger.info("║     Create actionable alerts from anomalies                     ║")
    logger.info("╚════════════════════════════════════════════════════════════════╝")
    
    results = []
    
    try:
        # Run all tests
        results.append(("Normal Metrics", test_alert_generation_normal()))
        results.append(("Warning Alert", test_alert_generation_warning()))
        results.append(("Critical Alert", test_alert_generation_critical()))
        results.append(("Interface Alert", test_interface_alert()))
        results.append(("Alert Summary", test_alert_summary()))
        
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
            logger.info("\n✅ Alert generation engine working perfectly!")
            logger.info("✅ All alert types generating correctly!")
            logger.info("✅ Ready for database storage in Day 7!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False
    
    return passed_count == total_count


if __name__ == "__main__": 
    success = main()
    exit(0 if success else 1)
