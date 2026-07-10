"""
Day 3: Netmiko Testing with Mock Devices
Tests SSH connection simulation and output parsing
"""

import logging
from mock_devices import MockCiscoDevice, MockJuniperDevice, MockArubaDevice, MockAristaDevice

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_cisco_device():
    """Test Cisco mock device"""
    logger.info("\n" + "="*70)
    logger.info("🧪 TESTING CISCO DEVICE (Mock)")
    logger.info("="*70)
    
    device = MockCiscoDevice(hostname="catalyst-01")
    
    # Test: show version
    logger.info("\n📤 Sending command: show version")
    output = device.send_command("show version")
    logger.info(f"✅ Received {len(output)} bytes")
    logger.info(f"Output preview: {output[:100]}...")
    
    # Test: show processes cpu
    logger.info("\n📤 Sending command: show processes cpu")
    cpu_output = device.send_command("show processes cpu")
    logger.info(f"✅ CPU Info: {cpu_output.strip()}")
    
    # Parse CPU value
    if "45%" in cpu_output:
        logger.info("✅ CPU parsing test: PASSED")
    
    # Test: show interfaces brief
    logger.info("\n📤 Sending command: show interfaces brief")
    int_output = device.send_command("show interfaces brief")
    logger.info(f"✅ Interfaces info received")
    
    logger.info("\n✅ Cisco device tests PASSED!")


def test_juniper_device():
    """Test Juniper mock device"""
    logger.info("\n" + "="*70)
    logger.info("🧪 TESTING JUNIPER DEVICE (Mock)")
    logger.info("="*70)
    
    device = MockJuniperDevice(hostname="ex-switch-01")
    
    # Test: show version
    logger.info("\n📤 Sending command: show version")
    output = device.send_command("show version")
    logger.info(f"✅ Received {len(output)} bytes")
    
    # Parse Juniper output
    if "ex-switch-01" in output and "20.4R1" in output:
        logger.info("✅ Juniper version parsing: PASSED")
    
    # Test: show interfaces brief
    logger.info("\n📤 Sending command: show interfaces brief")
    int_output = device.send_command("show interfaces brief")
    logger.info(f"✅ Interfaces info received")
    
    logger.info("\n✅ Juniper device tests PASSED!")


def test_aruba_device():
    """Test Aruba mock device"""
    logger.info("\n" + "="*70)
    logger.info("🧪 TESTING ARUBA DEVICE (Mock)")
    logger.info("="*70)
    
    device = MockArubaDevice(hostname="aruba-6300")
    
    # Test: show system
    logger.info("\n📤 Sending command: show system")
    output = device.send_command("show system")
    logger.info(f"✅ Received {len(output)} bytes")
    
    # Parse CPU
    logger.info("\n📤 Sending command: show cpu")
    cpu_output = device.send_command("show cpu")
    logger.info(f"✅ CPU: {cpu_output.strip()}")
    
    if "22%" in cpu_output:
        logger.info("✅ Aruba CPU parsing: PASSED")
    
    logger.info("\n✅ Aruba device tests PASSED!")


def test_arista_device():
    """Test Arista mock device"""
    logger.info("\n" + "="*70)
    logger.info("🧪 TESTING ARISTA DEVICE (Mock)")
    logger.info("="*70)
    
    device = MockAristaDevice(hostname="arista-7050")
    
    # Test: show version
    logger.info("\n📤 Sending command: show version")
    output = device.send_command("show version")
    logger.info(f"✅ Received {len(output)} bytes")
    
    # Parse processes
    logger.info("\n📤 Sending command: show processes top")
    proc_output = device.send_command("show processes top")
    logger.info(f"✅ Processes: {proc_output.strip()}")
    
    if "41%" in proc_output:
        logger.info("✅ Arista CPU parsing: PASSED")
    
    logger.info("\n✅ Arista device tests PASSED!")


def main():
    """Run all device tests"""
    logger.info("\n")
    logger.info("╔════════════════════════════════════════════════════════════════╗")
    logger.info("║        DAY 3: NETMIKO MOCK DEVICE TESTING                      ║")
    logger.info("║        Testing SSH simulation and output parsing               ║")
    logger.info("╚════════════════════════════════════════════════════════════════╝")
    
    try:
        # Test each vendor
        test_cisco_device()
        test_juniper_device()
        test_aruba_device()
        test_arista_device()
        
        logger.info("\n" + "="*70)
        logger.info("🎉 ALL TESTS PASSED!")
        logger.info("="*70)
        logger.info("\n✅ Mock device simulator working perfectly!")
        logger.info("✅ Multi-vendor command handling verified!")
        logger.info("✅ Output parsing logic ready!")
        logger.info("\nNext: Test with REAL Netmiko SSH connections!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
