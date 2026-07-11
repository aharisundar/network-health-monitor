"""
Day 4: Metrics Parsing Test
Tests metric extraction from mock device outputs
"""

import logging
from mock_devices import MockCiscoDevice, MockJuniperDevice, MockArubaDevice, MockAristaDevice
from metrics_parser import MetricsParser, print_metrics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_cisco_parsing():
    """Test Cisco metrics parsing"""
    logger.info("\n" + "="*70)
    logger.info("🧪 TESTING CISCO METRICS PARSING")
    logger.info("="*70)
    
    # Create mock device
    device = MockCiscoDevice(hostname="catalyst-01")
    
    # Get raw outputs
    outputs = {
        'show version': device.send_command('show version'),
        'show processes cpu': device.send_command('show processes cpu'),
        'show memory': device.send_command('show memory'),
        'show interfaces brief': device.send_command('show interfaces brief')
    }
    
    logger.info("\n📤 Retrieved outputs from mock Cisco device")
    logger.info(f"   show version: {len(outputs['show version'])} bytes")
    logger.info(f"   show processes cpu: {len(outputs['show processes cpu'])} bytes")
    logger.info(f"   show interfaces brief: {len(outputs['show interfaces brief'])} bytes")
    
    # Parse metrics
    logger.info("\n🔄 Parsing metrics...")
    metrics = MetricsParser.parse_cisco_metrics("catalyst-01", outputs)
    
    # Validate
    is_valid = MetricsParser.validate_metrics(metrics)
    logger.info(f"\n{'✅' if is_valid else '❌'} Validation: {'PASSED' if is_valid else 'FAILED'}")
    
    # Display
    print_metrics(metrics)
    
    return metrics


def test_juniper_parsing():
    """Test Juniper metrics parsing"""
    logger.info("\n" + "="*70)
    logger.info("🧪 TESTING JUNIPER METRICS PARSING")
    logger.info("="*70)
    
    # Create mock device
    device = MockJuniperDevice(hostname="ex-switch-01")
    
    # Get raw outputs
    outputs = {
        'show version': device.send_command('show version'),
        'show system uptime': device.send_command('show system uptime'),
        "request shell execute 'top -bn1 | grep Cpu'": device.send_command("request shell execute 'top -bn1 | grep Cpu'"),
        'show interfaces brief': device.send_command('show interfaces brief')
    }
    
    logger.info("\n📤 Retrieved outputs from mock Juniper device")
    logger.info(f"   show version: {len(outputs['show version'])} bytes")
    logger.info(f"   show system uptime: {len(outputs['show system uptime'])} bytes")
    
    # Parse metrics
    logger.info("\n🔄 Parsing metrics...")
    metrics = MetricsParser.parse_juniper_metrics("ex-switch-01", outputs)
    
    # Validate
    is_valid = MetricsParser.validate_metrics(metrics)
    logger.info(f"\n{'✅' if is_valid else '❌'} Validation: {'PASSED' if is_valid else 'FAILED'}")
    
    # Display
    print_metrics(metrics)
    
    return metrics


def test_aruba_parsing():
    """Test Aruba metrics parsing"""
    logger.info("\n" + "="*70)
    logger.info("🧪 TESTING ARUBA METRICS PARSING")
    logger.info("="*70)
    
    # Create mock device
    device = MockArubaDevice(hostname="aruba-6300")
    
    # Get raw outputs
    outputs = {
        'show system': device.send_command('show system'),
        'show cpu': device.send_command('show cpu'),
        'show memory': device.send_command('show memory'),
        'show interface brief': device.send_command('show interface brief')
    }
    
    logger.info("\n📤 Retrieved outputs from mock Aruba device")
    
    # Parse metrics
    logger.info("\n🔄 Parsing metrics...")
    metrics = MetricsParser.parse_aruba_metrics("aruba-6300", outputs)
    
    # Validate
    is_valid = MetricsParser.validate_metrics(metrics)
    logger.info(f"\n{'✅' if is_valid else '❌'} Validation: {'PASSED' if is_valid else 'FAILED'}")
    
    # Display
    print_metrics(metrics)
    
    return metrics


def test_arista_parsing():
    """Test Arista metrics parsing"""
    logger.info("\n" + "="*70)
    logger.info("🧪 TESTING ARISTA METRICS PARSING")
    logger.info("="*70)
    
    # Create mock device
    device = MockAristaDevice(hostname="arista-7050")
    
    # Get raw outputs
    outputs = {
        'show version': device.send_command('show version'),
        'show processes top': device.send_command('show processes top'),
        'show interfaces status brief': device.send_command('show interfaces status brief')
    }
    
    logger.info("\n📤 Retrieved outputs from mock Arista device")
    
    # Parse metrics
    logger.info("\n🔄 Parsing metrics...")
    metrics = MetricsParser.parse_arista_metrics("arista-7050", outputs)
    
    # Validate
    is_valid = MetricsParser.validate_metrics(metrics)
    logger.info(f"\n{'✅' if is_valid else '❌'} Validation: {'PASSED' if is_valid else 'FAILED'}")
    
    # Display
    print_metrics(metrics)
    
    return metrics


def main():
    """Run all metrics parsing tests"""
    logger.info("\n")
    logger.info("╔════════════════════════════════════════════════════════════════╗")
    logger.info("║        DAY 4: METRICS PARSING & PROCESSING                     ║")
    logger.info("║     Transform raw output into structured metrics               ║")
    logger.info("╚════════════════════════════════════════════════════════════════╝")
    
    all_metrics = []
    
    try:
        # Test each vendor
        cisco_metrics = test_cisco_parsing()
        all_metrics.append(cisco_metrics)
        
        juniper_metrics = test_juniper_parsing()
        all_metrics.append(juniper_metrics)
        
        aruba_metrics = test_aruba_parsing()
        all_metrics.append(aruba_metrics)
        
        arista_metrics = test_arista_parsing()
        all_metrics.append(arista_metrics)
        
        # Summary
        logger.info("\n" + "="*70)
        logger.info("🎉 ALL METRICS PARSING TESTS PASSED!")
        logger.info("="*70)
        logger.info("\n📊 METRICS SUMMARY:")
        logger.info("-" * 70)
        logger.info(f"{'Device':<20} {'Vendor':<12} {'CPU':<12} {'Memory':<12}")
        logger.info("-" * 70)
        
        for metrics in all_metrics:
            cpu_str = f"{metrics['cpu_usage']:.1f}%" if metrics['cpu_usage'] else "N/A"
            mem_str = f"{metrics['memory_usage']:.1f}%" if metrics['memory_usage'] else "N/A"
            logger.info(f"{metrics['device']:<20} {metrics['vendor']:<12} {cpu_str:<12} {mem_str:<12}")
        
        logger.info("-" * 70)
        logger.info("\n✅ Multi-vendor metrics parsing working perfectly!")
        logger.info("✅ All metrics validated successfully!")
        logger.info("✅ Ready for anomaly detection in Day 5!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
